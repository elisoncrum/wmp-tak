import requests
from sqlmodel import Session
from sqlmodel import select
from fastapi import APIRouter
from fastapi import Response
from app import config
from app.models import tiles
from app.database import engine
from sqlalchemy import exc

router = APIRouter()

"""
@route.get("/maps")

@router.get("/maps/json")

@router.get("/map/{map:str}/xml")

@router.get("/map/{map:str}/database")

@router.get("/map/{map:str}/{q:path}")

@router.get("/map/{map:str}/{z:str}/{x:str}/{y:str}")
"""

@router.get("/maps")
def get_maps():
    pass

@router.get("/maps/json")
def get_maps_json():
    pass

@router.get("/map/{map_name:str}/xml")
def get_map_xml(map_name: str):
    pass

@router.get("/map/{map_name:str}/database")
def get_map_database(map_name: str):
    pass

@router.get("/map/{z:str}/{x:str}/{y:str}")
def tile_xyz(x: str, y: str, z: str):
    with Session(engine) as session:
        # Converts /{y}.png -> y
        y = y.split(".")[0]
        try:
            key = int(f"{z}{x}{y}")
        except ValueError:
            return {"error": "Falformed Request."}

        statement = select(tiles).where(tiles.key == key)
        results = session.exec(statement)

        try:
            tile = results.one()
            return Response(
                content = tile.tile,
                media_type = "image/jpeg"
            )
        except exc.NoResultFound:
            try:
                req = requests.get(f"http://wms.chartbundle.com/tms/v1.0/wacgrids/{z}/{x}/{y}.png", verify = False)
                if req.status_code == 200:
                    _map = tiles(
                        key = key,
                        tile = req.content
                    )
                    session.add(_map)
                    session.commit()
                    return Response(
                        content = req.content,
                        media_type = "image/png", 
                    )

            except requests.exceptions.ConnectionError as e:
                return {"error": str(e)}, 400

@router.get("/map/{q:path}")
def tile_q(q: str):
    with Session(engine) as session:
        # Q: For some reason WinTAK places tiles
        # dependent on the name of the file in response
        # when the response wasnt r{q}.png it would
        # place the tiles randomly.

        # Converts /r{q}.png -> q
        q = q.split(".")[0][1:]

        try: 
            q = int(q)
        except ValueError: 
            return {"error": "Falformed Request."}

        statement = select(tiles).where(tiles.key == q)
        results = session.exec(statement)
        try:
            tile = results.one()
            return Response(
                content = tile.tile,
                media_type = "image/png", 
            )
        except exc.NoResultFound:
            try:
                # TODO: Better request function. Or Map property function.
                req = requests.get(f"http://r0.ortho.tiles.virtualearth.net/tiles/r{q}.png?g=45", verify = False)

                # Possibly keep re-trying?
                if req.status_code == 200:
                    _map = tiles(
                        key = q,
                        tile = req.content
                    )
                    session.add(_map)
                    session.commit()
                    return Response(
                        content = req.content,
                        media_type = "image/png", 
                    )
            except requests.exceptions.ConnectionError as e:
                return {"error": str(e)}, 400