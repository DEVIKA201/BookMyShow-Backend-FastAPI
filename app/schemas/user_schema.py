from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from datetime import date

from app.constants.enums import GenderEnum


class UserBase(BaseModel):
    phone_no: Optional[str]= None
    email: Optional[EmailStr]= None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    bday : Optional[date] = None
    identity : Optional[GenderEnum] = None
    is_married : Optional[bool] =None
    pincode : Optional[int] =None
    address_line1 : Optional[str] =None
    address_line2 : Optional[str]=None
    landmark :Optional[str]= None
    city: Optional[int]=None
    state : Optional[str]=None

    @model_validator(mode='after')  #checks the model instance for phone/mail input
    def check_phone_or_email(self):
        if not self.phone_no and not self.email:
            raise ValueError ("Require either phone or email field")
        return self
    
    
class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    phone_no: Optional[str]= None
    email: Optional[EmailStr]= None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    bday : Optional[date] = None
    identity : Optional[GenderEnum] = None
    is_married : Optional[bool] =None
    pincode : Optional[int] =None
    address_line1 : Optional[str] =None
    address_line2 : Optional[str]=None
    landmark :Optional[str]= None
    city: Optional[int]=None
    state : Optional[str]=None

class UserRead(UserBase):
    user_id: Optional[int]=None