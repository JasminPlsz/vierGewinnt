import Player

class Human(Player):

    def __init__(self, Name):
        #Player.__init__(self, Name)
        super().__init__(Name)

    def __repr__(self):
        return "[Human Player] %s" % self._Name

    def move(self, S):
        succs = S.get_Successors(True)
        if succs == [None] * COL:
            return 0, None
        moves = [i+1 for i in range(len(succs)) if succs[i] != None]
        while True:
            x = input("your move %s: " % moves)
            try:
                move = int(x)
            except:
                move = -1
            if move in moves:
                return 0, succs[move-1]


