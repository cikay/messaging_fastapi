
from pyexpat import model
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, query
from sqlalchemy.sql import select

from conversationgroup import schemas, models
from db_setup import get_db

conversationgroup_router = APIRouter(prefix='/conversationgroups')

@conversationgroup_router.post("/create")
async def create(
    schema_conversationgroup: schemas.ConversationGroupCreate,
    db: Session = Depends(get_db)
):
    users_query = db.query(models.User).filter(
        models.User.id.in_(schema_conversationgroup.users)
    ).all()
    model_conversationgroup = models.ConversationGroup()
    model_conversationgroup.name = schema_conversationgroup.name
    model_conversationgroup.users = users_query
    db.add(model_conversationgroup)
    db.commit()
    db.refresh(model_conversationgroup)
    return "Group was created successfully"
