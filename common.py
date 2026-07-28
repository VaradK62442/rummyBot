"""
Common constants, functions, configs.
"""

from enum import StrEnum

type Hand = list[Card]
type Set = list[Card]
type Sets = list[list[Card]]

DEBUG = True
STARTING_HAND_SIZE = 7


def dprint(*args):
    if DEBUG:
        print(*args)


class Suit(StrEnum):
    CLUB = "♣"
    DIAMOND = "♦"
    HEART = "♥"
    SPADE = "♠"


class Rank(StrEnum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"


class PlayerAction:
    """
    Represents a player action.

    Attributes:
        value (int): The action value.

    -1: Draw a card.
    i: For i >= 0, take all cards in the field from index i onwards.
    """

    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return "draw" if self.value == -1 else f"take {self.value}"


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}/{self.suit}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank

    def get_value(self):
        match self.rank:
            case Rank.ACE:
                return 1
            case Rank.TWO:
                return 2
            case Rank.THREE:
                return 3
            case Rank.FOUR:
                return 4
            case Rank.FIVE:
                return 5
            case Rank.SIX:
                return 6
            case Rank.SEVEN:
                return 7
            case Rank.EIGHT:
                return 8
            case Rank.NINE:
                return 9
            case Rank.TEN:
                return 10
            case Rank.JACK:
                return 11
            case Rank.QUEEN:
                return 12
            case Rank.KING:
                return 13


DECK = [Card(suit, rank) for suit in Suit for rank in Rank]


def score_set(card_set: list[Card]) -> int:
    return sum(10 if card.get_value() >= 10 else 5 for card in card_set)


def score_sets(sets: Sets) -> int:
    return sum(score_set(card_set) for card_set in sets)
