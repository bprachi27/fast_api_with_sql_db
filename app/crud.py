from sqlalchemy.orm import Session
from model import Department, User, BlackListToken
from schema import DepartmentSchema, UserSchema
from typing import Optional
from datetime import datetime

def get_department(db:Session, skip:int=0, limit:int=100):

    return db.query(Department).offset(skip).limit(limit).all()


def get_department_by_id(db:Session, department_id=int):

    return db.query(Department).filter(Department.id == department_id).first()


def create_department(db:Session, department: DepartmentSchema):
    _department =  Department(
        name=department.name,
        no_of_emaployee=department.no_of_emaployee,
        department_head_email=department.department_head_email,
        department_head=department.department_head
    )
    db.add(_department)
    db.commit()
    db.refresh(_department)
    return _department


def remove_department(db:Session, department_id:int):
    _department = get_department_by_id(db, department_id)
    db.delete(_department)
    db.commit()


def update_department(db:Session, department_id:int, name: str, no_of_emaployee: int, department_head_email: Optional[str], department_head: Optional[str]):
    _department = get_department_by_id(db, department_id)
    _department.name = name
    _department.no_of_emaployee = no_of_emaployee
    _department.department_head_email = department_head_email
    _department.department_head = department_head

    db.commit()
    db.refresh(_department)
    return _department


def get_user(db:Session, skip:int=0, limit:int=100):

    return db.query(User).offset(skip).limit(limit).all()


def create_user(db:Session, user: UserSchema):

    _user = User(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        image=user.image,
        my_department_id=user.my_department_id
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def get_user_by_id(db:Session, user_id: int):

    return db.query(User).filter(User.id == user_id).first()


def remove_user(db:Session, user_id:int):
    _user = get_user_by_id(db, user_id)
    db.delete(_user)
    db.commit()


def update_user(db:Session, user_id:int, username: str, full_name: int, email: Optional[str], hash_password: Optional[str], my_department_id:Optional[int]):
    _user = get_user_by_id(db, user_id)
    _user.username = username
    _user.full_name = full_name
    if email: _user.email = email
    if hash_password: _user.password = hash_password 
    _user.my_department_id = my_department_id

    db.commit()
    db.refresh(_user)
    return _user


def verify_refresh_token(db:Session, refresh_token: str):

    return db.query(BlackListToken).filter(BlackListToken.refresh_token == refresh_token)


def create_backlist_token(db:Session, refresh_token:str):

    _blacklist_tokken = BlackListToken(
        refresh_token=refresh_token
    )
    db.add(_blacklist_tokken)
    db.commit()
    db.refresh(_blacklist_tokken)
    return _blacklist_tokken

def remove_balcklist_token_by_timestamp(db: Session, timestamp: datetime):

    db.query(BlackListToken).filter(BlackListToken.created_at <= timestamp).delete()

def update_refrsh_token(db:Session, user: User, refresh_token: str):

    user.refresh_token = refresh_token

    db.commit()
    db.refresh(user)
    
    return user

def get_user_by_username(db:Session, username: str):

    return db.query(User).filter(User.username == username).first()