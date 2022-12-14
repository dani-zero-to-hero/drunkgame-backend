import abc
from typing import Any, Sequence, Type, cast

from pydantic import BaseModel, PrivateAttr

from ..players import UserAction, UserActionType


class Rule(abc.ABC, BaseModel):
    name: str
    effect: str
    user_input: UserAction | None

    @property
    def repeat(self) -> bool:
        if (
            self.user_input is not None
            and self.user_input.action_type == UserActionType.repeat.value
        ):
            return True
        return False


class TurnResult(abc.ABC, BaseModel):
    applied_rules: list[Rule]
    user_input: list[UserAction]


class Game(BaseModel, abc.ABC):
    _name: str
    _rules: Sequence[Rule] = PrivateAttr(default_factory=list)
    _turns: Sequence[TurnResult] = PrivateAttr(default_factory=list)
    _player: int = PrivateAttr(default=0)
    _players: int = PrivateAttr(default=2)

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
        turn = self._play_turn()
        if isinstance(self._turns, list):
            self._turns.append(turn)
        if not any(rule.repeat for rule in turn.applied_rules):
            self._player += 1
            if self._player >= self._players:
                self._player = 0
        print(f"Next player is {self._player}")
        return turn

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
