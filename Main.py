"""
Author: Jasmin Polszakewitz & Lea Kleinrensing, ITF17a
Version: 1.0
"""
from GuiClass import GuiClass
import pygame
from HumanPlayer import Human
from AlphaBeta import AlphaBeta
from MiniMax import MiniMax
from Game import Game
from State import State



class main():
    def main():
        Eingabe = input("Console 'C' , GUI 'G' or exit?")

        if Eingabe == "G" or Eingabe== "g":
            GuiClass.gui()
        elif Eingabe == "C" or Eingabe== "c":

            H = Human("HUM")
            AB = AlphaBeta("AB", 7)
            MM = MiniMax("MM", 4)
            G = Game()
            S = State()

            G.play(S, H, MM)

    if __name__ == '__main__':

        main()


