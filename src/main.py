from random import sample
from typing import NamedTuple
from constants import *


class Card:
    def __init__(self, suit:Suit, rank:RankOrder, enhancement=None, edition=None) -> None:
        self.suit:Suit = suit
        self.rank:RankOrder = rank
        self.base_chips:BaseChips = BaseChips[rank.name]
        self.base_mult = 0

    def score_card(self): # review scoring mechanism
        return self.base_chips, self.base_mult
    
    def __repr__(self) -> str:
        return f'{self.rank.name} of {self.suit.name}'

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
        sampled_cards = sample(self.deck.drawable_cards, HAND_SIZE)
        self.hand.add(sampled_cards)
        self.deck.remove(sampled_cards)

class Hand():
    def __init__(self, size:int) -> None:
        self.cards = []
        self.selected = []
        self.scorer = HandScorer()

    def add(self, card:list[Card] | Card):
        if isinstance(card, list):
            if len(card) > HAND_SIZE:
                raise Exception('Added Too Many Cards to Hand!')
            else:
                for i in card:
                    self.add(i)
        elif len(self.cards) < HAND_SIZE:
            self.cards.append(card)
        else: 
            raise Exception('Could not add card to Hand: Hand already full!')

    def remove(self, card:list[Card] | Card) -> None:
        if isinstance(card, list):
            for i in card:
                self.remove(i)
        else: 
            self.cards.remove(card)
    
    def select_cards(self, indexes:int|list[int]) -> None:
        if len(indexes) <= PLAYABLE_HAND_SIZE or isinstance(indexes, int):
            for i in indexes: 
                self.selected.append(self.cards[i])

    def deselect(self) -> None:
        self.selected = []

    def play_selected(self) -> None:
        if len(self.selected) > PLAYABLE_HAND_SIZE: 
            raise Exception('Too Many Cards Selected!')
        self.scorer.add(self.selected)

        self.remove(self.selected)
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
        self.rank_info = {}
        self.suit_info = {}
        self.score = 0,0

    def add(self, added_cards:list[Card] | Card) -> None:
        if isinstance(added_cards, list):
            if len(added_cards) > PLAYABLE_HAND_SIZE: 
                raise Exception('Too many cards Scored!')
            for card in added_cards:
                self.cards.append(card)
                #print(f"Appended {card} to HandScorer's cards")
        else:
            self.cards.append(card)
            #print(f"Appended {card} to HandScorer's cards")

    def get_hand_info(self, write_card_info:bool=True) -> dict[dict, dict]:
        if self.cards:
            ranks_seen = {}
            suits_seen = {}
            for card in self.cards:
                if card.rank in ranks_seen:
                    ranks_seen[card.rank] += 1
                else: ranks_seen[card.rank] = 1

                if card.suit in suits_seen:
                    suits_seen[card.suit] += 1
                else: suits_seen[card.suit] = 1
            if write_card_info: 
                self.rank_info = ranks_seen
                self.suit_info = suits_seen
            return ranks_seen, suits_seen
        else: 
            raise Exception('Cannot get_hand_info! Play some cards first!')

    def get_hand_type(self) -> HandType:
        self.get_hand_info(write_card_info=True)
        if self.cards:
            if self.is_royal_flush(): return HandType.ROYAL_FLUSH
            elif self.is_straight_flush(): return HandType.STRAIGHT_FLUSH
            elif self.is_4oak(): return HandType.FOUR_OAK
            elif self.is_full_house(): return HandType.FULL_HOUSE
            elif self.is_flush(): return HandType.FLUSH
            elif self.is_straight(): return HandType.STRAIGHT
            elif self.is_3oak(): return HandType.THREE_OAK
            elif self.is_two_pair(): return HandType.TWO_PAIR
            elif self.is_pair(): return HandType.PAIR
            else: return HandType.HIGH_CARD
        else: 
            return 'No Hand Played'

    def is_high_card(self) -> bool:
        return bool(self.cards)

    def is_pair(self) -> bool:
        return 2 in self.rank_info.values()

    def is_two_pair(self) -> bool:
        rank_info = self.rank_info
        first_pair: bool = self.is_pair()
        if not first_pair: return False
        for key, val in rank_info.items():
            if val == 2: 
                del rank_info[key]
                break
        return first_pair and 2 in rank_info.values()


    def is_3oak(self) -> bool:
        return 3 in self.rank_info.values()

    def is_straight(self) -> bool:
        rank_info = self.rank_info.keys()
        rank_order = [RankOrder[rank.name].value for rank in rank_info]
        return sorted(rank_order) == list(range(min(rank_order), max(rank_order)))
        rank_order.sort()
        for i in range(len(rank_order)):
            if rank_order[i+1] != rank_order[i] + 1: 
                return False
        return True

    def is_flush(self) -> bool:
        return 5 in self.suit_info.values()

    def is_full_house(self) -> bool:
        return 2 in self.rank_info.values() and 3 in self.rank_info.values()

    def is_4oak(self) -> bool:
        return 4 in self.rank_info.values()

    def is_straight_flush(self) -> bool:
        return self.is_flush() and self.is_straight()

    def is_royal_flush(self) -> bool:
        ...

    

class Deck(Card):
    def __init__(self) -> None:
        self.drawable_cards = [Card(suit=suit, rank=rank) for suit in Suit for rank in RankOrder]
        self.full_cards = self.drawable_cards

    def get_deck_size(self) -> int:
        return len(self.full_cards)
    
    def remove(self, card:list[Card] | Card) -> None:
        if isinstance(card, list):
            for i in card:
                self.remove(i)
        else:
            self.drawable_cards.remove(card)

    def __len__(self) -> str:
        return len(self.full_cards)


def main() -> None:
    gameinstance = Game()
    print(len(gameinstance.deck))
    gameinstance.draw_hand()
    gameinstance.hand.print_hand()
    gameinstance.hand.select_cards([i for i in range(5)])
    gameinstance.hand.play_selected()
    print(gameinstance.hand.scorer.cards)

    print(gameinstance.hand.scorer.get_hand_info())
    print()
    print(gameinstance.hand.scorer.is_high_card())
    print(gameinstance.hand.scorer.is_pair())
    print(gameinstance.hand.scorer.is_two_pair())
    print(gameinstance.hand.scorer.is_3oak())
    print(gameinstance.hand.scorer.is_straight())
    print(gameinstance.hand.scorer.is_flush())
    print(gameinstance.hand.scorer.is_full_house())
    
    print(len(gameinstance.deck))



if __name__ == '__main__':
    main()