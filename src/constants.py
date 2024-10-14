from enum import Enum

BASE_DECK_SIZE = 52
PLAYABLE_HAND_SIZE = 5
HAND_SIZE = 8

class Suit(Enum):
    SPADE = 0
    HEART = 1
    CLUB = 2
    DIAMOND = 3

class BaseChips(Enum):
    #ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10
    ACE = 11


class RankOrder(Enum):
    #ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class HandType(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OAK = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OAK = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

class Score:
    def __init__(self, chips:float=0, mult:float=0) -> None:
        self.chips = chips
        self.mult = mult

    def apply_chips(self, func:callable) -> None:
        self.chips = func(self.chips)

    def apply_mult(self, func:callable) -> None:
        self.mult = func(self.mult)

    def __add__(self, value):
        return Score(self.chips + value.chips, self.mult + value.mult)

    def __repr__(self) -> str:
        return f"Chips: {self.chips} | Mult: {self.mult}"


class PlanetScore(Enum):
    HIGH_CARD = Score([1, 5])
    PAIR = 10, 2
    TWO_PAIR = 20, 2
    THREE_OAK = 30, 2
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OAK = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


def main() -> None:
    print(PlanetScore.HIGH_CARD.value)

if __name__ == '__main__':
    main()