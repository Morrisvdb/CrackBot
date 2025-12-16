import discord, sqlalchemy, time, os
from discord.ext import commands
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import database_uri, TOKEN

from lingua import Language, LanguageDetectorBuilder
languages = [Language.ENGLISH, Language.FRENCH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

intents = discord.Intents.all()
# If this breaks change back to discord.Bot
bot = commands.Bot(intents=intents, command_prefix="!")

#Download Lavalink automatically (no clue what im doing here)
# if not os.path.exists("./lavalink/Lavalink.jar"):
#     print("Lavalink.jar not found, downloading from repo...")
#     r = requests.get("https://github.com/lavalink-devs/Lavalink/releases/download/4.1.1/Lavalink.jar")
#     with open("./lavalink/LavaLink.jar", "wb") as f:
#         f.write(r.content)
#     print("File downloaded successfully.")

for i in range(5):
    try:
        engine = create_engine(database_uri)
        
        Base = declarative_base()
        Session = sessionmaker(bind=engine)
        db = Session()
        Base.metadata.create_all(engine)
        break
        
    except Exception as e:
        print(f"Failed to connect to database. Retrying in 5 seconds. ({i+1}/5)")
        time.sleep(2)
        
