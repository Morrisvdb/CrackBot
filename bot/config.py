import os

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
database_uri = "sqlite:///database.db"
# self.database_uri = f"sqlite:///{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"