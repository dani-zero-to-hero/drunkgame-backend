from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Player(BaseModel):
    id: str
    name: str
    created: datetime
    updated: datetime
    games: list[str]


class UserActionType(Enum):
    set_rule = "set_rule"
    send_drink = "send_drink"
    repeat_throw = "repeat_throw"


class UserAction(BaseModel):
    action_type: UserActionType
    player: None | int | Player

    class Config:
        use_enum_values = True
