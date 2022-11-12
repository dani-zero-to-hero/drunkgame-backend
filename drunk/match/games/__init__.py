import abc
from typing import Type, cast

from pydantic import BaseModel


class Rule(abc.ABC, BaseModel):
    name: str
    effect: str
    repeat: bool
    user_input: bool


class TurnResult(abc.ABC, BaseModel):
    applied_rules: list[Rule]
    user_input: bool
    repeat: bool


class Game(abc.ABC, BaseModel):
    _name: str
    _rules: list[Rule]
    _turns: list[TurnResult]

    @property
    @classmethod
    def game_name(self) -> str:
        return self._name

    @property
    def rules(self) -> str:
        return self.rules

    @abc.abstractmethod
    def _play_turn(self) -> TurnResult:
        ...

    def play_turn(self) -> TurnResult:
        self._turns.append(self._play_turn())
        return self._turns[-1]

    @abc.abstractmethod
    @property
    def end_reached(self) -> bool:
        """
        Check end game conditions are matched or not and return the result
        """
        ...

    def game_state(self) -> dict:
        return {
            "name": self._name,
            "rules": self._rules,
            "ended": self.end_reached,
        }

    @classmethod
    def get_game(cls, name: str) -> Type["Game"]:
        if name in GAMES:
            return GAMES[name]
        raise Exception("Game does not exist for the moment")


GAMES = {cast(str, game.game_name): game for game in Game.__subclasses__()}
