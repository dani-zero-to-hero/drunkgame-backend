"""
This module contains the definition of the game devices, dices and cards for example.
"""
from abc import ABC
from dataclasses import dataclass
from random import randint
from typing import Any, Literal

from ...exceptions import InvalidDraw, UserError

DiceResult = int | str


class Dice(ABC):
    """
    This object represents a dice. It contains a single property, its sides.
    :param sides: sides of the current dice
    """

    sides: int | list[str]

    def random_roll(self) -> DiceResult:
        """
        Produces a random roll of the dice and returns the result.

        :return: Result of a random roll of the dice
        """
        if isinstance(self.sides, int):
            return randint(0, self.sides)  # nosec
        return self.sides[randint(0, len(self.sides) - 1)]  # nosec

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
            isinstance(self.sides, list)
            and isinstance(self.sides[0], str)
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


@dataclass
class CardDeck(ABC):
    """
    A set of Card objects. This represents the deck of cards many games are played with.
    - cards
    """

    available: list[Card]
    discarded: list[Card]
    delt: list[Card]

    def __init__(
        self,
        available: list[Card] | None = None,
        discarded: list[Card] | None = None,
        delt: list[Card] | None = None,
    ) -> None:
        self.available = available if available else []
        self.discarded = discarded if discarded else []
        self.delt = delt if delt else []

    def random_draw(self, action: Literal["deal", "discard"]) -> Card | None:
        """
        Draw a random card from the deck. All cards should have the same chance
        """
        if not self.available:
            return None
        choice = randint(0, len(self.available))  # nosec
        temp = self.available.pop(choice)
        if action == "discard":
            self.discarded.append(temp)
        elif action == "deal":
            self.delt.append(temp)
        else:
            raise UserError("Action not allowed, either deal or discard the card")
        return temp

    def cheat_draw(self, result: Card) -> Card | None:
        """
        Draw a card not from the deck. If someone cheats the card is not drawn but added to the deck
        """
        if not self.available and not self.discarded:
            return None
        if result in self.available + self.discarded:
            return result
        if result in self.delt:
            raise InvalidDraw("Card was drawn by a player")
        raise InvalidDraw("Drawn card is not valid")


class PockerDeck(CardDeck):
    """
    A classic pocker deck, the number of jockers can be altered through the jockers parameter.
    """

    def __init__(
        self,
        available: list[Card] | None = None,
        discarded: list[Card] | None = None,
        delt: list[Card] | None = None,
        jockers: int = 2,
    ):
        super().__init__(available=available, discarded=discarded, delt=delt)
        if available is not None or discarded is not None or delt is not None:
            return
        cards = []
        for suit in ["diamonds", "clubs", "hearts", "spades"]:
            for symbol in [
                "ace",
                *[str(i) for i in range(2, 11)],
                "jack",
                "queen",
                "king",
            ]:
                cards.append(Card(suit=suit, symbol=symbol))
        self.available = cards
        self.available.extend([Jocker for i in range(jockers)])


class SpanishDeck(CardDeck):
    """
    A classic spanish deck.
    """

    def __init__(
        self,
        available: list[Card] | None = None,
        discarded: list[Card] | None = None,
        delt: list[Card] | None = None,
    ):
        super().__init__(available=available, discarded=discarded, delt=delt)
        if available is not None or discarded is not None or delt is not None:
            return
        cards = []
        for suit in ["swords", "golds", "cups", "clubs"]:
            for symbol in [
                *[str(i) for i in range(1, 10)],
                "jack",
                "knight",
                "king",
            ]:
                cards.append(Card(suit=suit, symbol=symbol))
        self.available = cards
