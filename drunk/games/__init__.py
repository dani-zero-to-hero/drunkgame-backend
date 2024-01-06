"""
This module contains all the games offered in the DrunkGame api
"""
from __future__ import annotations

import abc
from typing import Any, ClassVar, Generic, Type, TypeVar, cast, overload

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic import PrivateAttr

from ..exceptions import DrunkException
from ..players import UserAction, UserActionType
from .devices import Card


class Rule(abc.ABC, BaseModel, Generic["T"]):
    """
    Object that defines a rule that applies to a game. These rule is generic and has to be redefined per game.
    """

    name: str
    effect: str
    user_input: UserAction | None
    trigger: str | list[str] | None | Card

    def __init__(
        self,
        name: None | str,
        effect: None | str,
        trigger: Any,
        user_input: None | UserAction,
    ):
        name = self.compose_name_rule(name=name, effect=effect, trigger=trigger)
        if effect is None:
            effect = name

        super().__init__(
            name=name,
            effect=effect,
            trigger=trigger,
            user_input=user_input,
        )

    @property
    def repeat(self) -> bool:
        """
        Property stating if the rule forces a player repeat of the turn.
        """
        if (
            self.user_input is not None
            and self.user_input.action_type == UserActionType.REPEAT.value
        ):
            return True
        return False

    @abc.abstractmethod
    def applies(self, trigger: Any, turns: list[T]) -> bool:
        ...

    @staticmethod
    def compose_name_rule(
        name: None | str,
        effect: None | str,
        trigger: Any,
    ) -> str:
        """
        Create a name for a rule from the given parameters.
        """
        if name is not None:
            return name
        name = ""
        if trigger is not None:
            name += f"{str(trigger)} "
        if effect is not None:
            name += "and " if name else ""
            name += effect

        if name == "":
            raise AttributeError("Wrong rule, missing attributes")
        return name


class TurnResult(abc.ABC, BaseModel):
    applied_rules: list[Rule]
    user_input: list[UserAction]


T = TypeVar("T", bound=TurnResult)


class Game(BaseModel, abc.ABC):
    """
    Abstract class specifying a game. It contains a name, a set of rules, the list of turns, the current player and the
    total number of players.

    :attr _name: Name of the game
    :attr _rules: Sequence of rules, these include the ones defined by the game itself and the ones defined during the
        game by the players
    :attr _player: Current player
    :attr _players: Total number of players
    """

    name: ClassVar[str]
    _rules: list[Rule] = PrivateAttr(default_factory=list)
    _turns: list[TurnResult] = PrivateAttr(default_factory=list)
    _player: int = PrivateAttr(default=0)
    _players: int = PrivateAttr(default=2)
    _rule_class: ClassVar[Type[Rule]]
    _turn_class: ClassVar[Type[TurnResult]]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._default_rules()

    @abc.abstractmethod
    def _play_turn(self) -> TurnResult:
        ...

    def play_turn(self) -> TurnResult:
        """
        Play a turn of the game. This function is a wrapper around _play_turn which defines the game specific rules and
        actions. After the turn has been played the result is saved in turns and the current player is advanced
        (or not) according to the result.

        :return: The result of the played turn.
        """
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

    def game_state(self) -> dict:
        return {
            "name": self.name,
            "rules": self._rules,
            "ended": self.end_reached,
        }

    @classmethod
    def get_game(cls, name: str) -> Type["Game"]:
        """
        Factory method to return the specific Game subclass with the given name. It raises an exception if no game is
        found with the specified name.

        :param name: Name of the game to be played

        :return: The Class of the game

        :raise: Exception is risen if the given game name doesn't correspond to any of the implemented games.
        """
        if name in GAMES:
            return GAMES[name]
        raise DrunkException("Game does not exist for the moment")

    @abc.abstractmethod
    def _default_rules(self) -> None:
        ...

    @overload
    def set_rule(self, *, rule: Rule) -> bool:
        ...

    @overload
    def set_rule(
        self,
        *,
        name: None | str = None,
        effect: None | str = None,
        trigger: Any = None,
        user_input: None | UserAction = None,
    ) -> bool:
        ...

    def set_rule(
        self,
        *,
        rule: None | Rule = None,
        name: None | str = None,
        effect: None | str = None,
        trigger: Any = None,
        user_input: None | UserAction = None,
    ) -> bool:
        """
        Add a rule to the current game set of rules
        """
        if rule is not None:
            self._rules.append(rule)
            return True

        rule = self._rule_class(name, effect, trigger, user_input)
        self._rules.append(rule)
        return True


GAMES = {game.name: game for game in Game.__subclasses__()}
