"""
Player abstract class
"""

from abc import ABC, abstractmethod

from common import Card, Field, Hand, PlayerAction, Sets, score_set, score_sets


class AbstractPlayer(ABC):
    def __init__(self, name: str):
        self.name = name
        self.hand: Hand = set()
        self.sets: Sets = []
        self.can_make_rank_sets: bool = False

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
        assert card in self.hand, f"Card {card} not in hand"
        self.hand.remove(card)

    def _print_hand(self):
        print(
            f"Hand: {', '.join(str(card) for card in sorted(self.hand, key=lambda card: (card.suit, card.get_value())))}"
        )

    def _print_sets(self):
        print(f"Sets: {', '.join(str(set) for set in self.sets)}")

    @abstractmethod
    def decide_action(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> PlayerAction:
        """
        Decide the player's action based on the current game state.
        If the player chooses to take from the field,
        the card at the index chosen must be able to form a set with the player's hand.
        - Validated in game._decide_action
        """
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
        - Validated in self.remove_card
        """
        raise NotImplementedError

    @abstractmethod
    def make_sets(self, mandatory: Card | None) -> Sets:
        """
        Again, this does not actually make the sets.
        This is the game class' responsibility.
        Exactly one of the returned sets must contain the mandatory card.
        - Validated in game._make_sets
        """
        raise NotImplementedError
