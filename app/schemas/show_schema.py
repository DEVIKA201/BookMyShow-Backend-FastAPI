from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

######### seat layout for screen #####
class SeatRow(BaseModel):
    row: str
    seats : List[int]

class SeatCategory(BaseModel):
    name: str
    price: float
    rows: List[str]

class SeatLayout(BaseModel):
    rows: List[SeatRow]
    category: List[SeatCategory]

######### screen #########
class ScreenBase(BaseModel):
    screen_name: str
    venue_id: int
    seat_layout: SeatLayout

class ScreenCreate(ScreenBase):
    pass

class ScreenRead(ScreenBase):
    screen_id: int
    model_config = {
    "from_attributes": True
}

class ScreenResponse(BaseModel):
    screen_id: int
    screen_name: str

    model_config = {
    "from_attributes": True
}
        
class VenueResponse(BaseModel):
    venue_id: int
    venue_name: str
    description: Optional[str]
    facilities: Optional[dict]
    screens: List[ScreenResponse] = [] 

    model_config = {
    "from_attributes": True
}

######### shows #############
class ShowBase(BaseModel):
    movie_id : str
    screen_id : int
    date : date
    time : time
    language : str

class ShowCreate(ShowBase):
    pass

class ShowRead(ShowBase):
    movie_id: str
    model_config = {
    "from_attributes": True
}
class ShowInfo(BaseModel):
    screen_id: int
    screen_name: str
    date: date
    time: time
    language : str

class ShowVenueResponse(BaseModel):
    venue_id : int
    venue_name: str
    shows : List[ShowInfo]

    model_config = {
    "from_attributes": True
}