import abc
from typing import Any, Type, cast

from pydantic import BaseModel, PrivateAttr

from ..players import UserAction


class Rule(abc.ABC, BaseModel):
    name: str
    effect: str
    user_input: UserAction | None


class TurnResult(abc.ABC, BaseModel):
    applied_rules: list[Rule]
    user_input: list[UserAction]


class Game(BaseModel, abc.ABC):
    _name: str
    _rules: list[Rule] = PrivateAttr(default_factory=list)
    _turns: list[TurnResult] = PrivateAttr(default_factory=list)
    _player: int = PrivateAttr(default=0)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._default_rules()

    @property
    @classmethod
    def game_name(self) -> str:
        return self._name

    @abc.abstractmethod
    def _play_turn(self) -> TurnResult:
        ...

    def play_turn(self) -> TurnResult:
        self._turns.append(self._play_turn())
        return self._turns[-1]

    @property
    @abc.abstractmethod
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

    @abc.abstractmethod
    def _default_rules(self):
        ...


GAMES = {cast(str, game.game_name): game for game in Game.__subclasses__()}
