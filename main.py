from fastapi import FastAPI

from db_setup import engine 
from auth.controllers import auth_router
from auth.models import User


all_models = [User]

for model in all_models:
    model.metadata.create_all(bind=engine)


app = FastAPI()
all_routers = [auth_router]

for router in all_routers:
    app.include_router(router)