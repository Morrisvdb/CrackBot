from __init__ import db, Base, engine
from sqlalchemy import Column, Integer, String
import discord, json, os

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    user_id = Column(Integer)
    content = Column(String)
    

class MessageArchive(Base):
    __tablename__ = 'messages_archive'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, unique=True)
    guild_id = Column(Integer)
    channel_id = Column(Integer)
    timestamp = Column(Integer)
    user = Column(String)
    content = Column(String)
    
    
    def save(message_id, guild_id, channel_id, timestamp, user, content, message_obj = None):
        if db.query(MessageArchive).filter(MessageArchive.message_id == message_id).first():
            return
        new_message = MessageArchive(message_id=message_id, guild_id=guild_id, channel_id=channel_id, timestamp=timestamp, user=user, content=content)
        db.add(new_message)
        db.commit()


Base.metadata.create_all(engine)