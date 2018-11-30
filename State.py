import functools


class State:

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

    BEST = 10**20


    # Initialisierung.
    # S darf None, eine Liste (len == COL) von Listen (len == ROW), oder eine Instanz von State sein.
    # Wird etwas anderes Übergeben, oder tritt ein Fehler in der Liste auf, wird eine Ausnahme erzeugt.
    # [ [int, ...], ... ] self.__F: Liste der Länge COL von Listen der Länge ROW. Die Spielfelder.
    # (int, int) self.__Last: enthält die Koordinaten des letzten Zugs.
    def __init__(self, S = None):
        self.__F = []
        if S == None:
            for c in range(COL):
                self.__F.append([0]*ROW)
        elif type(S) == list:
            self.__F = S
            if not self.is_legal():
                raise "*** FEHLER *** State.__init__  F = %s" % str(self.__F)
        else:
            try:
                for col in S.__F:
                    self.__F.append( col[:] )
            except:
                raise "*** FEHLER *** State.__init__  F = %s" % str(self.__F)
        self.__Last = None


    # Darstellung des Spielzustands als String.
    def __repr__(self):
        s = "\n"
        for r in reversed(range(ROW)):
            for col in self.__F:
                s += REPR[col[r]]
            s += "\n"
        return s


    # Testet auf Gleichheit zweier Spielzustände.
    # True, wenn die Zustände gleich sind, sonst False.
    # State other: der Spielzustand, gegen den getestet werden soll.
    def __eq__(self, other):
        try:
            if self.__F == other.__F:
                return True
        except:
            return False
        return False


    # Liefert einen String im SVG-Format zurück. Dieser stellt den Spielstand dar.
    # float scale: skalierung des erzeugten Bildes.
    def svg(self, scale = 30.0):
        line = '<?xml version="1.0" encoding="UTF-8"?>\n' \
               '<svg width="%f" height="%f">\n' \
               '\t<rect style="fill:#5555ff" x="0" y="0" width="%f" height="%f"/>\n' \
               % (COL * scale, ROW * scale, COL * scale, ROW * scale)

        color = { NONE: "#ffffff", MAXI: "#ff5555", MINI: "#ffff55" }
        for c in range(COL):
            for r in range(ROW):
                line += '\t<circle style="fill:%s" cx="%f" cy="%f" r="%f"/>\n' \
                        % (color[self.__F[c][r]], (c+0.5)*scale, (ROW-r-0.5)*scale, scale*0.5*0.8)

        if self.__Last != None:
            line += '\t<circle style="fill:#000000" cx="%f" cy="%f" r="%f"/>\n' \
                    % ((self.__Last[0]+0.5)*scale, (ROW-self.__Last[1]-0.5)*scale, scale*0.5*0.15)

        line += "</svg>"
        return line


    # Exportiert den Spielzustand mithilfe der SVG-Darstellung und 'convert' in ein nahezu beliebiges
    # Bildformat. Das Format richtet sich nach der Endung in file.
    # String file: Dateiname.
    # float scale: skalierung des erzeugten Bildes.
    def export(self, file = None, scale = 30.0):
        if file != None:
            posix.system( "echo '%s' | convert -antialias - %s" % ( self.svg(scale), file ) )


    # Testet die zulässigkeit des Spielzustands.
    # True, wenn in __F ein gültiger Zustand ist, sonst False.
    # Getestet wird die größe des Feldes, die Einträge, sowie deren Anzahl.
    # Nicht getestet wird, ob der Spielzustand wirklich im Spiel auftreten kann.
    def is_legal(self):
        if not (type(self.__F) == list and len(self.__F) == COL):
            return False
        for col in self.__F:
            if not (type(col) == list and len(col) == ROW):
                return False
            for field in col:
                if type(field) != int:
                    return False
        all = functools.reduce(lambda x,y: x+y, self.__F )
        Maxis = all.count( MAXI )
        Minis = all.count( MINI )
        Nones = all.count( NONE )
        if Maxis + Minis + Nones != COL*ROW:
            return False
        if not (Maxis == Minis or Maxis == Minis + 1):
            return False
        for col in self.__F:
            try:
                i = col.index(NONE)
            except:
                continue
            for field in col[i+1:ROW]:
                if field != NONE:
                    return False
        if self.winner() == -1:
            return False
        return True


    # Gibt zurück, wer als nächstes an der Reihe ist.
    # Gibt MAXI, MINI oder NONE zurück. Letzteres nur, wenn das Feld voll ist.
    # Prüft insbesondere nicht auf Gewinn.
    def whos_next(self):
        all = functools.reduce( lambda x,y: x+y, self.__F )
        Empty = all.count( NONE )
        if Empty == 0:
            return NONE
        if (COL*ROW - Empty) % 2 == 0:
            return MAXI
        else:
            return MINI


    # Liefert alle möglichen Folgezstände, als Liste.
    def get_Successors(self, Complete = False):
        if self.winner() in (MAXI, MINI):
            return []
        who = self.whos_next()
        succs = []

        ### Connect Four
        for c in range(COL):
            try:
                r = self.__F[c].index(NONE)
                S = State(self)
                S.__F[c][r] = who
                S.__Last = (c,r)
                succs.append(S)
            except:
                if Complete:
                    succs.append(None)


        return succs


    # Zählt die offenen Gewinnmöglichkeiten auf dem Spielfeld.
    # Gezählt wird vertikal, horizontal und in zwei Richtung diagonal.
    # Rückgabe ist ein Dictionary mit jeweils einem Eintrag für MAXI und für MINI.
    # Der Eintrag ist jeweils eine Liste der Länge WIN.
    # Dabei gilt: Eintrag[0] == Anzahl der "Einer", die noch zum Gewinn führen können.
    #             Eintrag[1] == Anzahl der "Zweier", ...
    def count(self):
        vert = self.__F                                                    # |
        horz = [ [col[row] for col in self.__F] for row in range(ROW) ]    # -
        dia1 = [ [] for x in range(COL+ROW-1) ]                            # \
        dia2 = [ [] for x in range(COL+ROW-1) ]                            # /
        for c in range(COL):
            for r in range(ROW):
                f = self.__F[c][r]
                dia1[c+r].append( f )
                dia2[c-r+ROW-1].append( f )

        counter = { MAXI: [0]*WIN, MINI: [0]*WIN }

        for strip in vert + horz + dia1 + dia2:
            for i in range(len(strip)-WIN+1):
                part = strip[i:i+WIN]
                c = dict( [(who, part.count(who)) for who in (NONE, MAXI, MINI)] )
                for who in (MAXI, MINI):
                    if c[who] > 0 and c[NONE] + c[who] == WIN:
                        counter[who][c[who]-1] += 1

        return counter


    # Wertet das Ergebnis aus self.count() aus, und liefert eine Bewertung zurück.
    # Positive Bewertugen sind gut für MAXI, negative für MINI.
    def value(self):
        counter = self.count()
        if counter[MAXI][WIN-1] > 0 and counter[MINI][WIN-1] == 0:
            return BEST
        if counter[MAXI][WIN-1] == 0 and counter[MINI][WIN-1] > 0:
            return -BEST
        maxval = functools.reduce(lambda x,y: x*10+y, reversed(counter[MAXI]))
        minval = functools.reduce(lambda x,y: x*10+y, reversed(counter[MINI]))
        return maxval - minval


    # Testet, ob der aktuellen Zustand eine Gewinnsituation ist.
    # -1, falls beide Spieler die Sieglänge erreicht haben.
    # MAXI oder MINI, falls der entsprechende Spieler gewonnen hat.
    # NONE, falls es noch keinen Gewinner gibt.
    def winner(self):
        counter = self.count()
        if counter[MAXI][WIN-1] > 0 and counter[MINI][WIN-1] > 0:
            return -1
        if counter[MAXI][WIN-1] > 0:
            return MAXI
        if counter[MINI][WIN-1] > 0:
            return MINI
        return NONE


