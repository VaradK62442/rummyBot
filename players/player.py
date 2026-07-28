"""
Player abstract class
"""

from abc import ABC, abstractmethod

from common import Card, Field, Hand, PlayerAction, Sets, score_set, score_sets


class AbstractPlayer(ABC):
    def __init__(self, name: str):
        self.name = name
        self.hand: Hand = set()
        self.sets: Sets = set()

    def __str__(self) -> str:
        return f"{self.name}: [{', '.join(str(card) for card in self.hand)}]"

    def __eq__(self, other) -> bool:
        if not isinstance(other, AbstractPlayer):
            return False
        return self.name == other.name

    def score(self) -> int:
        return score_sets(self.sets) - score_set(self.hand)

    def add_card(self, card: Card):
        self.hand.add(card)

    def remove_card(self, card: Card):
        assert card in self.hand
        self.hand.remove(card)

    @abstractmethod
    def decide_action(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> PlayerAction:
        raise NotImplementedError

    @abstractmethod
    def choose_discard(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> Card:
        """
        Note, does not actually discard the card from player's hand.
        This is the game class' responsibility.
        Returned card must be in player's hand.
        """
        raise NotImplementedError
