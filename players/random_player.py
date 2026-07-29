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

        if self.has_made_suit_set:
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
        opponent_sets: list[Sets],
        opponent_names: list[str],
    ) -> dict[str, Sets]:
        """
        Make all possible sets from the player's hand.
        """
        return get_all_sets(
            self.hand,
            opponent_sets,
            opponent_names,
            is_valid_set if self.has_made_suit_set else is_valid_suit_set,
        )
