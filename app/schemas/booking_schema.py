from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone

from app.schemas.seatlayout_schema import LockSeatsRequest, SeatInfo

class ConfirmBookingRequest(LockSeatsRequest):
    pass

class BookingResponse(BaseModel):
    booking_id: int
    total_amount: float
    seats: List[SeatInfo]
    booked_at: datetime = datetime.now(timezone.utc)
    
