from __init__ import db, Base, engine
from sqlalchemy import Column, Integer, String

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)
    user_id = Column(Integer)
    content = Column(String)
    

Base.metadata.create_all(engine)