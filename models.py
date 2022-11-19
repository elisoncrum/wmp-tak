from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# Need the class name to be upper clase but the table lowercase
class tiles(SQLModel, table=True):
    key: int = Field(default=None, primary_key=True)
    tile: bytes

class WMPStats(SQLModel, table = True):
    key: Optional[int] = Field(default = None, primary_key = True)
    total_requests: int
    total_cached_responses: int
    total_err_responses: int