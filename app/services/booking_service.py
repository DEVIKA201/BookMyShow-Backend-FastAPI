from sqlalchemy.orm import Session
from sqlalchemy import text
from bson import ObjectId
from fastapi import HTTPException
from app.models.postgres.seatlayout_model import ShowSeatMap
from app.models.postgres.booking_model import BookingDetail
from app.models.postgres.show_model import ShowSchedule, ShowTiming
from datetime import datetime,timezone, timedelta
from app.services.seatlayout_service import LOCK_EXPIRY_MINUTES

############### GET BOOKING INFO SERVICE ####################

async def get_booking_info(db: Session, db_mongo, user_id: int):
    query = text("""
        SELECT b.booking_id, b.user_id, b.schedule_id, 
            b.show_date, b.show_time, b.language, b.format, b.total_amount,
            b.seats, b.booked_at,
            ss.movie_id, ss.venue_id, ss.screen_id,v.venue_name, s.screen_name
        FROM booking_details b
        JOIN show_schedules ss on ss.schedule_id = b.schedule_id
        JOIN venues v on v.venue_id = ss.venue_id
        JOIN screens s on s.screen_id = ss.screen_id
        WHERE b.user_id = :user_id
        ORDER BY b.booked_at DESC
""")

    result = db.execute(query, {"user_id": user_id}).fetchall()
    if not result:
        return []
    
    movie_id = [r.movie_id for r in result if r.movie_id]
    object_ids = [ObjectId(m_id) for m_id in movie_id if ObjectId.is_valid(m_id)]
    
    mongo_movie_list  = await db_mongo["movie_details"].find(
        {"_id": {"$in": object_ids}}, {"_id": 1, "title": 1}
    ).to_list(length=None)

    movie_map = {str(m["_id"]): m["title"] for m in mongo_movie_list}
    return [
        {
            "booking_id": r.booking_id,
            "user_id": r.user_id,
            "movie_name": movie_map.get(r.movie_id),
            "language": r.language,
            "format": r.format,
            "venue_name": r.venue_name,
            "screen_name": r.screen_name,
            "show_date": r.show_date,
            "show_time": r.show_time,
            "seats": r.seats,
            "total_amount": r.total_amount,
            "booked_at": r.booked_at,            
        }

        for r in result
    ]

############### CONFIRM BOOKING SERVICE ####################
def confirm_booking(db: Session, data):
    now = datetime.now(timezone.utc)

    seat_map = db.query(ShowSeatMap).filter(
        ShowSeatMap.schedule_id == data.schedule_id,
        ShowSeatMap.show_id == data.show_id
    ).first()

    if not seat_map:
        raise HTTPException(status_code=404, detail="Show seat map not found")
    
    if seat_map.locked_at:
        locked_at = seat_map.locked_at
        if locked_at.tzinfo is None:
            locked_at = locked_at.replace(tzinfo = timezone.utc)
        if (now-locked_at)> timedelta(minutes=LOCK_EXPIRY_MINUTES):
            seat_map.locked_seats=[]
            seat_map.locked_at=None
            db.commit()
            raise HTTPException(status_code=400, detail="Seat lock expired.")

    schedule = db.query(ShowSchedule).filter(ShowSchedule.schedule_id == data.schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    show_timing = db.query(ShowTiming).filter(ShowTiming.show_id==data.show_id).first()
    if not show_timing:
        raise HTTPException(status_code=404, detail="Show not found")

    screen = schedule.screen
    layout = screen.seat_layout

    total = 0
    seat_details = []

    for seat in data.seats:
        category, price = derive_category_price(layout, seat.row_name)
        for num in seat.seat_number:
            seat_dict = {"row_name": seat.row_name, "seat_number": num}

            # ✅ Only check if seat is locked, not expired — auto_unlock handles expiry
            if seat_dict not in seat_map.locked_seats:
                raise HTTPException(status_code=400, detail=f"Seat {seat.row_name}{num} not locked or expired")

            total += price
            seat_details.append({
                "row_name": seat.row_name,
                "seat_number": num,
                "category": category,
                "price": price
            })

            # Move seat from locked → booked
            seat_map.locked_seats.remove(seat_dict)
            seat_map.booked_seats.append(seat_dict)

    booking = BookingDetail(
        user_id=data.user_id,
        schedule_id=data.schedule_id,
        show_date = show_timing.show_date,
        show_time = show_timing.show_time,
        format = show_timing.format,
        language = show_timing.language,
        total_amount=total,
        seats=seat_details
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "booking_id": booking.booking_id,
        "total_amount": total,
        "seats": seat_details,
        "booked_at": booking.booked_at
    }

############### HELPER ####################

def derive_category_price(layout, row_name):
    for cat in layout.get("category", []):
        if row_name in cat.get("rows", []):
            return cat["name"], cat["price"]
    raise HTTPException(status_code=400, detail=f"Row {row_name} does not exist in any category")
