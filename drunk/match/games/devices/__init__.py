from random import randint
from typing import Optional, Union

from pydantic import BaseModel

DiceSide = Union[int, list[str]]
DiceResult = Union[int, str]


class Dice(BaseModel):
    sides: DiceSide

    def random_roll(self) -> DiceResult:
        if isinstance(self.sides, int):
            return randint(0, self.sides)
        return self.sides[randint(0, len(self.sides))]

    def weighted_roll(self, weight) -> DiceResult:
        pass

    def cheat_roll(self, result: DiceResult) -> DiceResult:
        if (
            isinstance(self.sides, int)
            and isinstance(result, int)
            and 0 < result < self.sides
        ):
            return result
        elif (
            isinstance(self.sides, str)
            and isinstance(result, str)
            and result in self.sides
        ):
            return result
        else:
            raise AttributeError("Given result cannot be used")


class PokerDice(Dice):
    sides = ["black", "red", "j", "q", "k", "ace"]


CardSymbol = Union[int, str]


class Card:
    symbol: CardSymbol
    suit: Optional[str]


class Jocker(Card):
    symbol = "jocker"
    suit = None


class CardDeck(BaseModel):
    cards: list[Card]
    jockers: int

    def random_draw(self) -> Card:
        choice = randint(0, len(self.cards) + self.jockers)
        if choice > len(self.cards):
            return Jocker()
        return self.cards[choice]

    def weighted_draw(self, weight) -> DiceSide:
        pass

    def cheat_draw(self, result: Card) -> Card:
        if result in self.cards:
            return result
        elif isinstance(result, Jocker) and self.jockers > 0:
            return result
        else:
            raise AttributeError("Given result cannot be used")
