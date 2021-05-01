from enum import Enum


class Colour(str, Enum):
    pass


class SnookerColour(Colour):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    BROWN = "BROWN"
    BLUE = "BLUE"
    PINK = "PINK"
    BLACK = "BLACK"
    WHITE = "WHITE"
    TABLE = "TABLE"
