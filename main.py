from fastapi import FastAPI

from db_setup import engine 
from auth.controllers import auth_router
from auth.models import UserModel
from conversationgroup.controllers import conversationgroup_router
from conversationgroup.models import ConversationGroup

all_models = [UserModel, ConversationGroup]

for model in all_models:
    model.metadata.create_all(bind=engine)


app = FastAPI()
all_routers = [auth_router, conversationgroup_router]

for router in all_routers:
    app.include_router(router)