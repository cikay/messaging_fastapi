import jwt
from datetime import datetime, timedelta

from fastapi.security import HTTPBasicCredentials
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from auth import schemas, models
from auth.models import UserModel
from db_setup import get_db

auth_router = APIRouter(prefix='/users')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@auth_router.post("/create")
async def create(schema_user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = generate_hash_password(schema_user.password)
    model_user = UserModel(
        firstname=schema_user.firstname,
        lastname=schema_user.lastname,
        username=schema_user.username,
        password=hashed_password
    )
    db.add(model_user)
    db.commit()
    db.refresh(model_user)
    return {
        'username': model_user.username,
        'firstname': model_user.firstname,
        'lastname': model_user.lastname,
        'id': model_user.id
    }


@auth_router.post("/login")
def login(credentials: HTTPBasicCredentials, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        UserModel.username == credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}


def generate_hash_password(plain_password):
    return pwd_context.hash(plain_password)




def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

