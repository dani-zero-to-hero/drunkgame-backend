from . import Game, Rule


class Jack(Game):
    _name: str = "jack"

    def play_turn(self):
        pass

    def end_reached(self) -> bool:
        return False

    def _set_rule(self, rule: Rule) -> bool:
        if not hasattr(self, "_rules"):
            self._rules = []
        self._rules.append(rule)
        return True

    def game_state(self) -> dict:
        return {
            "name": self._name,
            "rules": self.__getattribute__("_rules"),
            "ended": self.end_reached(),
        }
