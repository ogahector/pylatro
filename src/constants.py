import numpy as np
import os
import scipy as sp

BASE_DECK_SIZE = 52
PLAYED_HAND_SIZE = 5
HAND_SIZE = 8
SUITS = ('h', 'c', 'd', 's')
RANK_MAPPING = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'j': 10, 'q': 10, 'k': 10, 'a': 11}
RANKS = tuple(RANK_MAPPING.keys())