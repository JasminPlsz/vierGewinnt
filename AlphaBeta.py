import functools
from Player import Player


class AlphaBeta(Player):


    global COL, ROW, WIN, NONE, MAXI, MINI, REPR, INFINITY, BEST


    ###
    # nur einzelene Ziffern vergeben
    NONE = 0
    MAXI = 1
    MINI = 2

    COL = 7
    ROW = 6
    WIN = 4


    INFINITY = 10**100

    def __init__(self, Name, Depth = INFINITY):
        Player.__init__(self, Name)
        self._Depth = Depth
        if self._Depth < 1:
            self._Depth = 1

    def __repr__(self):
        s = "[AlphaBeta Player] %s" % self._Name
        if self._Depth != INFINITY:
            s += " <%d>" % self._Depth
        return s

    def move(self, S):
        return self._AlphaBeta(S, -INFINITY, INFINITY, 0, [])

    def _AlphaBeta(self, S, Alpha, Beta, Depth, Trace):
        if Depth >= self._Depth:
            return S.value(), None
        succs = S.get_Successors()
        if succs == []:
            return S.value(), None

        v, next = 0, None
        if S.whos_next() == MAXI:
            succs.sort(key = lambda x: -x.value())
            v = -INFINITY
            for i, s in enumerate(succs):
                m, null = self._AlphaBeta(s, Alpha, Beta, Depth + 1, Trace + [i])
                if v < m:
                    v = m
                    next = s
                if v >= Beta:
                    return v, next
                Alpha = max( Alpha, v )
        else:
            succs.sort(key = lambda x: x.value())
            v = INFINITY
            for i, s in enumerate(succs):
                m, null = self._AlphaBeta(s, Alpha, Beta, Depth + 1, Trace + [i])
                if v > m:
                    v = m
                    next = s
                if v <= Alpha:
                    return v, next
                Beta = min( Beta, v )

        return v, next

