import functools
import Player


class MiniMax(Player):


    INFINITY = 10**100


    ###
    # nur einzelene Ziffern vergeben
    NONE = 0
    MAXI = 1
    MINI = 2

    def __init__(self, Name, Depth = INFINITY):
        Player.__init__(self, Name)
        self._Depth = Depth
        if self._Depth < 1:
            self._Depth = 1

    def __repr__(self):
        s = "[MiniMax Player] %s" % self._Name
        if self._Depth != INFINITY:
            s += " <%d>" % self._Depth
        return s

    def move(self, S):
        return self._MiniMax(S, 0)

    def _MiniMax(self, S, Depth):
        if Depth >= self._Depth:
            return S.value(), None

        succs = S.get_Successors()
        if succs == []:
            return S.value(), None

        if S.whos_next() == MAXI:
            succs.sort(key = lambda x: -x.value())
            vals = [ self._MiniMax(s, Depth + 1)[0] for s in succs ]
            v = max( vals )
        else:
            succs.sort(key = lambda x: x.value())
            vals = [ self._MiniMax(s, Depth + 1)[0] for s in succs ]
            v = min( vals )

        return v, succs[ vals.index( v ) ]


