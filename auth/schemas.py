from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str

