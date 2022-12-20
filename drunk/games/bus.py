"""
This module contains all the code necessary to play a match of bus driver
"""
from random import choice
from typing import Any

from . import Game, Rule, TurnResult
from .devices import Card, Jocker, PockerDeck


class BusResult(TurnResult):
    card_result: Card


class BusRule(Rule):
    """
    A rule that applies to the bus game
    """

    def applies(self, trigger: Any, turns: list[BusResult]) -> bool:
        if isinstance(self.trigger, str) and trigger == self.trigger:
            return True
        if isinstance(self.trigger, list) and trigger == self.trigger[-1]:
            applies = True
            for i in range(1, len(self.trigger)):
                if turns[0 - i].card_result != self.trigger[-1 - i]:
                    applies = False
                    break
            if applies:
                return True
        return False


class Bus(Game):
    """
    This class contains all the logic to play the Bus driver
    """

    _name: str = "bus"
    _deck: list[PockerDeck]

    @property
    def current_deck(self) -> PockerDeck:
        return choice([deck for deck in self._deck if deck.cards])

    def _play_turn(self) -> BusResult:
        user_input = []
        card = self.current_deck.random_draw()
        rules = []
        for rule in self._rules:
            if rule.applies(card, self._turns):
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
        return False

    def _default_rules(self) -> None:
        self.set_rule(
            rule=BusRule(
                "Drink shot",
                effect="Drink",
                trigger=Jocker,
                user_input=None,
            )
        )


if __name__ == "__main__":
    bus = Bus()
