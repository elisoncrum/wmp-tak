import base64
import requests
from fastapi import FastAPI
from fastapi import Response
from fastapi import Depends
from fastapi.responses import FileResponse

from sqlmodel import Session
from sqlmodel import select

from sqlalchemy import exc

from functools import lru_cache

from app.database import create_db_and_tables, engine
from app.models import tiles
from app import config

from app.routers import worldmap

app = FastAPI()
app.include_router(worldmap.router)

@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def root():
    return {"message": "TAK Map Proxy Cacher"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()