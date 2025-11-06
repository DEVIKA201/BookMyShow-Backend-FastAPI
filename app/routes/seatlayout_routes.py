from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.config.postgres_config import get_db
from app.schemas.booking_schema import LockSeatsRequest
from app.services.seatlayout_service import lock_or_unlock_seats, seat_availability

seatlayout_router = APIRouter(prefix="/seat_layout", tags=["Seat Layout"])

### Seat lock and unlock ###
@seatlayout_router.post("/lock")
def lock_seats(req: LockSeatsRequest, db: Session = Depends(get_db)):
    return lock_or_unlock_seats(db, req, lock=True)

@seatlayout_router.post("/unlock")
def unlock_seats(req: LockSeatsRequest, db: Session = Depends(get_db)):
    return lock_or_unlock_seats(db, req, lock=False)


############### SEAT AVAILABILITY ####################

@seatlayout_router.get("/availability")
def get_seat_availability(
    show_id: int = Query(..., description="Show ID for which seat availability is needed"),
    select_seats: int = Query(1, ge=1, le=10, description="Number of seats user wants to book"),
    db: Session = Depends(get_db),
):
    return seat_availability(db, show_id=show_id, select_seats=select_seats)
