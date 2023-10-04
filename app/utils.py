from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Security
from crud import verify_refresh_token, remove_balcklist_token_by_timestamp


ACCESS_TOKEN_EXPIRE_MINUTES = 1 
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"
SECRET_KEY = "prachi_badami"
EMAIL_USERNAME = "prachibadami.vision@gmail.com"
EMAIL_PASSWORD = "auqkoqffdwmnjbap"


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    return pwd_context.hash(password)

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, db, user_id):
        try: 
            payload = {
                'exp': datetime.utcnow() + timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm=ALGORITHM
            )

        finally:
            #code to delete blacklist token based on time
            balcklist_time = datetime.now() - timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
            remove_balcklist_token_by_timestamp(db, balcklist_time)

    # Function to create refresh token
    def create_refresh_token(self, user_id:str):
        
        data = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            "sub": user_id + SECRET_KEY[::-1]    
        }

        encoded_jwt = jwt.encode(data, SECRET_KEY[::-1], algorithm=ALGORITHM)

        return encoded_jwt

    def decode_token(self, token):
        
        try:

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            return payload['sub']
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')
        

    def decode_refresh_token(self, db, token):
        
        try:
            
            blacklist_token = verify_refresh_token(db, token)
            
            if blacklist_token.count() == 0:
                
                payload: str = jwt.decode(token, SECRET_KEY[::-1], algorithms=[ALGORITHM])
                
                return payload['sub'].replace(SECRET_KEY[::-1], '')
            
            else:      
                
                raise HTTPException(status_code=401, detail='Invalid token')

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

