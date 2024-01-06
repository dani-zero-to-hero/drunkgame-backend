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
        if isinstance(self.trigger, list) and trigger == self.trigger[-1]:
            applies = True
            for i in range(1, len(self.trigger)):
                if turns[0 - i].dice_result != self.trigger[-1 - i]:
                    applies = False
                    break
            if applies:
                return True
        return False


class Jack(Game):
    """
    This class contains all the logic to play the Jack game
    """

    _name: str = "jack"
    _dice = PokerDice()
    _rule_class = JackRule
    _turn_class = JackResult

    def _play_turn(self) -> JackResult:
        user_input = []
        roll = self._dice.random_roll()
        rules = []
        for rule in self._rules:
            if rule.applies(roll, self._turns):
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
