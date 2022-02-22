import bcrypt

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import schemas, models
from db_setup import get_db

auth_router = APIRouter(prefix='/users')


@auth_router.post("/create")
async def create(schema_user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = generate_hash_password(schema_user.password)
    model_user = models.User(
        firstname=schema_user.firstname,
        lastname=schema_user.lastname,
        username=schema_user.username,
        password=hashed_password
    )
    db.add(model_user)
    db.commit()
    db.refresh(model_user)
    return "Created successfully"


def generate_hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt( 12 ))
