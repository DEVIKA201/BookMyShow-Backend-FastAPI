from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.postgres import Base

class Show(Base):
    __tablename__="shows"
    show_id = Column(Integer, primary_key=True)
    movie_id = Column(String, index=True)
    screen_id = Column(Integer, ForeignKey("screens.screen_id"))
    date = Column(Date)
    time = Column(Time)
    language = Column(String)

    screen = relationship("Screen",back_populates="shows")
    bookings = relationship("Booking", back_populates="shows")

class Screen(Base):
    __tablename__="screens"
    screen_id = Column(Integer, primary_key=True)
    screen_name = Column(String)
    venue_id = Column(Integer, ForeignKey("venues.venue_id"))
    seat_layout = Column(JSONB)

    venue = relationship("Venue", back_populates="screens")
    shows = relationship("Show",back_populates="screen")