from typing import Optional, Union, cast, overload

from . import Game, Rule, TurnResult
from .devices import DiceResult, PokerDice


class JackResult(TurnResult):
    dice_result: str


def compose_name_rule(
    name: Optional[str],
    effect: Optional[str],
    trigger: Optional[DiceResult],
    repeat: bool,
):
    if name is not None:
        return name
    name = ""
    if trigger is not None:
        name += f"{str(trigger)} "
    if repeat is not None:
        name += "rolls again "
    if effect is not None:
        name += "and " if name else ""
        name += effect

    if name == "":
        raise AttributeError("Wrong rule, missing attributes")
    return name


class JackRule(Rule):
    trigger: Union[str, list[str], None]

    def __init__(
        self,
        name: Optional[str],
        effect: Optional[str],
        trigger: Optional[
            DiceResult,
        ],
        repeat: bool,
        user_input: bool,
    ):
        name = compose_name_rule(
            name=name, effect=effect, trigger=trigger, repeat=repeat
        )
        if effect is None:
            effect = name

        super().__init__(
            name=name,
            effect=effect,
            trigger=trigger,
            repeat_throw=repeat,
            user_input=user_input,
        )

    def roll_applies(self, roll: DiceResult, turns: list[JackResult]) -> bool:
        if isinstance(self.trigger, str) and roll == self.trigger:
            return True
        if isinstance(self.trigger, list) and roll == self.trigger[-1]:
            applies = True
            for i in range(1, len(self.trigger)):
                if turns[0 - i].dice_result != self.trigger[-1 - i]:
                    applies = False
                    break
            if applies:
                return True
        return False


class Jack(Game):
    _name: str = "jack"
    _dice: PokerDice

    def play_turn(self) -> JackResult:
        repeat = False
        user_input = False
        if (roll := self._dice.random_roll()) == "jack":
            repeat = True
        elif roll == "ace":
            user_input = True
        rules = []
        for rule in self._rules:
            if cast(JackRule, rule).roll_applies(
                roll, cast(list[JackResult], self._turns)
            ):
                rules.append(rule)
                if rule.repeat:
                    repeat = True
                if rule.user_input:
                    user_input = True

        return JackResult(
            dice_result=roll,
            applied_rules=roll,
            repeat=repeat,
            user_input=user_input,
        )

    def end_reached(self) -> bool:
        return False

    @overload
    def set_rule(self, *, rule: JackRule) -> bool:
        pass

    @overload
    def set_rule(
        self,
        *,
        name: Optional[str] = None,
        effect: Optional[str] = None,
        trigger: Optional[DiceResult] = None,
        repeat: bool = False,
        user_input: bool = False,
    ) -> bool:
        pass

    def set_rule(
        self,
        rule: JackRule = None,
        name: Optional[str] = None,
        effect: Optional[str] = None,
        trigger: Optional[DiceResult] = None,
        repeat: bool = False,
        user_input: bool = False,
    ) -> bool:
        if rule is not None:
            self._rules.append(rule)
            return True

        rule = JackRule(name, effect, trigger, repeat, user_input)
        self._rules.append(rule)
        return True
