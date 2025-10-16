from fastapi import APIRouter,Depends
from typing import List
from sqlalchemy.orm import Session

from app.services.movie_service import get_movies_services, create_movie_service, fetch_movie_by_id, delete_movie_by_id, update_movie_by_id, get_movie_by_location, get_movie_by_venue
from app.schemas.movie_schema import AllMovies,Movie, MovieDelete, MovieUpdate
from app.config.postgres_config import get_db

movie_router = APIRouter(tags=["movies"])

#Create movie
@movie_router.post("/movies/",response_model=Movie)
async def create_movie(movie:Movie):
    return await create_movie_service(movie)

#Fetch movies
@movie_router.get("/movies/",response_model=list[AllMovies])
async def get_movies():
    return await get_movies_services()

#Fetch movies by id
@movie_router.get("/movies/{movie_id}",response_model=MovieUpdate)
async def get_movie_by_id(movie_id:str):
    return await fetch_movie_by_id(movie_id)

#Update movie by id
@movie_router.put("/movies/{movie_id}",response_model=MovieUpdate)
async def update_movie(movie_id:str, movie:MovieUpdate):
    return await update_movie_by_id(movie_id, movie)

#Delete movie by id
@movie_router.delete("/movies/{movie_id}",response_model=MovieDelete)
async def delete_movie(movie_id: str):
    return await delete_movie_by_id(movie_id)

#movies by location filter
@movie_router.get("/movies-{location_name}",response_model=List[AllMovies])
async def get_movie_by_location_filter(location_name: str,db:Session=Depends(get_db)):
    return await get_movie_by_location(location_name, db)

#movie by venue filter
@movie_router.get("/cinemas-{venue_name}",response_model=List[AllMovies])
async def get_movie_by_venue_filter(venue_name: str, db:Session=Depends(get_db)):
    return await get_movie_by_venue(venue_name,db)