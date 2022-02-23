
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Text, Table, String
from sqlalchemy.orm import relationship

from db_setup import Base
from auth.models import User


conversationgroup_user = Table('conversationgroup_user', Base.metadata,
    Column('conversationgroup_id', ForeignKey('conversationgroup.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)


class ConversationGroup(Base):
    __tablename__ = 'conversationgroup'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    users = relationship(User, secondary=conversationgroup_user, uselist=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    conversationgroup_id = Column(Integer, ForeignKey(ConversationGroup.id), nullable=False)
    sender_id = Column(Integer,  ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sender = relationship("User")