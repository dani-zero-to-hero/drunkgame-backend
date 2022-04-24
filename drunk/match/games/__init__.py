import abc
from typing import Optional, Type

from pydantic import BaseModel


class Game(abc.ABC):
    name: str

    @abc.abstractmethod
    def play_turn(self):
        ...

    @abc.abstractmethod
    @property
    def end_reached(self) -> bool:
        """
        Check end game conditions are matched or not and return the result
        """
        ...

    @abc.abstractmethod
    def game_state(self) -> dict:
        ...

    @classmethod
    def get_game(cls, name: str) -> Type["Game"]:
        games = {game.name: game for game in Game.__subclasses__()}
        if name in games:
            return games[name]
        raise Exception


class Rule(BaseModel):
    name: str
    player: Optional[str] = None
    effect: str
