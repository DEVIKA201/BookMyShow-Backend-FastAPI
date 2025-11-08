from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from sqlalchemy.orm import Session

from app.config.mongo_config import get_mongo_db
from app.config.postgres_config import get_db

user_router = APIRouter(prefix="/user")


# ------------------- USERS -------------------
from app.schemas.user_schema import UserLoginResponse, UserLogin,UserUpdate, UserRead
from app.services.user_service import user_login, update_user,sign_out_user

#Create/Login user
@user_router.post("/", tags=["User - Users"], response_model=UserLoginResponse)
async def create_new_user(user:UserLogin, db:Session= Depends(get_db)):
    return user_login(db, user)

#Update user
@user_router.put("/{user_id}", tags=["User - Users"], response_model=UserRead)
async def update_existing_user(user:UserUpdate, user_id:int, db: Session=Depends(get_db)):
    update_existing_user = update_user(db, user, user_id)
    if not update_existing_user:
        raise HTTPException(status_code=404, detail="User not found!")
    return update_existing_user

#User Sign Out
@user_router.delete("/{user_id}", tags=["User - Users"], response_model= UserRead)
async def delete_existing_user(user_id:int, db:Session = Depends(get_db)):
    delete_existing_user = sign_out_user(db,user_id)
    if delete_existing_user:
        return delete_existing_user
    raise HTTPException(status_code=404, detail="User not found")


# ------------------- MOVIES -------------------
from app.services.movie_service import get_movie_by_filter, fetch_movie_by_id
from app.services.venue_service import read_location
from app.schemas.venue_schema import LocationRead
from app.schemas.movie_schema import AllMovies, MovieUpdate

#Get available locations
@user_router.get("/explore/locations", tags=["User - Movies"], response_model=List[LocationRead]) 
async def get_locations(db:Session=Depends(get_db)):
    location = read_location(db)
    return location

#Fetch movies by location
@user_router.get("/explore/movies-{location_name}",tags=["User - Movies"], response_model=List[AllMovies])
async def get_movie_given_filters(
    location_name: str,
    language: Optional[str]=Query(None),
    genre: Optional[str]=Query(None),
    format: Optional[str]=Query(None),
    db:Session=Depends(get_db)):
    return await get_movie_by_filter(location_name, db,language, genre,format)


#Fetch movies by id -- get specific movie info
@user_router.get("/movies/{movie_id}",tags=["User - Movies"], response_model=MovieUpdate)
async def get_movie_by_id(movie_id:str):
    return await fetch_movie_by_id(movie_id)


# ------------------- SHOWS -------------------
from app.services.show_service import get_shows_by_movie_and_location , get_movieshows_for_venue

#get shows by movie name and location name
@user_router.get("/movies/{location_name}/{movie_name}/buytickets/",tags=["User - Shows"])
async def get_shows(location_name: str, movie_name: str, format:str=None, language:str=None,
                    db_pg: Session=Depends(get_db), db_mongo:Session= Depends(get_mongo_db)):
    return await get_shows_by_movie_and_location(db_pg, db_mongo, location_name,movie_name, language, format )
    
#get shows by venue name
@user_router.get("/cinemas/{location_name}/{venue_name}/buytickets/",tags=["User - Shows"])
async def get_movie_by_venue(location_name:str, venue_name:str, db:Session=Depends(get_db),db_mongo:Session=Depends(get_mongo_db)):
    res = await get_movieshows_for_venue(db, venue_name,location_name,db_mongo)
    if not res:
        raise HTTPException(status_code=404)
    return res


# ------------------- SEAT LAYOUT -------------------
from app.schemas.booking_schema import LockSeatsRequest
from app.services.seatlayout_service import lock_or_unlock_seats, seat_availability

# Seat lock 
@user_router.post("/lock",tags=["User - Seat Layout"])
def lock_seats(req: LockSeatsRequest, db: Session = Depends(get_db)):
    return lock_or_unlock_seats(db, req, lock=True)

# Seat availability
@user_router.get("/availability",tags=["User - Seat Layout"])
def get_seat_availability(
    show_id: int = Query(..., description="Show ID for which seat availability is needed"),
    select_seats: int = Query(1, ge=1, le=10, description="Number of seats user wants to book"),
    db: Session = Depends(get_db),
):
    return seat_availability(db, show_id=show_id, select_seats=select_seats)


# ------------------- BOOKING -------------------
from app.schemas.booking_schema import  ConfirmBookingRequest
from app.services.booking_service import confirm_booking, get_booking_info

# Confirm booking 
@user_router.post("/confirm", tags=["User - Booking"])
def confirm(req: ConfirmBookingRequest, db: Session = Depends(get_db)):
    return confirm_booking(db, req)

# Get booking info 
@user_router.get("/bookings/{user_id}", tags=["User - Booking"])
async def booking_info(user_id:int, db_mongo = Depends(get_mongo_db),db:Session=Depends(get_db)):
    return await get_booking_info(db,db_mongo,user_id)
