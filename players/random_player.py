from random import choice

from common import Card, Field, PlayerAction, Sets
from set_utility import can_make_set_with, get_all_sets, is_valid_set, is_valid_suit_set

from .abstract_player import AbstractPlayer


class RandomPlayer(AbstractPlayer):
    def decide_action(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> PlayerAction:
        """
        Choose a random action within valid choices.
        """
        choices = [-1]

        if self.can_make_rank_sets:
            set_check = is_valid_set
        else:
            set_check = is_valid_suit_set

        for i in range(len(field)):
            if can_make_set_with(field[i], self.hand, set_check):
                choices.append(i)

        return PlayerAction(choice(choices))

    def choose_discard(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> Card:
        return choice(list(self.hand))

    def make_sets(
        self,
        mandatory: Card | None,
    ) -> Sets:
        """
        Make all possible sets from the player's hand.
        """
        return get_all_sets(
            self.hand, is_valid_set if self.can_make_rank_sets else is_valid_suit_set
        )
