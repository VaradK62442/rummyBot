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
    Set,
    dprint,
)
from players import AbstractPlayer, RandomPlayer


class Game:
    def __init__(self, players: list[AbstractPlayer]):
        self.players = players
        self.deck = DECK[:]
        self.current_player = 0
        self.field: Field = set()

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
        self.field.add(card)

    def _is_valid_set(self, card_set: Set) -> bool:
        if len(card_set) < 3:
            return False

        if len({card.rank for card in card_set}) == 1:
            return True

        elif len({card.suit for card in card_set}) == 1:
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

    def handle_action(self, action: PlayerAction, player: AbstractPlayer):
        match action.value:
            case -1:
                player.add_card(self.deck.pop())
            case idx:
                for _ in range(len(self.field) - idx):
                    player.add_card(self.field.pop())

        chosen_discard = player.choose_discard(
            self.field,
            [len(opponent.hand) for opponent in self.players if opponent != player],
            [opponent.sets for opponent in self.players if opponent != player],
        )

        if chosen_discard not in player.hand:
            raise ValueError("Chosen discard is not in player's hand")

        player.remove_card(chosen_discard)
        self.field.add(chosen_discard)


def main():
    player = RandomPlayer("Player 1")
    opponent = RandomPlayer("Player 2")

    game = Game([player, opponent])
    game.field = {game.deck.pop() for _ in range(5)}
    dprint(game)

    action = player.decide_action(
        game.field, opponent_hand_sizes=[0], opponent_sets=[set()]
    )
    dprint(action)
    game.handle_action(action, player)
    dprint(game)


if __name__ == "__main__":
    main()
