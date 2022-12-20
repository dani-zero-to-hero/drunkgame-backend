"""
This module contains all the code relating to players
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Player(BaseModel):
    """
    This class represents a player
    """

    id: str
    name: str
    created: datetime
    updated: datetime
    games: list[str]


class UserActionType(Enum):
    """
    This class enumerates the kinds of actions a player might need to act upon
    """

    SET_RULE = "set_rule"
    SEND_DRINK = "send_drink"
    REPEAT = "repeat"
    DRINK = "drink"


class UserAction(BaseModel):
    """
    This class models an action a player must perform
    """

    action_type: UserActionType
    player: None | int | Player = None
    drink_amount: None | int = None

    class Config:
        use_enum_values = True
