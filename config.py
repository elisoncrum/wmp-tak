from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL = "sqlite:///database.sqlite"
