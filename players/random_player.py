from random import randint

from common import Card, PlayerAction, Sets

from .player import AbstractPlayer


class RandomPlayer(AbstractPlayer):
    def decide_action(
        self,
        field: list[Card],
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> PlayerAction:
        return PlayerAction(randint(-1, len(field) - 1))

    def choose_discard(
        self,
        field: list[Card],
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> Card:
        return self.hand[0]
