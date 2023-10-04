from pydantic import BaseModel, EmailStr
from typing import Optional, Generic, TypeVar, List
from pydantic.generics import GenericModel

T = TypeVar('T')


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]

class UserSchema(BaseModel):
    id: Optional[str] = None
    username: str
    full_name: str
    email: Optional[str] = None
    password: Optional[str] = None
    image: Optional[str] = None
    my_department_id: Optional[int] = None

class DepartmentSchema(BaseModel):
    id: Optional[str] = None#= Field(defult='', alias='_id')
    name: str
    department_head_email: EmailStr
    no_of_emaployee: int
    department_head: Optional[str] = None
    employees: Optional[List[UserSchema]] = []

class SignUpSchema(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    refresh_token: str

class LoginSchema(BaseModel):
    access_token: str
    refresh_token: str
