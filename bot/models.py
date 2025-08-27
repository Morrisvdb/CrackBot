from __init__ import db, Base, engine
from sqlalchemy import Column, Integer, String, JSON, Boolean, func
import discord


import sqlalchemy.types as types
class MessageType(types.UserDefinedType):
    cache_ok = True
    
    def __init__(self, messageData: discord.Message):
        self.messageData = messageData
        
    def get_col_spec(self, **kw):
        return "MessageType(%s)" % self.messageData

    def bind_processor(self, dialect):
        def process(value):
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value

        return process


# messages = (
        #     db.query(Message)
        #     .filter(func.json_extract(Message.json_content, '$.author.id') == str(user.id))
        #     .order_by(Message.id.desc())
        #     .limit(count)
        #     .all()
        # )

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    json_content = Column(JSON)
    deleted = Column(Boolean)

    @staticmethod
    def from_discord_message(msg: discord.Message):
        m = db.query(Message).filter(func.json_extract(Message.json_content, '$.id') == str(msg.id)).first()
        if m is not None:
            # Message already recorded
            return m
        return Message(
            json_content={
                "id": msg.id,
                "author": {
                    "id": msg.author.id,
                    "name": msg.author.name,
                    "discriminator": msg.author.discriminator,
                },
                "content": msg.content,
                "channel_id": msg.channel.id,
                "guild_id": msg.guild.id if msg.guild else None,
                "created_at": msg.created_at.isoformat(),
                "poll": msg.poll,
                # Add more fields as needed
            }
        )
    

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

class ServerConfig(Base):
    __tablename__ = 'server_config'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, unique=True)
    key = Column(String)
    value = Column(String)

class TrackedChannels(Base):
    __tablename__ = 'tracked_channels'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    channel_id = Column(Integer)
    target_channel_id = Column(Integer)
    


Base.metadata.create_all(engine)