from sqlalchemy import Column, Integer,String, ForeignKey,Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.postgres import Base

class Location(Base):
    __tablename__= 'locations'

    location_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    venues = relationship("Venue", back_populates="location")
    users = relationship("User", back_populates="locations")

class Venue(Base):
    __tablename__= "venues"
    venue_id = Column(Integer, primary_key=True)
    venue_name = Column(String)
    location_id = Column(Integer, ForeignKey("locations.location_id"))
    description = Column(String)
    facilities = Column(JSONB)

    location = relationship("Location", back_populates="venues")
    screens = relationship("Screen", back_populates="venue")