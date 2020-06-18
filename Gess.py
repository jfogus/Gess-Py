# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Starting point for the Gess game.


import sys
from models.Game import Game
from models.Player import Player
from models.Board import Board
from models.History import History
from controllers.BoardController import BoardController
from controllers.HistoryController import HistoryController
from views.GameView import GameView
from views.BoardView import BoardView
from views.SquareView import SquareView
from views.StatusView import StatusView
from views.HistoryView import HistoryView
from PySide2.QtWidgets import QApplication


class Gess(QApplication):
    """ This is not meant to be run as a script. Performs simple tests. """
    def __init__(self, sys_argv):
        super(Gess, self).__init__(sys_argv)

        # Models
        self._board = Board()
        # TODO: Move to external file of constants
        self._players = (Player('b'), Player('w'))
        self._game = Game(self._players, self._board)
        self._history = History(self._game)

        # Controllers
        self._board_controller = BoardController(self._game)
        self._history_controller = HistoryController(self._game)

        board_size = len(self._board.get_squares())

        # Views
        self._square_views = [[SquareView((i, j)) for j in range(board_size)] for i in range(board_size)]
        self._board_view = BoardView(self._square_views, self._game, self._board_controller)
        self._status_view = StatusView(self._game)
        self._history_view = HistoryView(self._history, self._history_controller)
        self._game_view = GameView(self._board_view, self._status_view, self._history_view)
        self._game_view.show()


if __name__ == "__main__":
    app = Gess(sys.argv)
    sys.exit(app.exec_())
