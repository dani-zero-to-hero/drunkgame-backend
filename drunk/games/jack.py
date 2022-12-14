from typing import overload

from ..players import UserAction, UserActionType
from . import Game, Rule, TurnResult
from .devices import DiceResult, PokerDice


class JackResult(TurnResult):
    dice_result: str


def compose_name_rule(
    name: None | str,
    effect: None | str,
    trigger: None | DiceResult,
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


class JackRule(Rule):
    trigger: str | list[str] | None

    def __init__(
        self,
        name: None | str,
        effect: None | str,
        trigger: None | DiceResult,
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
    _dice = PokerDice()
    _rules: list[JackRule]
    _turns: list[JackResult]

    def _play_turn(self) -> JackResult:
        user_input = []
        roll = self._dice.random_roll()
        rules = []
        for rule in self._rules:
            if rule.roll_applies(roll, self._turns):
                rules.append(rule)
                if rule.user_input is not None:
                    user_input.append(rule.user_input)

        return JackResult(
            dice_result=roll,
            applied_rules=rules,
            user_input=user_input,
        )

    def end_reached(self) -> bool:
        return False

    @overload
    def set_rule(self, *, rule: JackRule) -> bool:
        ...

    @overload
    def set_rule(
        self,
        *,
        name: None | str = None,
        effect: None | str = None,
        trigger: None | DiceResult = None,
        user_input: None | UserAction = None,
    ) -> bool:
        ...

    def set_rule(
        self,
        *,
        rule: JackRule = None,
        name: None | str = None,
        effect: None | str = None,
        trigger: None | DiceResult = None,
        user_input: None | UserAction = None,
    ) -> bool:
        if rule is not None:
            self._rules.append(rule)
            return True

        rule = JackRule(name, effect, trigger, user_input)
        self._rules.append(rule)
        return True

    def _default_rules(self) -> None:
        self.set_rule(
            rule=JackRule(
                "Default black rule",
                effect="Player to the right drinks",
                trigger="black",
                user_input=None,
            )
        )
        self.set_rule(
            rule=JackRule(
                "Default red rule",
                effect="Player to the left drinks",
                trigger="red",
                user_input=None,
            )
        )
        self.set_rule(
            rule=JackRule(
                "Default jack rule",
                effect="All jacks drink",
                trigger="j",
                user_input=UserAction(action_type=UserActionType.repeat),
            )
        )
        self.set_rule(
            rule=JackRule(
                "Default king rule",
                effect="Both sides drink",
                trigger="k",
                user_input=None,
            )
        )
        self.set_rule(
            rule=JackRule(
                "Default ace rule",
                effect="Player sets a rule",
                trigger="ace",
                user_input=UserAction(action_type=UserActionType.set_rule),
            )
        )


if __name__ == "__main__":
    jack = Jack()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
    jack.play_turn()
