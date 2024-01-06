"""
This module contains the definition of the game devices, dices and cards for example.
"""
from abc import ABC
from dataclasses import dataclass
from random import randint
from typing import Any

DiceSide = int | list[str]
DiceResult = int | str


class Dice(ABC):
    """
    This object represents a dice. It contains a single property, its sides.
    :param sides: sides of the current dice
    """

    sides: DiceSide

    def random_roll(self) -> DiceResult:
        """
        Produces a random roll of the dice and returns the result.

        :return: Result of a random roll of the dice
        """
        if isinstance(self.sides, int):
            return randint(0, self.sides)
        return self.sides[randint(0, len(self.sides) - 1)]

    def cheat_roll(self, result: DiceResult) -> DiceResult:
        """
        If the result is believable return the given result.

        :param result: Result that wants to be obtained

        :return: The result given as a parameter
        """
        if (
            isinstance(self.sides, int)
            and isinstance(result, int)
            and 0 < result < self.sides
        ):
            return result

        if (
            isinstance(self.sides, str)
            and isinstance(result, str)
            and result in self.sides
        ):
            return result

        raise AttributeError("Given result cannot be used")


class PokerDice(Dice):
    sides = ["black", "red", "j", "q", "k", "ace"]


CardSymbol = int | str


@dataclass
class Card:
    """
    This class represents a single playing card. It has a symbol and a suit. For example:
    The ace of spades is a Card(symbol="ace", suit="spades")
    """

    symbol: CardSymbol
    suit: str | None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.symbol == other.symbol and self.suit == other.suit


Jocker = Card("jocker", None)


class CardDeck(ABC):
    """
    A set of Card objects.
    """

    cards: list[Card]
    discarded: list[Card]

    def __init__(self) -> None:
        self.discarded = []

    def random_draw(self) -> Card:
        """
        Draw a random card from the deck. All cards should have the same chance
        """
        choice = randint(0, len(self.cards))
        temp = self.cards.pop(choice)
        self.discarded.append(temp)
        return temp

    def cheat_draw(self, result: Card) -> Card:
        """
        Draw a card not from the deck. If someone cheats the card is not drawn but added to the deck
        """
        if result in self.cards + self.discarded:
            return result
        raise AttributeError("Given result cannot be used")


class PockerDeck(CardDeck):
    """
    A classic pocker deck, the number of jockers can be altered through the jockers parameter.
    """

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
