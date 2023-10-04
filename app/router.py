from fastapi import APIRouter, Depends
from config import sessionLocal
from sqlalchemy.orm import Session
from schema import Response, DepartmentSchema, UserSchema
import crud
from utils import AuthHandler, get_password_hash

router = APIRouter()

def get_db():
    db = sessionLocal()
    
    # it means when request is initiate, it create new db connection 
    # and when request is complete, it will close the db connection
    try:
        yield db
    finally:
        db.close()

auth_handler = AuthHandler()

@router.get('/', response_model=Response,)
def get(db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:
       
        _department = crud.get_department(db, 0, 100)
        
        for department in _department:

            department.employees = department.employees

        return Response(code=200, status="ok", message="Success fetch all data", result=_department).dict(exclude_none=True)
    
    except Exception as e:

        raise

@router.post('/', response_model=Response, status_code=201)
def create(data:DepartmentSchema, db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:

        result = crud.create_department(db,data)

        return Response(code=201, status="ok", message="department created successfully", result=result).dict(exclude_none=True)
    
    except Exception as e:
        
        raise


@router.get('/{id}', response_model=Response)
def get_by_id(id:int,db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:

        _department = crud.get_department_by_id(db, id)
        
        return Response(code=200, status="ok", message="success get data", result=_department).dict(exclude_none=True)

    except Exception as e:

        raise


@router.patch('/{id}', response_model=Response)
def update(id:int, data:DepartmentSchema, db:Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:

        _department = crud.update_department(db, id, data.name, data.no_of_emaployee, data.department_head_email, data.department_head)

        return Response(code=200, status="ok", message="success update data", result=_department).dict(exclude_none=True)
    
    except Exception as e:

        raise


@router.delete('/{id}', response_model=Response)
def delete(id:int, db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:

        crud.remove_department(db, id)
        
        return Response(code=204, status="ok", message="success delete data").dict(exclude_none=True)

    except Exception as e:

        raise


user_router = APIRouter()

@user_router.get('/', response_model=Response, status_code=200) #response_model=List[Response],
def get(db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:

        _users = crud.get_user(db, 0, 100)

        return Response(code=200, status="ok", message="Success fetch all data", result=_users).dict(exclude_none=True)
    
    except Exception as e:

        raise
    

@user_router.post('/', response_model=Response, status_code=201)
def create(data:UserSchema, db:Session=Depends(get_db)):
    try:

        data.password = get_password_hash(data.password)
        result = crud.create_user(db, data)

        return Response(code=201, status="ok", message="user created sucessfully", result=result).dict(exclude_none=True)
    
    except Exception as e:

        raise
    

@user_router.get('/{id}', response_model=Response)
def get_by_id(id:int, db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:
        _user = crud.get_user_by_id(db, id)

        return Response(code=200, status="ok", message="success get data", result=_user).dict(exclude_none=True)

    except Exception as e:

        raise


@user_router.patch('/{id}', response_model=Response)
def update(id:int, data:UserSchema, db:Session = Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:
        if data.password: data.password = get_password_hash(data.password)

        _user = crud.update_user(db, id, data.username, data.full_name, data.email, data.password, data.my_department_id)

        return Response(code=200, status="ok", message="success update data", result=_user).dict(exclude_none=True)
    
    except Exception as e:

        raise


@user_router.delete('/{id}', response_model=Response)
def delete(id:int, db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):
    try:

        crud.remove_user(db, id)
        
        return Response(code=204, status="ok", message="success delete data").dict(exclude_none=True)

    except Exception as e:

        raise

