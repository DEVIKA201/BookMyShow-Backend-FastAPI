from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.config.postgres_config import get_db
from app.models.postgres.show_model import Show
from app.schemas.show_schema import ShowCreate, ShowRead
from app.services.show_service import create_show, read_show,get_show_by_movie
from app.services.movie_service import fetch_movie_by_id

########## Shows #########
show_router = APIRouter(prefix="/shows", tags=["Shows"])

#create show
@show_router.post("/",response_model=ShowRead)
async def create_new_show(show:ShowCreate, db:Session=Depends(get_db)):
    return create_show(db,show)

#get show by movies
@show_router.get("/{movie_id}")
async def get_shows_by_movie(movie_id:str,db:Session=Depends(get_db)):
    movie = await fetch_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    shows = get_show_by_movie(db,movie_id)
    
    return{
        "movie":movie,
        "shows":shows
    }