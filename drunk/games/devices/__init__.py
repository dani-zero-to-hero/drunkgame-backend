from abc import ABC
from dataclasses import dataclass
from random import randint

DiceSide = int | list[str]
DiceResult = int | str


class Dice(ABC):
    sides: DiceSide

    def random_roll(self) -> DiceResult:
        if isinstance(self.sides, int):
            return randint(0, self.sides)
        return self.sides[randint(0, len(self.sides) - 1)]

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


CardSymbol = int | str


@dataclass
class Card:
    symbol: CardSymbol
    suit: str | None

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.symbol == other.symbol and self.suit == other.suit


Jocker = Card("jocker", None)


class CardDeck(ABC):
    cards: list[Card]
    discarded: list[Card]

    def __init__(self) -> None:
        self.discarded = list()

    def random_draw(self) -> Card:
        choice = randint(0, len(self.cards))
        temp = self.cards.pop(choice)
        self.discarded.append(temp)
        return temp

    def weighted_draw(self, weight) -> DiceSide:
        pass

    def cheat_draw(self, result: Card) -> Card:
        if result in self.cards + self.discarded:
            return result
        else:
            raise AttributeError("Given result cannot be used")


class PockerDeck(CardDeck):
    def __init__(self, jockers: int = 2):
        super().__init__()
        cards = []
        for suit in ["diamond", "clubs", "hearts", "spades"]:
            for symbol in [
                "ace",
                *[str(i) for i in range(2, 11)],
                "jack",
                "queen",
                "king",
            ]:
                cards.append(Card(suit=suit, symbol=symbol))
        self.cards = cards
        self.cards.extend([Jocker for i in range(jockers)])
