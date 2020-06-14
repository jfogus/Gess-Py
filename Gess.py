# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Starting point for the Gess game.


import sys
from models.Game import Game
from models.History import History
from controllers.BoardController import BoardController
from controllers.HistoryController import HistoryController
from views.GameView import GameView
from PySide2.QtWidgets import QApplication


class Gess(QApplication):
    """ This is not meant to be run as a script. Performs simple tests. """
    def __init__(self, sys_argv):
        super(Gess, self).__init__(sys_argv)

        # Models
        self._game_model = Game()
        self._history_model = History()

        # Controllers
        self._board_controller = BoardController(self._game_model)
        self._history_controller = HistoryController(self._game_model)

        # Views
        self._game_view = GameView(self._game_model,
                                  self._board_controller,
                                  self._history_model,
                                  self._history_controller)
        self._game_view.show()


if __name__ == "__main__":
    app = Gess(sys.argv)
    sys.exit(app.exec_())
