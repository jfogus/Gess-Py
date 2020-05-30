# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Starting point for the Gess game.


import sys
from models.Board import Board
from models.Player import Player
from PySide2.QtWidgets import QApplication
from views.GameView import GameView


def main():
    """ This is not meant to be run as a script. Performs simple tests. """
    b = Board()
    p = Player('b')
    b.move_piece(p, 'c3', 'c4')
    b.print_board()

    app = QApplication(sys.argv)

    board = GameView()
    board.show()

    app.exec_()


if __name__ == "__main__":
    main()
