"""
Author: Jasmin Polszakewitz & Lea Kleinrensing, ITF17a
Version: 1.0
"""
from GuiClass import GuiClass
from ConsoleClass import ConsoleClass
import pygame
from HumanPlayer import Human
import AlphaBeta
import MiniMax
import Game
import State



class Main():
    def main():
        Eingabe = input("Console 'C' , GUI 'G' or exit?")

        if Eingabe == "G" or Eingabe== "g":
            GuiClass.gui()
        elif Eingabe == "C" or Eingabe== "c":
            ConsoleClass.console()


    H = Human("HUM")
    AB = AlphaBeta("AB", 7)
    MM = MiniMax("MM", 4)
    G = Game()
    S = State()

    G.play(S, H, MM)




    if __name__ == '__main__':

        main()

