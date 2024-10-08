import numpy as np
import os
import scipy as sp

BASE_DECK_SIZE = 52
PLAYED_HAND_SIZE = 5
HAND_SIZE = 8
SUITS = ('h', 'c', 'd', 's')
BASE_CHIP_MAPPING = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'j': 10, 'q': 10, 'k': 10, 'a': 11}
RANK_ORDER_MAPPING = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'j': 11, 'q': 12, 'k': 13, 'a': (14,1)}
RANKS = tuple(BASE_CHIP_MAPPING.keys())