from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.config.postgres_config import get_db
from app.models.postgres import user_model
from app.schemas.user_schema import UserCreate, UserUpdate, UserRead
from app.services.user_service import create_user, read_user, update_user,delete_user

user_router = APIRouter(prefix="/users", tags=["Users"])

############# create user ###########
@user_router.post("/",response_model=UserCreate)
async def create_new_user(user:UserCreate, db:Session= Depends(get_db)):
    return create_user(db, user)

############ get user ############
@user_router.get("/{user_id}", response_model=UserRead)
async def get_users(
    user_id : Optional[int] = None,
    db: Session = Depends(get_db)
):
    user = read_user(db, user_id)
    if user_id is not None and not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user
    
############# update user ###########
@user_router.put("/{user_id}",response_model=UserRead)
async def update_existing_user(user:UserUpdate, user_id:int, db: Session=Depends(get_db)):
    update_existing_user = update_user(db, user, user_id)
    if not update_existing_user:
        raise HTTPException(status_code=404, detail="User not found!")
    return update_existing_user

############## delete user #############3
@user_router.delete("/{user_id}",response_model= UserRead)
async def delete_existing_user(user_id:int, db:Session = Depends(get_db)):
    delete_existing_user = delete_user(db,user_id)
    if delete_existing_user:
        return delete_existing_user
    raise HTTPException(status_code=404, detail="User not found")