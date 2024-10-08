import numpy as np
import os
import scipy as sp
from collections import namedtuple
from constants import *


class Card:
    def __init__(self, suit:str, rank:str, enhancement=None, edition=None) -> None:
        self.suit = suit
        self.rank = rank
        self.base_chips = BASE_CHIP_MAPPING[rank]
        self.base_mult = 0

    def score_card(self):
        return self.base_chips, self.base_mult
    
    def __repr__(self) -> str:
        return f'{self.rank} of {self.suit}'

class Game:
    def __init__(self) -> None:
        self.deck = Deck()
        self.score = 0
        self.money = 0
        self.hand = Hand(HAND_SIZE)

    def reset_game(self) -> None:
        self.deck = Deck()
        self.score = 0
        self.money = 0
        self.hand = []

    def reset_deck(self) -> None:
        self.deck = Deck()

    def draw_hand(self) -> None:
        randindexes = np.random.randint(low=0, high=self.deck.get_deck_size(), size=HAND_SIZE)
        for i in randindexes:
            self.hand.add(self.deck.cards_left[i])
        for i in self.hand.cards:
            self.deck.remove(i)

class Hand():
    def __init__(self, size:int) -> None:
        self.cards = []
        self.selected = []
        self.size = size
        self.scorer = HandScorer()

    def add(self, card:Card):
        if len(self.cards) < self.size:
            self.cards.append(card)
        else: raise Exception('Could not add card to Hand: Hand already full!')

    def remove(self, card) -> None:
        self.cards.remove(card)
    
    def select_cards(self, indexes:int|list[int]) -> None:
        if len(indexes) <= PLAYED_HAND_SIZE or isinstance(indexes, int):
            for i in indexes: 
                self.selected.append(self.cards[i])

    def deselect(self) -> None:
        self.selected = []

    def play_selected(self) -> None:
        if len(self.selected) > PLAYED_HAND_SIZE: 
            raise Exception('Too Many Cards Selected!')
        self.scorer.add(self.selected)
        #print(f'Hand Score: {self.scorer.score}')
        for card in self.selected:
            self.remove(card)
        self.selected = []

    def print_hand(self) -> None:
        print([card for card in self.cards])

    def print_selected(self) -> None:
        print([card for card in self.selected])

    def __repr__(self) -> str:
        return f'{[repr(card) for card in self.cards]}'


class HandScorer:
    def __init__(self) -> None:
        self.cards = []
        self.card_info = namedtuple('CardInfo', ['ranks', 'suits'])
        self.score = 0,0

    def add(self, added_cards:list[Card] | Card) -> None:
        if isinstance(added_cards, list) and len(added_cards) > PLAYED_HAND_SIZE: 
            raise Exception('Too many cards Scored!')
        for card in added_cards:
            self.cards.append(card)
            print(f'Appended {card} to HandScorer"s cards')

    def get_hand_info(self, write_card_info:bool=True) -> tuple[dict, dict]:
        if self.cards:
            ranks_seen = {}
            suits_seen = {}
            for card in self.cards:
                if card.rank in ranks_seen:
                    ranks_seen[card.rank] += 1
                else: ranks_seen[card.rank] = 1

                if card.suit in suits_seen:
                    suits_seen[card.suit] += 1
                else: ranks_seen[card.rank]
            if write_card_info: self.card_info = self.card_info(ranks=ranks_seen, suits=suits_seen)
            return ranks_seen, suits_seen
        else: 
            raise Exception('Cannot get_hand_info! Play some cards first!')

    def get_hand_type(self) -> str:
        self.get_hand_info()
        if self.cards:
            if self.is_royal_flush(): return 'rf'
            elif self.is_straight_flush(): return 'sf'
            elif self.is_4oak(): return '4oak'
            elif self.is_full_house(): return 'fh'
            elif self.is_flush(): return 'f'
            elif self.is_straight(): return 's'
            elif self.is_3oak(): return '3oak'
            elif self.is_2pair(): return '2p'
            elif self.is_pair(): return 'p'
            else: return 'hc'
        else: return 'No Hand Played'

    def is_high_card(self) -> bool:
        return bool(self.cards)

    def is_pair(self) -> bool:
        return 2 in self.card_info.ranks.values()

    def is_2pair(self) -> bool:
        rank_info = self.card_info.ranks
        first_pair: bool = self.is_pair(self)
        if not first_pair: return False
        for key, val in rank_info.items():
            if val == 2: 
                del rank_info[key]
                break
        return first_pair and 2 in rank_info.values()


    def is_3oak(self) -> bool:
        return 3 in self.card_info.ranks.values()

    def is_straight(self) -> bool:
        rank_info = list(self.card_info.ranks.keys())
        rank_order = [RANK_ORDER_MAPPING[rank] for rank in rank_info]
        rank_order.sort()
        for i in rank_order:
            if rank_order[i+1] != rank_order[i] + 1: 
                return False
        return True

    def is_flush(self) -> bool:
        return 5 in self.card_info.suits.values()

    def is_full_house(self) -> bool:
        rank_info = self.card_info.ranks
        return 2 in rank_info.values() and 3 in rank_info.values()

    def is_4oak(self) -> bool:
        return 4 in self.card_info.ranks.values()

    def is_straight_flush(self) -> bool:
        return self.is_flush() and self.is_straight()

    def is_royal_flush(self) -> bool:
        ...

    
    


class Deck(Card):
    def __init__(self) -> None:
        self.cards_left = [Card(suit=suit, rank=rank) for suit in SUITS for rank in RANKS]
        self.full_cards = self.cards_left

    def get_deck_size(self) -> int:
        return len(self.full_cards)
    
    def remove(self, card:Card=None, index:int=None) -> None:
        if isinstance(card, Card): self.cards_left.remove(card)
        else: self.cards_left.pop(index)

    def __len__(self) -> str:
        return len(self.full_cards)


def main() -> None:
    gameinstance = Game()
    print(len(gameinstance.deck))
    gameinstance.draw_hand()
    gameinstance.hand.print_hand()
    gameinstance.hand.select_cards([i for i in range(5)])
    gameinstance.hand.play_selected()
    print(gameinstance.hand.selected)

    #print(gameinstance.hand.scorer.get_hand_info())
    print(len(gameinstance.deck))



if __name__ == '__main__':
    main()