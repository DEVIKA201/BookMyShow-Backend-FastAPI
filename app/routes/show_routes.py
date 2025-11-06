from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.mongo_config import get_mongo_db
from app.config.postgres_config import get_db
from app.schemas.show_schema import ShowScheduleCreate,ShowScheduleRead,ShowTimingCreate,ShowTimingRead
from app.services.show_service import create_schedule,create_schedule_timings, get_shows_by_movie_and_location , get_movieshows_for_venue

show_router = APIRouter(tags=["Shows"])

#create show schedule
@show_router.post("/schedule/",response_model=ShowScheduleRead)
async def create_show_schedules(schedule:ShowScheduleCreate, db: Session= Depends(get_db)):
    return create_schedule(db,schedule)

#create show timings
@show_router.post("/schedule/timings/", response_model=list[ShowTimingRead])
async def create_timings_for_schedule(schedule_id: int,timings: list[ShowTimingCreate],days_ahead :int =10, db: Session = Depends(get_db), db_mongo = Depends(get_mongo_db)):
    return await create_schedule_timings(db, db_mongo,schedule_id, timings, days_ahead)

#get shows by movie name and location name
@show_router.get("/movies/{location_name}/{movie_name}/buytickets/")
async def get_shows(location_name: str, movie_name: str, format:str=None, language:str=None,
                    db_pg: Session=Depends(get_db), db_mongo:Session= Depends(get_mongo_db)):
    return await get_shows_by_movie_and_location(db_pg, db_mongo, location_name,movie_name, language, format )
    
#get shows by venue name
@show_router.get("/cinemas/{location_name}/{venue_name}/buytickets/")
async def get_movie_by_venue(location_name:str, venue_name:str, db:Session=Depends(get_db),db_mongo:Session=Depends(get_mongo_db)):
    res = await get_movieshows_for_venue(db, venue_name,location_name,db_mongo)
    if not res:
        raise HTTPException(status_code=404)
    return res