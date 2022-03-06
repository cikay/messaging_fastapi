from dataclasses import make_dataclass
from typing import List

from pydantic import BaseModel

from auth.schemas import User
from utils.pydantic_utils import AllOptional


class ConversationGroupCreate(BaseModel):
    name: str
    users: List[int]

class ConversationGroupUpdate(ConversationGroupCreate, metaclass=AllOptional):
    pass


class MessageCreate(BaseModel):
    content: str
    sender_id: int
    conversationgroup_id: int
