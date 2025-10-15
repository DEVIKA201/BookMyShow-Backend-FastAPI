from sqlalchemy import Column, Integer, ForeignKey,Enum, DateTime
from sqlalchemy.orm import relationship

from app.constants.enums import BookingEnum
from app.models.postgres import Base

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.user_id"))
    show_id = Column(Integer,ForeignKey("shows.show_id"))
    booking_status = Column(Enum(BookingEnum))
    booking_date = Column(DateTime)

    shows = relationship("Show", back_populates="bookings")
    users = relationship("User",back_populates='bookings')