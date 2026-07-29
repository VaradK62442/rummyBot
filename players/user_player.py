from common import SUIT_ABBREVS, Card, Field, PlayerAction, Rank, Sets, Suit

from .abstract_player import AbstractPlayer


class UserPlayer(AbstractPlayer):
    def _validate_input(self, raw_input: str) -> bool:
        if not raw_input or "/" not in raw_input:
            print(
                "Invalid input. Please enter a card name in the format '<rank>/<suit>'"
            )
            return False

        if len(raw_input.split("/")) != 2:
            print(
                "Invalid input. Please enter a card name in the format '<rank>/<suit>'"
            )
            return False

        rank, suit = raw_input.split("/")
        if not (rank in Rank and suit in SUIT_ABBREVS):
            print(
                "Invalid input. Please enter a card name in the format '<rank>/<suit>'"
            )
            return False

        return True

    def decide_action(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> PlayerAction:
        print("Enter -1 to draw, or a number to take all cards from that index onwards")
        value = -2
        while value < -1 or value >= len(field):
            raw_value = input()
            if not (
                raw_value.isdigit() or (raw_value[0] == "-" and raw_value[1:].isdigit())
            ):
                print("Invalid input. Please enter a number")
                continue

            value = int(raw_value)
            if value < -1 or value >= len(field):
                print(
                    f"Invalid input. Please enter a number between -1 and {len(field) - 1}"
                )

        return PlayerAction(value)

    def choose_discard(
        self,
        field: Field,
        opponent_hand_sizes: list[int],
        opponent_sets: list[Sets],
    ) -> Card:
        self._print_hand()
        print(
            "Enter the name of the card you want to discard in the format '<rank>/<suit>'"
        )

        raw_input = input()
        while not self._validate_input(raw_input):
            raw_input = input()

        rank, suit = raw_input.split("/")
        card = Card(Suit(SUIT_ABBREVS[suit]), Rank(rank))
        return card

    def make_sets(
        self,
        mandatory: Card | None,
        opponent_sets: list[Sets],
        opponent_names: list[str],
    ) -> dict[str, Sets]:
        self._print_hand()
        print("Enter the number of sets you want to make / add")

        raw_input = input()
        while not raw_input.isdigit():
            print("Invalid input. Please enter a number")
            raw_input = input()

        num_sets = int(raw_input)
        sets = {name: [] for name in opponent_names + [self.name]}

        for i in range(num_sets):
            print(
                f"Enter the name of the player to add set {i + 1} to (leave blank for self)"
            )
            player_name = input()
            while player_name not in opponent_names + [self.name, ""]:
                print("Invalid input. Please enter a player name")
                player_name = input()

            if not player_name:
                player_name = self.name

            print(f"Enter the cards for set {i + 1}, separated by spaces")
            raw_input = input()
            while not raw_input or not all(
                self._validate_input(raw) for raw in raw_input.split()
            ):
                print(
                    "Invalid input. Please enter valid card names separated by spaces"
                )
                raw_input = input()

            sets[player_name].append(
                {
                    Card(Suit(SUIT_ABBREVS[suit]), Rank(rank))
                    for rank, suit in (raw.split("/") for raw in raw_input.split())
                }
            )

        return sets
