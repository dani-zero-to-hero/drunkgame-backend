"""
This module contains all the code necessary to play a match of jack
"""
from ..players import UserAction, UserActionType
from . import Game, Rule, TurnResult
from .devices import DiceResult, PokerDice


class JackResult(TurnResult):
    dice_result: DiceResult


class JackRule(Rule):
    """
    A rule that's specific to the Jack game
    """

    def applies(self, trigger: DiceResult, turns: list[JackResult]) -> bool:
        if isinstance(self.trigger, str) and trigger == self.trigger:
            return True
        if isinstance(self.trigger, list) and trigger == self.trigger[-1] and turns:
            applies = True
            for index, iter_trigger in enumerate(self.trigger[1::-1]):
                if index > len(turns):
                    break
                if turns[0 - index].dice_result != iter_trigger:
                    applies = False
                    break
            if applies:
                return True
        return False


class Jack(Game):
    """
    This class contains all the logic to play the Jack game
    """

    name = "jack"
    _dice = PokerDice()
    _rule_class = JackRule

    def _play_turn(self) -> JackResult:
        user_input = []
        roll = self._dice.cheat_roll("j")
        rules = []
        for rule in self.rules:
            if rule.applies(roll, self.turns):
                rules.append(rule)
                if rule.user_input is not None:
                    user_input.append(rule.user_input)

        return JackResult(
            dice_result=roll,
            applied_rules=rules,
            user_input=user_input,
        )

    @property
    def end_reached(self) -> bool:
        return False

    def _default_rules(self) -> None:
        self.set_rule(
            rule=JackRule(
                name="Default black rule",
                effect="Player to the right drinks",
                trigger="black",
                user_input=None,
            )
        )
        self.set_rule(
            rule=JackRule(
                name="Default red rule",
                effect="Player to the left drinks",
                trigger="red",
                user_input=None,
            )
        )
        self.set_rule(
            rule=JackRule(
                name="Default jack rule",
                effect="All jacks drink",
                trigger="j",
                user_input=UserAction(action_type=UserActionType.REPEAT),
            )
        )
        self.set_rule(
            rule=JackRule(
                name="Default king rule",
                effect="Both sides drink",
                trigger="k",
                user_input=None,
            )
        )
        self.set_rule(
            rule=JackRule(
                name="Default ace rule",
                effect="Player sets a rule",
                trigger="ace",
                user_input=UserAction(action_type=UserActionType.SET_RULE),
            )
        )
        self.set_rule(
            rule=JackRule(
                name="Default triple jack drinks shot",
                effect="Player drinks",
                trigger=["j", "j", "j"],
                user_input=UserAction(
                    action_type=UserActionType.DONT_REPEAT, drink_amount=10
                ),
            )
        )


if __name__ == "__main__":
    jack = Jack()
    for _ in range(20):
        print(jack.play_turn().dice_result)
