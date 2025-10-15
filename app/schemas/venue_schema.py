from pydantic import BaseModel
from typing import Optional , List

from app.constants.enums import FacilitiesEnum

##### location #####
class LocationBase(BaseModel):
    name: str

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    location_id: Optional[int]=None

    class Config:
        from_attributes = True

###### venue ######
class VenueBase(BaseModel):
    venue_name : str
    location_id: int
    description : str 
    facilities: List[FacilitiesEnum]

class VenueCreate(VenueBase):
    pass

class VenueRead(VenueBase):
    venue_id:Optional[int]=None
    class Config:
        from_attributes = True



