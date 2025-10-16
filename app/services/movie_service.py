from fastapi import HTTPException
from bson import ObjectId
from app.config.mongo_config import db
from app.schemas.movie_schema import Movie, AllMovies, MovieUpdate, MovieDelete
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import text
#debug
import sys

#create a movie
async def create_movie_service(movie:Movie):
    movie_dict = movie.model_dump(by_alias=True, exclude_none=True)
    result = await db["movie_details"].insert_one(movie_dict)
    movie_dict["_id"] = str(result.inserted_id)
    return movie_dict

#Fetch all movies
async def get_movies_services():
    movies = await db["movie_details"].find(
        {},
        {"title":1,"language":1,"rating":1}
    ).to_list()
    for movie in movies:
        movie["_id"] = str(movie["_id"])
    return movies

#Fetch movies by id
#get artist details in cast and crew
async def fetch_movie_by_id(movie_id:str):
    pipeline = [
        {"$match":{"_id":ObjectId(movie_id)}},
        {
            "$lookup":{
                "from":"artist_details",
                "localField":"cast._id",
                "foreignField":"_id",
                "as": "cast_info"
            }
        },
        {
            "$lookup":{
                "from":"artist_details",
                "localField":"crew._id",
                "foreignField":"_id",
                "as":"crew_info"
            }
        },
        {
            "$project":{
                "_id": {"$toString": "$_id"},
                "title":1,
                "date_of_release":1,
                "duration":1,
                "language":1,
                "rating":1,
                "format":1,
                "genre":1,
                "about":1,
                "is_active":1,
                "is_available":1,
                "is_stream":1,
                "price_rent":1,
                "price_buy":1,
                "cast":1,
                "crew":1,

                "cast_info":{
                    "$map":{
                        "input":"$cast_info",
                        "as":"person",
                        "in":{
                            "_id":{"$toString":"$$person.id"},
                            "name":"$$person.name",
                            "occupation":"$$person.occupation",
                            "also_known":"$$person.also_known",
                            "birthplace":"$$person.birthplace",
                            "children":"$$person.children",
                            "about":"$$person.about",
                            "spouse":"$$person.spouse",
                            "family":"$$person.family",
                            "peer_and_more":"$$person.peer_and_more"
                        }
                    }
                },
                "crew_info":{
                    "$map":{
                        "input":"$crew_info",
                        "as":"person",
                        "in":{
                            "_id":{"$toString":"$$person.id"},
                            "name":"$$person.name",
                            "occupation":"$$person.occupation",
                            "also_known":"$$person.also_known",
                            "birthplace":"$$person.birthplace",
                            "children":"$$person.children",
                            "about":"$$person.about",
                            "spouse":"$$person.spouse",
                            "family":"$$person.family",
                            "peer_and_more":"$$person.peer_and_more"
                        }
                    }                    
                }
            }
        }
        
    ]

    movie = await db["movie_details"].aggregate(pipeline).to_list(length=1)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie[0]
    
#Update movie by id
async def update_movie_by_id(movie_id:str, movie:MovieUpdate):
    update_data = movie.model_dump(by_alias=True, exclude_none=True)
    result = await db["movie_details"].update_one(
        {"_id":ObjectId(movie_id)},
        {"$set":update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found!")
    updated_movie = await db["movie_details"].find_one({"_id":ObjectId(movie_id)})
    updated_movie["_id"] = str(updated_movie["_id"])
    return updated_movie

#Delete movie by id
async def delete_movie_by_id(movie_id:str):
    result = await db["movie_details"].update_one(
        {"_id":ObjectId(movie_id), "is_available":True},
        {"$set":{"is_available":False}}
    )
    if result.matched_count==0:
        raise HTTPException(status_code=404,detail="Movie doesn't exist")
    return {"message":"Movie deleted successfully"}

##################### Filter APIs ########################

###movie by location filter###
async def get_movie_by_location(location_name:str, s: Session) -> List[dict]:

    #get location id for the given name of location
    location_id = s.execute(text(
        "SELECT location_id FROM locations WHERE name = :loc"),
        {"loc":location_name}
    ).scalar()
    if not location_id:
        return []
    
    #get venue ids for the location
    venue_ids = s.execute(text(
        "SELECT venue_id FROM venues WHERE location_id = :loc"),
        {"loc":location_id}
    ).fetchall()
    venue_ids = [v[0] for v in venue_ids]

    if not venue_ids:
        return []
    
    #get screens in those venues
    screen_ids = s.execute(text(
        "SELECT screen_id FROM screens WHERE venue_id = ANY(:venues)"),
        {"venues":venue_ids}
        ).fetchall()
    screen_ids = [sc[0] for sc in screen_ids]

    if not screen_ids:
        return []
    
    #get the distinct movie ids playing in those screens
    movie_ids = s.execute(text(
        "SELECT movie_id FROM shows WHERE screen_id = ANY(:screens)"),
        {"screens":screen_ids}
    ).fetchall()
    movie_ids = [m[0]for m in movie_ids]

    if not movie_ids:
        return []
    
    #movie_id (postgres) -> objectId (mongo query)
    object_ids = [ObjectId(m_ids) for m_ids in movie_ids]

    #Query mongo to get those movies
    movie_collection = db["movie_details"]
    movie = await movie_collection.find(
        {"_id":{"$in":object_ids}},
        {"title":1,"rating":1,"language":1}
    ).to_list(length=None)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found at theaters near you")
    
    movies = []
    for doc in movie:
        movies.append({
            "_id":str(doc["_id"]),
            "title":str(doc.get("title")),
            "rating":str(doc.get("rating")),
            "language":str(doc.get("language"))
        })
    return movies


###movie by venue filter###


async def get_movie_by_venue(venue_name: str, s:Session) -> List[dict]:
    print("DEBUG - venue_name from API:", venue_name)
    #get venue id for the given name 
    venue_id = s.execute(text(
        "SELECT venue_id FROM venues WHERE venue_name = :loc"),
        {"loc":venue_name}
    ).scalar()
    print("DEBUG - venue_id:", venue_id)
    


#debug
    print("venue_id",venue_id,type(venue_id))

    if not venue_id:
        print("No venue found")
        return []   
    
    # Debugging raw screens query result
    res = s.execute(
        text("SELECT screen_id FROM screens WHERE venue_id = :v"),
        {"v": venue_id}
    )
    print("raw screens rows:", res.fetchall())
    
    #get screens in those venues
    screen_ids = s.execute(text(
        "SELECT screen_id FROM screens WHERE venue_id = :venue"),
        {"venue":venue_id}
        ).fetchall()
    screen_ids = [sc[0] for sc in screen_ids]

    # ✅ Debugging screen_ids
    print("screen_ids:", screen_ids, [type(x) for x in screen_ids])

    if not screen_ids:
        return []
    
    #get the distinct movie ids playing in those screens
    movie_ids = s.execute(text(
        "SELECT movie_id FROM shows WHERE screen_id IN :screens"),
        {"screens":tuple(screen_ids)}
    ).fetchall()
    movie_ids = [m[0]for m in movie_ids]

    # ✅ Debugging movie_ids
    print("movie_ids:", movie_ids, [type(x) for x in movie_ids])

    if not movie_ids:
        return []
    
    #movie_id (postgres) -> objectId (mongo query)
    object_ids = [ObjectId(m_ids) for m_ids in movie_ids]

    # ✅ Debugging object_ids
    print("object_ids:", object_ids)

    #Query mongo to get those movies
    movie_collection = db["movie_details"]
    movie = await movie_collection.find(
        {"_id":{"$in":object_ids}},
        {"title":1,"rating":1,"language":1}
    ).to_list(length=None)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found at theaters near you")
    
    movies = []
    for doc in movie:
        movies.append({
            "_id":str(doc["_id"]),
            "title":str(doc.get("title")),
            "rating":str(doc.get("rating")),
            "language":str(doc.get("language"))
        })
    return movies