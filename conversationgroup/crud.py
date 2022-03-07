from fastapi import HTTPException

from conversationgroup import models, schemas


def create_message(db, message_schema: schemas.MessageCreate):
    c_group = db.query(models.ConversationGroup).where(
        models.ConversationGroup.id == message_schema.conversationgroup_id
    ).first()

    users_id = [user.id for user in c_group.users]
    if message_schema.sender_id not in users_id:
        raise HTTPException(
            status_code=404,
            detail="User must be member of group")
    message_model = models.Message(**message_schema.dict())
    db.add(message_model)
    db.commit()
    db.refresh(message_model)
    return message_model
