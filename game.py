"""
Main game logic for the card game Rummy.
"""

from random import shuffle

from common import (
    DECK,
    STARTING_HAND_SIZE,
    Card,
    Field,
    PlayerAction,
    Sets,
    dprint,
)
from players import AbstractPlayer, RandomPlayer
from set_utility import (
    can_make_set_with,
    get_longest_set,
    is_valid_rank_set,
    is_valid_set,
    is_valid_suit_set,
)


class Game:
    def __init__(self, players: list[AbstractPlayer]):
        self.players = players
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
            for player in self.players:
                self._give_card(player)

    def add_to_field(self, card: Card):
        self.field.append(card)

    def _make_sets(
        self, player_sets: Sets, player: AbstractPlayer, mandatory_card: Card
    ):
        # check mandatory card appears in at least one set
        if not any(mandatory_card in set for set in player_sets):
            raise ValueError("Mandatory card not in any set")

        for set in player_sets:
            if not is_valid_set(set):
                raise ValueError("Invalid set")

            player.sets.add(set)
            for card in set:
                # will (rightfully) error if same card is submitted in two sets
                player.remove_card(card)

    def _handle_action(self, action: PlayerAction, player: AbstractPlayer):
        match action.value:
            case -1:
                player.add_card(self.deck.pop())
            case idx:
                l = self.field[idx]
                if not can_make_set_with(l, player.hand, is_valid_set):
                    raise ValueError("Cannot make set with card")

                elif (
                    can_make_set_with(l, player.hand, is_valid_rank_set)
                    and not player.can_make_rank_sets
                ):
                    raise ValueError("Player cannot make rank sets")

                for _ in range(len(self.field) - idx):
                    player.add_card(self.field.pop())

                player_sets = player.make_sets(mandatory=l)
                self._make_sets(player_sets, player, l)

        chosen_discard = player.choose_discard(
            self.field,
            [len(opponent.hand) for opponent in self.players if opponent != player],
            [opponent.sets for opponent in self.players if opponent != player],
        )

        if chosen_discard not in player.hand:
            raise ValueError("Chosen discard is not in player's hand")

        player.remove_card(chosen_discard)
        self.field.append(chosen_discard)

    def _get_winner(self) -> AbstractPlayer | None:
        for player in self.players:
            if len(player.hand) == 0:
                return player

        return None

    def _get_opponent_hand_sizes(self) -> list[int]:
        return [
            len(opponent.hand)
            for opponent in self.players
            if opponent != self.players[self.current_player_idx]
        ]

    def _get_opponent_sets(self) -> list[Sets]:
        return [
            opponent.sets
            for opponent in self.players
            if opponent != self.players[self.current_player_idx]
        ]

    def game_loop(self):
        winner = None

        while winner is None:
            current_player = self.current_player_idx
            action = self.players[current_player].decide_action(
                self.field,
                self._get_opponent_hand_sizes(),
                self._get_opponent_sets(),
            )
            self._handle_action(action, self.players[current_player])

            if len(self.players[current_player].hand) == 0:
                winner = self.players[current_player]

            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

        print(f"Player {winner.name} has won!")


def main():
    player = RandomPlayer("Player 1")
    opponent = RandomPlayer("Player 2")

    game = Game([player, opponent])
    game.field = [game.deck.pop() for _ in range(5)]
    dprint(game)

    action = player.decide_action(
        game.field, opponent_hand_sizes=[0], opponent_sets=[set()]
    )
    dprint(f"Player 1 does {action}")
    game._handle_action(action, player)
    dprint(game)

    dprint(f"any: {can_make_set_with(game.field[-1], player.hand, is_valid_set)}")
    dprint(f"rank: {can_make_set_with(game.field[-1], player.hand, is_valid_rank_set)}")
    dprint(f"suit: {can_make_set_with(game.field[-1], player.hand, is_valid_suit_set)}")

    dprint(f"longest: {get_longest_set(player.hand, is_valid_set)}")


if __name__ == "__main__":
    main()
