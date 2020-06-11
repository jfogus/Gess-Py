# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Starting point for the Gess game.


import sys
from models.Game import Game
from controllers.BoardController import BoardController
from views.GameView import GameView
from PySide2.QtWidgets import QApplication


class Gess(QApplication):
    """ This is not meant to be run as a script. Performs simple tests. """
    def __init__(self, sys_argv):
        super(Gess, self).__init__(sys_argv)

        # Models
        self.game_model = Game()

        # Controllers
        self.board_controller = BoardController(self.game_model)

        # Views
        self.game_view = GameView(self.game_model, self.board_controller)
        self.game_view.show()


if __name__ == "__main__":
    app = Gess(sys.argv)
    sys.exit(app.exec_())
