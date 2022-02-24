
from pyexpat import model
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, query
from sqlalchemy.sql import select

from conversationgroup import schemas, models
from auth.models import UserModel
from db_setup import get_db

conversationgroup_router = APIRouter(prefix='/conversationgroups')

@conversationgroup_router.post("/create")
async def create(
    schema_conversationgroup: schemas.ConversationGroupCreate,
    db: Session = Depends(get_db)
):
    users_query = db.query(UserModel).filter(
        UserModel.id.in_(schema_conversationgroup.users)
    ).all()
    model_conversationgroup = models.ConversationGroup()
    model_conversationgroup.name = schema_conversationgroup.name
    model_conversationgroup.users = users_query
    db.add(model_conversationgroup)
    db.commit()
    db.refresh(model_conversationgroup)
    return "Group was created successfully"


@conversationgroup_router.post('/message/create')
async def create_message(message_schema: schemas.MessageCreate, db: Session = Depends(get_db)):
    users_id = db.query(models.ConversationGroup.id).filter(
        models.ConversationGroup.id==message_schema.conversationgroup_id
    ).all()
    users_id = [user_id for user_id, in users_id]
    if message_schema.sender_id not in users_id:
        raise HTTPException(status_code=404, detail="User must be member of group")
    message_model = models.Message(**message_schema.dict())
    db.add(message_model)
    db.commit()
    db.refresh(message_model)
    return "Message was created successfully"
