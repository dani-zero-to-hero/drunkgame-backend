from datetime import datetime

from pydantic import BaseModel


class Player(BaseModel):
    id: str
    name: str
    created: datetime
    updated: datetime
    games: list[str]
