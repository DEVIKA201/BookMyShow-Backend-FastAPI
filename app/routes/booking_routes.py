from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.postgres_config import get_db
from app.config.mongo_config import get_mongo_db
from app.schemas.booking_schema import  ConfirmBookingRequest
from app.services.booking_service import confirm_booking, get_booking_info

booking_router = APIRouter(prefix="/booking", tags=["Booking"])

#### Confirm booking ###
@booking_router.post("/confirm")
def confirm(req: ConfirmBookingRequest, db: Session = Depends(get_db)):
    return confirm_booking(db, req)

### Get booking info ###
@booking_router.get("/bookings/{user_id}")
async def booking_info(user_id:int, db_mongo = Depends(get_mongo_db),db:Session=Depends(get_db)):
    return await get_booking_info(db,db_mongo,user_id)
