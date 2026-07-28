from common import Card, Field, PlayerAction, Sets

from .player import AbstractPlayer


class UserPlayer(AbstractPlayer):
    def decide_action(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> PlayerAction:
        return PlayerAction(-1)

    def choose_discard(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> Card:
        return next(iter(self.hand))

    def make_sets(
        self,
        mandatory: Card,
    ) -> Sets:
        """
        Make all possible sets from the player's hand.
        """
        return set()
