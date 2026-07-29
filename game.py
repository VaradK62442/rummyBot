"""
Main game logic for the card game Rummy.
"""

import math
from random import seed, shuffle

from common import (
    DECK,
    STARTING_HAND_SIZE,
    Card,
    Field,
    PlayerAction,
    Sets,
    # dprint,
)
from players import AbstractPlayer
from players.random_player import RandomPlayer
from players.user_player import UserPlayer
from set_utility import (
    can_add_to_sets,
    can_make_set_with,
    is_valid_rank_set,
    is_valid_set,
    is_valid_suit_set,
)


class Game:
    def __init__(self, players: list[AbstractPlayer]):
        self.players = {p.name: p for p in players}
        self.player_names = [p.name for p in players]
        self.deck = DECK[:]
        self.current_player_idx = 0
        self.field: Field = []

        shuffle(self.deck)
        self.deal_cards()
        self.add_to_field(self.deck.pop())

    def __str__(self) -> str:
        return f"Field: {', '.join(str(card) for card in self.field)}\nPlayers:\n{'\n'.join(str(player) for player in self.players)}"

    def _give_card(self, player: AbstractPlayer):
        player.add_card(self.deck.pop())

    def deal_cards(self):
        for _ in range(STARTING_HAND_SIZE):
            for player in self.players.values():
                self._give_card(player)

    def add_to_field(self, card: Card):
        self.field.append(card)

    def _make_sets(
        self,
        player_sets: dict[str, Sets],
        player: AbstractPlayer,
        mandatory_card: Card | None,
    ):
        # check mandatory card appears in at least one set
        if mandatory_card is not None and not any(
            mandatory_card in card_set
            for card_sets in player_sets.values()
            for card_set in card_sets
        ):
            raise ValueError(
                f"Mandatory card {mandatory_card} not in any set in {player_sets}"
            )

        for player_name, sets in player_sets.items():
            for set in sets:
                if not is_valid_set(set) and not can_add_to_sets(
                    set, self.players[player_name].sets
                ):
                    raise ValueError(
                        f"Invalid set, cannot make new set nor add to specified player's sets: {self.players[player_name].sets}"
                    )

                if is_valid_suit_set(set):
                    player.has_made_suit_set = True

                player.sets.append(set)
                for card in set:
                    # will (rightfully) error if same card is submitted in two sets
                    player.remove_card(card)

    def _handle_action(self, action: PlayerAction, player: AbstractPlayer):
        print(f"{player.name} takes action: {action}")
        mandatory_card = None
        match action.value:
            case -1:
                if len(self.deck) == 0:
                    self.deck = self.field[:]
                    shuffle(self.deck)
                    self.field = []
                player.add_card(self.deck.pop())
            case idx:
                mandatory_card = self.field[idx]
                if not can_make_set_with(
                    mandatory_card,
                    player.hand | set(self.field[idx + 1 :]),
                    is_valid_set,
                ):
                    raise ValueError(f"Cannot make set with card {mandatory_card}")

                elif (
                    can_make_set_with(
                        mandatory_card,
                        player.hand | set(self.field[idx + 1 :]),
                        is_valid_rank_set,
                    )
                    and not player.has_made_suit_set
                ):
                    raise ValueError("Player cannot make rank sets")

                for _ in range(len(self.field) - idx):
                    player.add_card(self.field.pop())

        player_sets = player.make_sets(
            mandatory_card, self._get_opponent_sets(), self._get_opponent_names()
        )
        self._make_sets(player_sets, player, mandatory_card)

        chosen_discard = player.choose_discard(
            self.field,
            [
                len(opponent.hand)
                for opponent in self.players.values()
                if opponent != player
            ],
            [opponent.sets for opponent in self.players.values() if opponent != player],
        )

        if chosen_discard not in player.hand:
            raise ValueError("Chosen discard is not in player's hand")

        player.remove_card(chosen_discard)
        self.field.append(chosen_discard)

    def _get_winner(self) -> AbstractPlayer | None:
        for player in self.players.values():
            if len(player.hand) == 0:
                return player

        return None

    def _get_opponent_hand_sizes(self) -> list[int]:
        return [
            len(opponent.hand)
            for opponent in self.players.values()
            if opponent != self.player_names[self.current_player_idx]
        ]

    def _get_opponent_sets(self) -> list[Sets]:
        return [
            opponent.sets
            for opponent in self.players.values()
            if opponent != self.player_names[self.current_player_idx]
        ]

    def _get_opponent_names(self) -> list[str]:
        return [
            opponent.name
            for opponent in self.players.values()
            if opponent != self.player_names[self.current_player_idx]
        ]

    def _find_winner(self) -> list[str]:
        scores = {player.name: player.score() for player in self.players.values()}
        winner_score = -math.inf
        winner_names = []

        for k, v in scores.items():
            print(f"{k}: {v} pts")
            if v > winner_score:
                winner_score = v
                winner_names = [k]
            elif v == winner_score:
                winner_names.append(k)

        return winner_names

    def game_loop(self):
        turn_number = 1
        winner = None

        while winner is None:
            current_player = self.players[self.player_names[self.current_player_idx]]

            print(f"Turn {turn_number} - {current_player.name}'s turn.")
            print(f"Field: {', '.join(str(card) for card in self.field)}")
            current_player._print_hand()
            current_player._print_sets()
            print("Opponent hand size and sets:")
            for size, sets, name in zip(
                self._get_opponent_hand_sizes(),
                self._get_opponent_sets(),
                self._get_opponent_names(),
            ):
                print(f"    {name}: {size} - {', '.join(str(card) for card in sets)}")

            action = current_player.decide_action(
                self.field,
                self._get_opponent_hand_sizes(),
                self._get_opponent_sets(),
            )
            self._handle_action(action, current_player)

            print()

            if len(current_player.hand) == 0:
                winner = current_player

            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            turn_number += 1

        print(f"Winner(s): {', '.join(self._find_winner())}")


def main():
    seed(42)

    p1 = RandomPlayer("Player 1")
    p2 = RandomPlayer("Player 2")
    game = Game([p1, p2])

    game.game_loop()


if __name__ == "__main__":
    main()
