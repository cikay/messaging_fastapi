from typing import List

from pydantic import BaseModel

from auth.schemas import User


class ConversationGroupCreate(BaseModel):
    name: str
    users: List[int]

class MessageCreate(BaseModel):
    content: str
    sender_id: int
    conversationgroup_id: int
