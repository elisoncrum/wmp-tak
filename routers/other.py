import requests
from sqlmodel import Session
from sqlmodel import select
from fastapi import APIRouter
from fastapi import Response
from app import config
from app.models import WMPStats
from app.database import engine
from sqlalchemy import exc

router = APIRouter()

@router.get("/stats")
def get_stats():
    statement = select(WMPStats)
    results = session.exec(statement)

    stats = {
        "Total Requests": 0,
        "Total Requests Cached": 0,
        "Total Size Saved": 0,
        "Proxy Effeciency": 0
    }