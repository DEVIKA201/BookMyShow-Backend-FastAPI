from pydantic import BaseModel
from datetime import date

######### Booking ########
class BookingBase(BaseModel):
    user_id :int
    show_id : int
    booking_status : str
    booking_date : date

class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    id: int
    class Config:
        from_attributes: True