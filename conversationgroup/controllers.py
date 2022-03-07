
from ntpath import join
from pyexpat import model
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, query
from sqlalchemy.sql import select

from conversationgroup import schemas, models
from conversationgroup.schemas import ConversationGroupUpdate
from auth.models import UserModel
from auth.utils import get_current_user
from conversationgroup.models import conversationgroup_user
from conversationgroup.utils import get_single_field
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


@conversationgroup_router.patch("/update/{item_id}")
async def update_partially(
    item_id: int,
    schema_conversationgroup: ConversationGroupUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    partial_update = schema_conversationgroup.dict(exclude_unset=True)
    model_instance = db.query(models.ConversationGroup).filter(
        models.ConversationGroup.id == item_id
    ).first()
    model_instance.__dict__.update(partial_update)
    db.commit()
    db.refresh(model_instance)
    return model_instance


@conversationgroup_router.get('/messages/')
async def get_messages(
    conversationgroup_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    c_groups_id = get_single_field(
        db, models.ConversationGroup.id, conversationgroup_id)
    return db.query(models.Message).filter(
        models.Message.conversationgroup_id.in_(c_groups_id)
    ).all()
