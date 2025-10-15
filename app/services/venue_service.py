from sqlalchemy.orm import Session

from app.models.postgres.show_model import Screen
from app.models.postgres.venue_model import Location, Venue
from app.schemas.venue_schema import LocationCreate, VenueCreate, VenueRead

########### Location #############
def create_location(db:Session, data:LocationCreate):
    location = Location(**data.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

def read_location(db:Session, location_id :int | None = None):
    query = db.query(Location)
    if location_id:
        return query.filter(Location.location_id == location_id).first()
    return query.all()

########### Venue #############
def create_venue(db:Session, data:VenueCreate):
    venue = Venue(**data.model_dump())
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

def read_venue(db:Session, venue_id :int | None = None):
    query = db.query(Venue)
    if venue_id:
        return query.filter(Venue.venue_id == venue_id).first()
    return query.all()

