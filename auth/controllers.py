import bcrypt
import jwt
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from auth import schemas, models
from auth.models import UserModel
from db_setup import get_db

auth_router = APIRouter(prefix='/users')


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
    return "Created successfully"


@auth_router.post("/login")
def login(credentials: HTTPBasicCredentials, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(
        UserModel.username == credentials.username
    ).first()

    if not (user or bcrypt.checkpw(credentials.password, user.password)):
        raise HTTPException(status_code=404, detail="Credentials are not correct")

    token = generate_jwt_token(user)
    return {
        "username": user.username,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "token": token
    }


def generate_hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def generate_jwt_token(user: UserModel):
    payload = {
        "username": user.username,
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload=payload, key="secret", algorithm="HS256")

