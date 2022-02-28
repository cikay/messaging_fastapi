from fastapi import FastAPI, APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from db_setup import engine 
from auth.controllers import auth_router
from auth.models import UserModel
from conversationgroup.controllers import conversationgroup_router
from conversationgroup.models import ConversationGroup
from websocket.html import HTML_AS_STRING

from conversationgroup import schemas
from auth.utils import get_current_user
from conversationgroup.crud import create_message
from db_setup import get_db
from websocket.connectionManager import ConnectionManager

all_models = [UserModel, ConversationGroup]

for model in all_models:
    model.metadata.create_all(bind=engine)


app = FastAPI()
all_routers = [auth_router, conversationgroup_router]

for router in all_routers:
    app.include_router(router)

websocket_router = APIRouter()
manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(HTML_AS_STRING)


@app.websocket("/ws/{conversationgroup_id}")
async def send_message(
    conversationgroup_id: int,
    websocket: WebSocket,
):
    await manager.connect(websocket)
    try:
        while True:
            content = await websocket.receive_text()
            await manager.broadcast(content, websocket)
    except:
        await websocket.close("User left")
