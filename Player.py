import time
import functools
import os




class Player:

    global COL, ROW, WIN, NONE, MAXI, MINI, REPR, INFINITY, BEST


    def __init__(self, Name):


        COL = 7
        ROW = 6
        WIN = 4

        NONE = 0
        MAXI = 1
        MINI = 2

        BEST = 10**20
        self._Name = Name

    def __repr__(self):
        return "[Player] %s" % self._Name

    # Liefert das Tupel (Folgezustand, Bewertung) zurück.
    # State S: der Spielzustand, der gespielt werden soll.
    def move(self, S):
        return 0, None


