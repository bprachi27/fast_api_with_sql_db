from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, DateTime
from config import Base
from sqlalchemy.orm import validates, relationship
import re
from sqlalchemy.sql import func

class Department(Base):
    
    __tablename__ = 'department'

    id                      = Column(Integer, primary_key=True, autoincrement="auto")
    name                    = Column(String, nullable=False, unique=True)
    no_of_emaployee         = Column(Integer, nullable=False)
    department_head_email   = Column(String)
    department_head         = Column(String, nullable=True)
    employees               = relationship('User', backref='department')

    __table__args__ = (
        CheckConstraint('value >= 6', name='check_min_value'),
        CheckConstraint('value <= 20', name='check_max_value')
    )

    @validates('department_head_email')
    def validate_email(self, key, value):

        if value and not re.match(r'^[\w\.-]+@[\w\.-]+$', value):
            raise ValueError('Invalid email addess format')
        
        return value
    
    
class User(Base):

    __tablename__= 'user'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    username            = Column(String(50), nullable=False, unique=True)
    full_name           = Column(String, nullable=False)
    email               = Column(String(100), nullable=False, unique=True)
    password            = Column(String, nullable=False)
    image               = Column(String, nullable=True)
    my_department_id    = Column(Integer, ForeignKey('department.id'), nullable=True)
    refresh_token       = Column(String, nullable=True)

    @validates('email')
    def validate_email(self, key, value):

        if value and not re.match(r'^[\w\.-]+@[\w\.-]+$', value):
            raise ValueError('Invalid email addess format')
        
        return value


class BlackListToken(Base):

    __tablename__= 'balcklist_token'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    refresh_token       = Column(String, nullable=False, unique=True) 
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
