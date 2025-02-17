import discord, sqlalchemy, time, os
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from config import database_uri

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

for i in range(5):
    try:
        engine = create_engine(database_uri)
        # engine = create_engine('sqlite:///database.db')
        Base = declarative_base()
        Session = sessionmaker(bind=engine)
        db = Session()
        break
        
    except Exception as e:
        print(f"Failed to connect to database. Retrying in 5 seconds. ({i+1}/5)")
        time.sleep(2)
        
