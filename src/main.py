from random import sample, shuffle
from typing import NamedTuple
from constants import *


class Card:
    def __init__(self, suit:Suit, rank:RankOrder, game=None, enhancement=None, edition=None) -> None:
        self.suit:Suit = suit
        self.rank:RankOrder = rank
        self.game:Game = game
        self.enhancement = enhancement
        self.edition = edition
        self.base_chips:BaseChips = BaseChips[rank.name]
        self.base_mult = 0

    def score(self) -> None:
        self.game.score.add_chips(self.base_chips.value)
        self.game.score.apply_func(lambda x:x) # enchancement
        self.game.score.apply_func(lambda x:x) # edition
    
    def __repr__(self) -> str:
        return f'{self.rank.name} of {self.suit.name}'

class Game:
    def __init__(self) -> None:
        self.deck = Deck(self)
        shuffle(self.deck.drawable_cards)
        self.deck.full_cards = self.deck.drawable_cards
        self.score = Score(0, 0)
        self.money = 0
        self.hand = Hand(HAND_SIZE)
        self.jokers:list[Joker] = []

    def reset_game(self) -> None:
        self.__init__()

    def reset_deck(self) -> None:
        self.deck = Deck()

    def draw_hand(self) -> None:
        sampled_cards = self.deck.drawable_cards[:HAND_SIZE - len(self.hand.cards)]
        self.hand.add(sampled_cards)
        self.deck.remove(sampled_cards)

    def play_hand(self) -> float:
        self.hand.play_selected()
        hand_type = self.hand.scorer.get_hand_type()
        self.score = PlanetScore[hand_type.name].value

        played_card_score_queue = []
        played_card_score_queue = self.hand.scorer.cards
        for card in played_card_score_queue:
            card.score()

        card_in_hand_score_queue = []
        for card in card_in_hand_score_queue:
            card.score()

        for joker in self.jokers:
            joker.ability()
        print(f'Your Hand Was: {hand_type.name}')
        print(f'Your Score Was: {self.score.chips*self.score.mult}')
        return self.score.chips * self.score.mult


class Hand:
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

    def sort_ranks(self) -> None:
        self.cards.sort(key=lambda card:card.rank.value)

    def sort_suits(self) -> None:
        sorted_suits = [[card for card in self.cards if card.suit == suit] for suit in Suit]
        for i in sorted_suits:
            i.sort(key=lambda card: card.rank.value)
        self.cards = [card for sorted_suit in sorted_suits for card in sorted_suit]

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
        self.hand_type: HandType = None

    def add(self, added_cards:list[Card] | Card) -> None:
        if isinstance(added_cards, list):
            if len(added_cards) > PLAYABLE_HAND_SIZE: 
                raise Exception('Too many cards Scored!')
            for card in added_cards:
                self.cards.append(card)
                #print(f"Appended {card} to HandScorer's cards")
        else:
            self.cards.append(added_cards)
            #print(f"Appended {card} to HandScorer's cards")

    def sort_ranks(self) -> None:
        self.cards.sort(key=lambda card:card.rank.value)

    def sort_suits(self) -> None:
        sorted_suits = [[card for card in self.cards if card.suit == suit] for suit in Suit]
        for i in sorted_suits:
            i.sort(key=lambda card: card.rank.value)
        self.cards = [card for sorted_suit in sorted_suits for card in sorted_suit]

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
        if len(self.cards) < 5: 
            return False
        rank_order = [rank.value for rank in self.rank_info.keys()]
        rank_order.sort()
        # check for ace-based straight:
        if RankOrder.ACE.value in rank_order and RankOrder.TWO.value in rank_order:
            for i in range(2, 6):
                if i not in rank_order: return False
            return True
        for i in range(len(rank_order) - 1):
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
        royal = self.rank_info.keys() == [Card(suit=self.cards[0].suit, rank=rank) 
                                        for rank in RankOrder if rank.value >= RankOrder.TEN.value]
        return self.is_straight_flush() and royal
    

class Deck(Card):
    def __init__(self, game:Game) -> None:
        self.game = game
        self.drawable_cards = [Card(suit=suit, rank=rank, game=game) for suit in Suit for rank in RankOrder]
        self.full_cards = self.drawable_cards

    def get_deck_size(self) -> int:
        return len(self.full_cards)
    
    def remove(self, card:list[Card] | Card) -> None:
        if isinstance(card, list):
            for i in card:
                self.remove(i)
        else:
            self.drawable_cards.remove(card)

    def add(self, card:Card) -> None:
        self.full_cards.append(card)
        self.drawable_cards.append(card)

    def delete_card(self, card:Card) -> None:
        self.drawable_cards.remove(card)
        self.full_cards.remove(card)

    def __len__(self) -> str:
        return len(self.full_cards)


def main() -> None:
    G = Game()
    G.draw_hand()
    G.hand.print_hand()
    G.hand.sort_ranks()
    G.hand.select_cards(list(range(5)))
    G.hand.print_selected()
    G.play_hand()
    print(G.score)



if __name__ == '__main__':
    main()