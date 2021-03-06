
from datetime import datetime

from sqlalchemy import Column, Integer, String, null
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import relationship

from db_setup import Base
from conversationgroup.models import conversationgroup_user


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(80), nullable=False)
    firstname = Column(String(20), nullable=False)
    lastname = Column(String(20), nullable=False)
    username = Column(String(30), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    conversationgroups = relationship(
        "ConversationGroup",
        secondary=lambda: conversationgroup_user,
        backref="conversationgroups"
    )
