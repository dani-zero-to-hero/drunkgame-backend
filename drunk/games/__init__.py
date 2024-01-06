"""
This module contains all the games offered in the DrunkGame api
"""
from __future__ import annotations

import abc
from typing import Any, ClassVar, Generic, Type, TypeVar, overload

from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
    Field,
    PrivateAttr,
)

from ..exceptions import DrunkException
from ..players import UserAction, UserActionType
from .devices import Card, DiceResult


class Rule(abc.ABC, BaseModel):
    """
    Object that defines a rule that applies to a game. This rule is generic and has to be redefined per game.
    - name: identifiable name for the rule
    - effect: result of this rule being activated
    - user_input: An action the user has to take when this rule is activated. It is a specific kind of effect
    - trigger: The action or turn result that activates the specific rule
    """

    name: str
    effect: str
    user_input: UserAction | None
    trigger: DiceResult | Card | list[str] | list[int] | list[Card] | None

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
            and self.user_input.action_type == UserActionType.DONT_REPEAT.value
        ):
            return True
        return False

    @abc.abstractmethod
    def applies(self, trigger: Any, turns: Any) -> bool:
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


class Game(BaseModel, abc.ABC, Generic[T]):
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
    rules: list[Rule] = Field(default_factory=list)
    turns: list[T] = Field(default_factory=list)
    player: int = Field(default=0)
    _players: int = PrivateAttr(
        default=2
    )  # TODO: rethink the connection between players and game
    _rule_class: ClassVar[Type[Rule]]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._default_rules()

    @abc.abstractmethod
    def _play_turn(self) -> T:
        ...

    def play_turn(self) -> T:
        """
        Play a turn of the game. This function is a wrapper around _play_turn which defines the game specific rules and
        actions. After the turn has been played the result is saved in turns and the current player is advanced
        (or not) according to the result.

        :return: The result of the played turn.
        """
        turn = self._play_turn()
        if isinstance(self.turns, list):
            self.turns.append(turn)
        if not any(rule.repeat for rule in turn.applied_rules):
            self.player += 1
            if self.player >= self._players:
                self.player = 0
        print(f"Next player is {self.player}")
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
            "rules": self.rules,
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
        if rule is not None and isinstance(rule, self._rule_class):
            self.rules.append(rule)  # pylint: disable=no-member
            return True

        rule = self._rule_class(name, effect, trigger, user_input)
        self.rules.append(rule)  # pylint: disable=no-member
        return True


GAMES = {game.name: game for game in Game.__subclasses__()}
