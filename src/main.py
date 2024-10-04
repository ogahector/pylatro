import numpy as np
import os
import scipy as sp
from constants import *

class Edition:
    def __init__(self, edition:str) -> None:
        pass

class Card:
    def __init__(self, suit:str, rank:str, enhancement:str=None, edition:str=None) -> None:
        self.suit = suit
        self.rank = rank
        self.base_chips = RANK_MAPPING[rank]
        self.base_mult = 0
        self.enhancement = enhancement
        self.edition = edition
