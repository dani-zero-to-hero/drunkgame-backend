"""
This module contains all the code necessary to play a match of bus driver
"""
from random import choice
from typing import Any

from ..exceptions import InvalidDraw
from . import Game, Rule, TurnResult
from .devices import Card, Jocker, PockerDeck


class BusResult(TurnResult):
    card_result: Card


class BusRule(Rule):
    """
    A rule that applies to the bus game
    """

    def applies(self, trigger: Any, turns: list[BusResult]) -> bool:
        return False


class Bus(Game):
    """
    This class contains all the logic to play the Bus driver
    """

    name = "bus"
    _deck: list[PockerDeck]

    @property
    def current_deck(self) -> PockerDeck:
        return choice([deck for deck in self._deck if deck.available])  # nosec

    def _play_turn(self) -> BusResult:
        user_input = []
        card = self.current_deck.random_draw("deal")
        if card is None:
            raise InvalidDraw("Card is not valid")
        rules = []
        for rule in self.rules:
            if rule.applies(card, self.turns):
                rules.append(rule)
                if rule.user_input is not None:
                    user_input.append(rule.user_input)

        return BusResult(
            card_result=card,
            applied_rules=rules,
            user_input=user_input,
        )

    @property
    def end_reached(self) -> bool:
        return NotImplemented

    def _default_rules(self) -> None:
        self.set_rule(
            rule=BusRule(
                name="Drink shot",
                effect="Drink",
                trigger=Jocker,
                user_input=None,
            )
        )


if __name__ == "__main__":  # pragma: no cover
    bus = Bus(_deck=[PockerDeck()])
