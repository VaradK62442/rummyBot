"""
Utility methods for sets.
"""

from collections.abc import Callable
from itertools import combinations

from common import Card, Hand, Set, Sets


def is_valid_suit_set(card_set: Set) -> bool:
    if len(card_set) < 3:
        return False

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
    if len(card_set) < 3:
        return False

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
    hand: Hand,
    opponent_sets: list[Sets],
    opponent_names: list[str],
    set_check: Callable[[Set], bool] = is_valid_set,
) -> tuple[Set | None, str]:
    for set_size in range(len(hand), 2, -1):
        for combination in combinations(hand, set_size):
            if set_check(set(combination)):
                return (set(combination), "")

    for set_size in [2, 1]:
        for combination in combinations(hand, set_size):
            for name, opponent_set in zip(opponent_names, opponent_sets):
                if can_add_to_sets(set(combination), opponent_set, set_check):
                    return (set(combination), name)

    return (None, "")


def get_all_sets(
    hand: Hand,
    opponent_sets: list[Sets],
    opponent_names: list[str],
    set_check: Callable[[Set], bool] = is_valid_set,
) -> dict[str, Sets]:
    """
    Greedy, search for longest possible set,
    remove those cards, and repeat until no more sets can be found.
    """
    all_sets: dict[str, Sets] = {name: [] for name in opponent_names + [""]}
    hand_copy = hand.copy()
    while len(hand_copy) > 0:
        longest_set, name = get_longest_set(
            hand_copy, opponent_sets, opponent_names, set_check
        )
        if longest_set is not None:
            all_sets[name].append(longest_set)
            hand_copy = hand_copy - longest_set
        else:
            break

    return all_sets


def can_add_to_sets(
    card_set: Set, sets: Sets, set_check: Callable[[Set], bool] = is_valid_set
) -> bool:
    for set in sets:
        if set_check(set | card_set):
            return True

    return False
