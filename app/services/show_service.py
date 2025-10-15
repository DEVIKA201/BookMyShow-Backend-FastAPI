from sqlalchemy.orm import Session
from bson import ObjectId

from app.models.postgres.show_model import Show, Screen
from app.models.postgres.venue_model import Venue
from app.schemas.show_schema import SeatLayout, ScreenCreate, ScreenRead, ShowCreate, ShowRead 

########### Screen #############
def create_screen(db:Session, data:ScreenCreate) -> Screen:
    screen_dict = data.model_dump()
    screen = Screen(**screen_dict)
    db.add(screen)
    db.commit()
    db.refresh(screen)
    return screen

def read_screen(db:Session, screen_id :int | None = None):
    query = db.query(Screen)
    if screen_id:
        return query.filter(Screen.screen_id == screen_id)#.first()
    return query.all()

########### Shows #############
def create_show(db:Session, data:ShowCreate) -> Show:
    show = Show(**data.model_dump())
    db.add(show)
    db.commit()
    db.refresh(show)
    return show

def read_show(db:Session, show_id: int | None=None):
    query = db.query(Show)
    if show_id:
        return query.filter(Show.show_id==show_id)#.first()
    return query.all()

def get_show_by_movie(db: Session, movie_id: str):
    query = (
        db.query(
            Venue.venue_id,
            Venue.venue_name,
            Screen.screen_id,
            Screen.screen_name,
            Show.date,
            Show.time,
            Show.language
        )
        .join(Screen, Screen.screen_id == Show.screen_id)
        .join(Venue, Venue.venue_id == Screen.venue_id)
        .filter(Show.movie_id==movie_id)
        .order_by(Venue.venue_id, Show.time)
    )
    result = query.all()

    venue_dict = {}
    for row in result:
        if row.venue_id not in venue_dict:
            venue_dict[row.venue_id] = {
                "venue_id" : row.venue_id,
                "venue_name": row.venue_name,
                "shows":[]
            }
        venue_dict[row.venue_id]["shows"].append({
            "screen_id": row.screen_id,
            "screen_name": row.screen_name,
            "date": row.date,
            "time": row.time,
            "language":row.language
        })
    return list(venue_dict.values())