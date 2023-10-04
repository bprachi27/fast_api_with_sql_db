from fastapi import FastAPI, Depends, HTTPException, status
import model, router, crud
from config import engine
from utils import AuthHandler
from config import sessionLocal
from sqlalchemy.orm import Session
from schema import SignUpSchema, Response, TokenSchema, LoginSchema

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
auth_handler = AuthHandler()

def get_db():
    db = sessionLocal()
    
    # it means when request is initiate, it create new db connection 
    # and when request is complete, it will close the db connection
    try:
        yield db
    finally:
        db.close()


@app.post('/login', response_model=LoginSchema)
def login(data:SignUpSchema, db:Session=Depends(get_db)):
    try:
        _user = crud.get_user_by_username(db, data.username)
        
        if _user is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

        if not auth_handler.verify_password(data.password, _user.password):
        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )

        if _user.refresh_token is not None and crud.verify_refresh_token(db, _user.refresh_token).count() == 0:        
            crud.create_backlist_token(db, _user.refresh_token)

        #generating new token
        access_token = auth_handler.encode_token(db, data.username)
        refresh_token = auth_handler.create_refresh_token(data.username)
        
        #updating refresh token in user model
        crud.update_refrsh_token(db, _user, refresh_token)
        
        return LoginSchema(
            refresh_token=refresh_token,
            access_token=access_token
        ) 
        
    except Exception as e:

        raise
    

@app.get('/logout', response_model=Response)
def logout(db:Session=Depends(get_db), username=Depends(auth_handler.auth_wrapper)):

    _user = crud.get_user_by_username(db, username)

    if _user:

        crud.create_backlist_token(db, _user.refresh_token)

        return Response(
            code=200,
            status="ok",
            message="logout successfully",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Bad Request"
    )


@app.post('/refresh_token', response_model=LoginSchema)
def refresh_token(data: TokenSchema, db:Session=Depends(get_db)):
    try:
        username = auth_handler.decode_refresh_token(db, data.refresh_token)

        if not username or (crud.get_user_by_username(db, username) is None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
        access_token = auth_handler.encode_token(db, username)

        return LoginSchema(
            access_token=access_token,
            refresh_token=data.refresh_token
        ) 
    
    except Exception as e:
        raise 


app.include_router(router.router, prefix="/department", tags=["department"])
app.include_router(router.user_router, prefix="/user", tags=["user"])

