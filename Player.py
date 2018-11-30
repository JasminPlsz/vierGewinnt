import time
import functools
import os


###
# Spielfeldgröße und Gewinnlänge
COL = 7
ROW = 6
WIN = 4


###
# nur einzelene Ziffern vergeben
NONE = 0
MAXI = 1
MINI = 2


###
# Darstellung
REPR = { NONE: "· ", MAXI: "x ", MINI: "o " }


INFINITY = 10**100
BEST = 10**20


###
# Spielzustand
# Vorrausgesetzt wird, dass MAXI immer den ersten Zug macht.


class Player:

    def __init__(self, Name):
        self._Name = Name

    def __repr__(self):
        return "[Player] %s" % self._Name

    # Liefert das Tupel (Folgezustand, Bewertung) zurück.
    # State S: der Spielzustand, der gespielt werden soll.
    def move(self, S):
        return 0, None


