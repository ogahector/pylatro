from enum import Enum
# from main import Game, Hand, HandScorer

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

    def add_chips(self, chips) -> None:
        self.chips += chips

    def add_mult(self, mult) -> None:
        self.mult += mult

    def apply_chips(self, func:callable) -> None:
        self.chips = func(self.chips)

    def apply_mult(self, func:callable) -> None:
        self.mult = func(self.mult)

    def apply_func(self, func:callable) -> None:
        self = func(self)

    def __add__(self, value):
        return Score(self.chips + value.chips, self.mult + value.mult)

    def __repr__(self) -> str:
        return f"Chips: {self.chips} | Mult: {self.mult}"


class PlanetScore(Enum):
    HIGH_CARD = Score(5, 1)
    PAIR = Score(10, 2)
    TWO_PAIR = Score(20, 2)
    THREE_OAK = Score(30, 2)
    STRAIGHT = Score(30, 4)
    FLUSH = Score(35, 4)
    FULL_HOUSE = Score(40, 4)
    FOUR_OAK = Score(60, 7)
    STRAIGHT_FLUSH = Score(100, 8)
    ROYAL_FLUSH = STRAIGHT_FLUSH


class Joker:
    def __init__(self, game, name:str, rarity:str, 
                blueprint_compat:bool, eternal_compat:bool, 
                perishable_compat:bool, buy_value:int, sell_value:int,
                description:str=None) -> None:
        self.game = game
        self.name = name
        self.rarity = rarity
        self.buy_value = buy_value
        self.sell_value = sell_value
        self.blueprint_compat = blueprint_compat
        self.eternal_compat = eternal_compat
        self.perishable_compat = perishable_compat
        self.description = description

    def ability(self) -> Score | None:
        raise NotImplementedError("Joker Must Implement Ability!")

    def sell(self) -> None:
        self.game.money += self.sell_value
        del self


def main() -> None:
    print(PlanetScore.HIGH_CARD.value)

if __name__ == '__main__':
    main()