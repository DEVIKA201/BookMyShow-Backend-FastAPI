from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.postgres.seatlayout_model import ShowSeatMap
from app.models.postgres.booking_model import BookingDetail
from app.models.postgres.show_model import ShowTiming, ShowSchedule
from app.models.postgres.venue_model import Screen
from app.constants.enums import SeatStatus
from datetime import datetime,timezone

LOCK_CACHE = {}  
LOCK_EXPIRY_MINUTES = 10

############### SEATS AVAILABILITY SERVICE ####################

def seat_availability(db:Session, show_id: int, select_seats:int=1):
    show_timing = db.query(ShowTiming).filter(ShowTiming.show_id == show_id).first()
    if not show_timing:
        raise HTTPException(status_code=404, detail="No shows found!")
    
    schedule = db.query(ShowSchedule).filter(ShowSchedule.schedule_id==show_timing.schedule_id).first()
    
    show_screen = db.query(Screen).filter(Screen.screen_id==schedule.screen_id).first()
    if not show_screen:
        raise HTTPException(status_code=404, detail="No screen info found!")
    
    #fetch seat layout
    try:
        layout = show_screen.seat_layout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid layout{str(e)}")
    
    rows_info = layout.get("rows",[])
    category_info = layout.get("category",[])
    
    row_to_cat = {}
    cat_to_price ={}
    for cat in category_info:
        cat_name = cat["name"]
        cat_to_price[cat_name] = cat["price"]
        for row_name in cat["rows"]:
            row_to_cat[row_name.upper()] = cat_name
    
    #seat count per category
    available_by_category = {cat["name"]:[] for cat in category_info}

    booked_seats = db.query(BookingDetail).filter(BookingDetail.show_id==show_id).all()
    locked_seats = db.query(ShowSeatMap).filter(ShowSeatMap.show_id==show_id).all()

    booked_set = set()
    for b in booked_seats:
        try:
            seats = b.seats # parse JSON
            for seat in seats:
                booked_set.add((seat["row_name"].upper(), seat["seat_number"]))
        except Exception:
            continue  # skip invalid seat data
    
    locked_set = set()
    for l in locked_seats:
        for seat in l.locked_seats:  
            locked_set.add((seat["row_name"].upper(), seat["seat_number"]))


    #available seat count
    for row in rows_info:
        row_name = row["row"].upper()
        category = row_to_cat.get(row_name)
        if not category: # possible rarely
            continue
        
        for seat_number in row["seats"]:
            key = (row_name, seat_number)
            if key not in booked_set and key not in locked_set:
                available_by_category[category].append({
                    "row_name": row_name,
                    "seat_number": seat_number
                })


    #dynamic seat status checking
    category_status = {}
    for cat in category_info:
        cat_name = cat["name"]
        total = sum(1 for row in rows_info if row_to_cat.get(row["row"].upper()) == cat_name for _ in row["seats"])
        available = len(available_by_category[cat_name])
      
        if total ==0:
            continue
        
        #Update the seat filling status
        percent_left = (available/total)*100
        if available ==0:
            status = SeatStatus.Sold_Out.value
        elif percent_left>0 and percent_left<=10:
            status = SeatStatus.Almost_Full.value
        elif percent_left>10 and percent_left<=20:
            status = SeatStatus.Filling_Fast
        else:
            status = SeatStatus.Available.value

        category_status[cat_name] = {
            "price": f" {cat_to_price[cat_name]}",
            "available seats":available_by_category[cat_name],
            "total":available,
            "status":status
        }
    
    return {
        "show_id":show_id,
        "seats_required":select_seats,
        "category":category_status
    }


############### LOCK/UNLOCK SEATS SERVICE ####################

def lock_or_unlock_seats(db: Session, data, lock: bool = True):

    now = datetime.now(timezone.utc)

    seat_map = (
        db.query(ShowSeatMap)
        .filter(ShowSeatMap.schedule_id == data.schedule_id,
                ShowSeatMap.show_id == data.show_id)
        .first()
    )

    if not seat_map:
        seat_map = ShowSeatMap(schedule_id=data.schedule_id, show_id=data.show_id)
        db.add(seat_map)
        db.commit()
        db.refresh(seat_map)

    if lock:
        for s in data.seats:
            for num in s.seat_number:
                seat_dict = {"row_name": s.row_name, "seat_number": num}
                key = (data.schedule_id, data.show_id, s.row_name, num)

                # Recheck seat availability
                if seat_dict in seat_map.locked_seats or seat_dict in seat_map.booked_seats:
                    raise HTTPException(status_code=400, detail=f"Seat {s.row_name}{num} unavailable")
                seat_map.locked_at = now
                # Lock seat + cache time
                seat_map.locked_seats.append(seat_dict)
                LOCK_CACHE[key] = now

        db.commit()
        return {"message": "Seats locked"}

    else:
        # Unlock flow
        for s in data.seats:
            for num in s.seat_number:
                seat_dict = {"row_name": s.row_name, "seat_number": num}
                key = (data.schedule_id, data.show_id, s.row_name, num)
                if seat_dict in seat_map.locked_seats:
                    seat_map.locked_seats.remove(seat_dict)
                    if not seat_map.locked_seats:  # all unlocked
                        seat_map.locked_at = None

                LOCK_CACHE.pop(key, None)

        db.commit()
        return {"message": "Seats unlocked"}
