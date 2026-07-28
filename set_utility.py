"""
Utility methods for sets.
"""

from collections.abc import Callable
from itertools import combinations

from common import Card, Hand, Set


def is_valid_suit_set(card_set: Set) -> bool:
    """
    Assume len(card_set) >= 3.
    """

    if len({card.suit for card in card_set}) == 1:
        ranks = sorted(card.get_value() for card in card_set)

        if len(set(ranks)) != len(card_set):
            return False

        ranks = set(ranks)

        if 1 in ranks:
            alt_ranks = sorted(14 if r == 1 else r for r in ranks)

            if max(alt_ranks) - min(alt_ranks) != len(alt_ranks) - 1:
                return False

        elif max(ranks) - min(ranks) != len(ranks) - 1:
            return False

        return True

    return False


def is_valid_rank_set(card_set: Set) -> bool:
    """
    Assume len(card_set) >= 3.
    """
    return len({card.rank for card in card_set}) == 1


def is_valid_set(card_set: Set) -> bool:
    if len(card_set) < 3:
        return False

    return is_valid_suit_set(card_set) or is_valid_rank_set(card_set)


def can_make_set_with(
    card: Card, hand: Hand, set_check: Callable[[Set], bool] = is_valid_set
) -> Set | None:
    for set_size in range(2, len(hand) + 1):
        for combination in combinations(hand, set_size):
            if set_check(set(combination) | {card}):
                return set(combination) | {card}

    return None


def get_longest_set(
    hand: Hand, set_check: Callable[[Set], bool] = is_valid_set
) -> Set | None:
    for set_size in range(len(hand), 2, -1):
        for combination in combinations(hand, set_size):
            if set_check(set(combination)):
                return set(combination)

    return None
