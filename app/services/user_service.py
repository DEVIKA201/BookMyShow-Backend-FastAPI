from sqlalchemy.orm import Session

from app.models.postgres.user_model import User
from app.schemas.user_schema import UserBase, UserCreate, UserRead, UserUpdate

############ User CRUD #########

def create_user(db:Session, data: UserCreate):
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def read_user(db:Session, user_id: int | None = None):
    query = db.query(User)
    if user_id :
        return query.filter(User.user_id == user_id).first()
    return query.all()

def update_user(db:Session,user: UserUpdate, user_id: int):
    update_query = db.query(User).filter(User.user_id == user_id).first()
    if update_query:
        for key,value in user.model_dump(exclude_unset=True).items():
            setattr(update_query,key,value)
    if not update_query:
        return None
    db.commit()
    db.refresh(update_query)
    return update_query

def delete_user(db:Session, user_id:int):
    delete_query = db.query(User).filter(User.user_id == user_id).first()
    if delete_query:
        db.delete(delete_query)
        db.commit()
    return delete_query
