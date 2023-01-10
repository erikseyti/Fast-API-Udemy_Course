from fastapi import APIRouter, Depends
from todo_app.database import SessionLocal
import models
from todo_app.routers.auth import get_current_user, get_password_hash, get_user_exception
from sqlalchemy.orm import Session

from todo_app.routers.todos import sucessful_response

router = APIRouter(
  prefix='/users_personal',
  tags=['users_personal'],
  responses={404: {'user':'User Not Found'}}
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/')
async def read_all_users(db: SessionLocal = Depends(get_db)):
  return db.query(models.Users).all()


@router.get('/get_user/{user_id}')
async def get_user_with_path(user_id: int,db: SessionLocal = Depends(get_db)):
  return db.query(models.Users).filter(user_id==models.Users.id).first()


@router.get('/get_user/')
async def get_user_with_query(user_id: int,db: SessionLocal = Depends(get_db)):
  return db.query(models.Users).filter(user_id==models.Users.id).first()


@router.put('/change_password/')
async def change_user_password(new_password: str,user: dict = Depends(get_current_user),
db: Session = Depends(get_db)):
  if user is None:
    raise get_user_exception()

  user = db.query(models.Users).filter(models.Users.id== user.get('id')).first()
  user_password_hashed = get_password_hash(new_password)
  user.hashed_password = user_password_hashed

  db.add(user)
  db.commit()

  return sucessful_response(200)

  
@router.delete('/delete_user/{user_id}')
async def delete_user(user_id: int,user: dict = Depends(get_current_user),
db: Session = Depends(get_db)):
  if user is None:
    raise get_user_exception()

  user = db.query(models.Users).filter(models.Users.id== user.get('id')).first()

  db.query(models.Todos).filter(models.Todos.owner_id == user.id).delete()

  db.query(models.Users).filter(models.Users.id == user_id).delete()
  db.commit()

  return sucessful_response(200)