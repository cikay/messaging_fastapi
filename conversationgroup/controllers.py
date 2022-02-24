
from ntpath import join
from pyexpat import model
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, query
from sqlalchemy.sql import select

from conversationgroup import schemas, models
from auth.models import UserModel
from auth.utils import get_current_user
from conversationgroup.models import conversationgroup_user
from db_setup import get_db

conversationgroup_router = APIRouter(prefix='/conversationgroups')

@conversationgroup_router.post("/create/")
async def create(
    schema_conversationgroup: schemas.ConversationGroupCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
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
    return model_conversationgroup


@conversationgroup_router.post('/message/create/')
async def create_message(
    message_schema: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    c_group = db.query(models.ConversationGroup).where(
        models.ConversationGroup.id==message_schema.conversationgroup_id
    ).first()

    users_id = [user.id for user in c_group.users]
    if message_schema.sender_id not in users_id:
        raise HTTPException(status_code=404, detail="User must be member of group")
    message_model = models.Message(**message_schema.dict())
    db.add(message_model)
    db.commit()
    db.refresh(message_model)
    return message_model


@conversationgroup_router.get('/messages/')
async def get_messages(
    conversationgroup_id: int,
    db: Session=Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    c_groups = db.query(models.ConversationGroup.id).filter(
        models.ConversationGroup.id==conversationgroup_id
    )
    c_groups_id = [c_group_id for c_group_id, in c_groups]
    return db.query(models.Message).filter(
        models.Message.conversationgroup_id.in_(c_groups_id)
    ).all()
