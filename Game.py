import time
import os
from Player import Player

class Game:




    def __init__(self):

        global COL, ROW, WIN, NONE, MAXI, MINI, REPR, INFINITY, BEST
        COL = 7
        ROW = 6
        WIN = 4

        NONE = 0
        MAXI = 1
        MINI = 2

        REPR = { NONE: "· ", MAXI: "x ", MINI: "o " }


        INFINITY = 10**100
        BEST = 10**20


        ###
        # Darstellung
        REPR = { NONE: "· ", MAXI: "x ", MINI: "o " }

        BEST = 10**20

        self.States = []
        self.OutDir = None


    def play(self, S, PlayerMaxi, PlayerMini = None, OutDir = None):


        self.States = []
        self.OutDir = OutDir
        if self.OutDir != None:
            try:
                os.mkdir( self.OutDir )
                os.chdir( self.OutDir )
            except:
                self.out( "Verzeichnis existiert bereits oder lässt sich nicht erzeugen: %s !" % self.OutDir )
                self.OutDir = None

        if PlayerMini != None:
            Player = { MAXI: PlayerMaxi, MINI: PlayerMini }
        else:
            Player = { MAXI: PlayerMaxi, MINI: PlayerMaxi }

        if not S.is_legal():
            self.out( "illegal: %d" % str(S) )
            return -1

        N = S
        statenr = 0
        #self.out( "", True )
        self.out( "Connect Four" )
        self.out( "%s   - vs -   %s" % (str(Player[MAXI]), str(Player[MINI])) )
        self.out( "start state" )
        while True:
            self.States.append(N)
            self.out( N )
            if self.OutDir != None:
                N.export( "state-%02d.png" % statenr )
                statenr += 1

            self.out( "val: %s" % self.__val_to_str( N.value() ) )
            #self.out( "", True )

            if N.get_Successors() == []:
                break
            who = N.whos_next()

            self.out( "-" * 20 )
            self.out( Player[who] )
            t = time.time()
            w, N = Player[who].move(N)
            self.out( "%.3f sec" % (time.time()-t) )
            self.out( "prediction: %s" % self.__val_to_str(w) )

        self.out( "-" * 20 )
        win = N.winner()
        if win in (MAXI, MINI):
            self.out( "WINNER: %s (%s)" % (Player[win], REPR[win].strip()) )
        else:
            self.out( "TIE" )
        #self.out( "", True )

        if self.OutDir != None:
            os.chdir( ".." )

        return win


    def out(self, S, Timestamp = False):
        outfile = "out.txt"
        if Timestamp:
            S = "[%04d-%02d-%02d %02d:%02d:%02d]  " % time.localtime()[:6] + str(S)
        print(S)
        if self.OutDir != None and outfile != None:
            try:
                f = open(outfile, 'a')
                f.write( str(S) + "\n" )
                f.close()
            except:
                print ("*** FEHLER *** out: Datei \"%s\" lässt sich nicht schreiben!" % outfile)
                outfile = None


    def __val_to_str(self, val):


        if val == BEST:
            return REPR[MAXI] + "wins"
        if val == -BEST:
            return REPR[MINI] + "wins"
        return str(val)
