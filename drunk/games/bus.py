from random import choice
from typing import overload

from ..players import UserAction
from . import Game, Rule, TurnResult
from .devices import Card, Jocker, PockerDeck


class BusResult(TurnResult):
    card_result: Card


def compose_name_rule(
    name: None | str,
    effect: None | str,
    trigger: None | Card,
):
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


class BusRule(Rule):
    trigger: str | list[str] | None

    def __init__(
        self,
        name: None | str,
        effect: None | str,
        trigger: None | Card,
        user_input: None | UserAction,
    ):
        name = compose_name_rule(name=name, effect=effect, trigger=trigger)
        if effect is None:
            effect = name

        super().__init__(
            name=name,
            effect=effect,
            trigger=trigger,
            user_input=user_input,
        )

    def draw_applies(self, card: Card, turns: list[BusResult]) -> bool:
        if isinstance(self.trigger, str) and card == self.trigger:
            return True
        if isinstance(self.trigger, list) and card == self.trigger[-1]:
            applies = True
            for i in range(1, len(self.trigger)):
                if turns[0 - i].card_result != self.trigger[-1 - i]:
                    applies = False
                    break
            if applies:
                return True
        return False


class Bus(Game):
    _name: str = "bus"
    _deck: list[PockerDeck]
    _rules: list[BusRule]
    _turns: list[BusResult]

    @property
    def current_deck(self) -> PockerDeck:
        return choice([deck for deck in self._deck if deck.cards])

    def _play_turn(self) -> BusResult:
        user_input = []
        card = self.current_deck.random_draw()
        rules = []
        for rule in self._rules:
            if rule.draw_applies(card, self._turns):
                rules.append(rule)
                if rule.user_input is not None:
                    user_input.append(rule.user_input)

        return BusResult(
            card_result=card,
            applied_rules=rules,
            user_input=user_input,
        )

    def end_reached(self) -> bool:
        return False

    @overload
    def set_rule(self, *, rule: BusRule) -> bool:
        ...

    @overload
    def set_rule(
        self,
        *,
        name: None | str = None,
        effect: None | str = None,
        trigger: None | Card = None,
        user_input: None | UserAction = None,
    ) -> bool:
        ...

    def set_rule(
        self,
        *,
        rule: BusRule = None,
        name: None | str = None,
        effect: None | str = None,
        trigger: None | Card = None,
        user_input: None | UserAction = None,
    ) -> bool:
        if rule is not None:
            self._rules.append(rule)
            return True

        rule = BusRule(name, effect, trigger, user_input)
        self._rules.append(rule)
        return True

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
