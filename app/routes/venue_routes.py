from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.config.postgres_config import get_db
from app.schemas.venue_schema import LocationCreate, LocationRead, VenueCreate, VenueRead, ScreenCreate, ScreenResponse
from app.services.venue_service import read_location, create_location, create_venue, read_venue, read_screen, create_screen


########## Location #########
location_router = APIRouter(prefix="/locations", tags=["Locations"])

#create location
@location_router.post("/",response_model=LocationCreate)
async def create_new_location(location:LocationCreate, db:Session=Depends(get_db)):
    return create_location(db,location)

#get location
@location_router.get("/", response_model=List[LocationRead]) #get location by location id
async def get_locations(db:Session=Depends(get_db)):
    location = read_location(db)
    return location

########## Venue #########
venue_router = APIRouter(prefix="/venues", tags=["Venues"])

#create venue
@venue_router.post("/",response_model=VenueCreate)
async def create_new_venue(venue:VenueCreate, db:Session=Depends(get_db)):
    return create_venue(db,venue)

#get venue
@venue_router.get("/",response_model=List[VenueRead])
async def get_venues(
    db:Session=Depends(get_db)):
    venue = read_venue(db)
    return venue


########## Screens #########
screen_router = APIRouter(prefix="/screens",tags=["Screens"])

#create screen
@screen_router.post("/",response_model=ScreenCreate)
async def create_screens(screen:ScreenCreate,db: Session=Depends(get_db)):
    return create_screen(db, screen)
    
@screen_router.get("/",response_model=List[ScreenResponse])
async def get_screen(db:Session=Depends(get_db)):
    screen = read_screen(db)
    return screen