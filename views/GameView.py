# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  The main view for the Gess game.  Contains the grid, a title,
#               a status indicator, and a history of moves.


from PySide2.QtWidgets import QMainWindow
from views.BoardView import BoardView


class GameView(QMainWindow):
    """ Represents the main window of a Gess game. """
    def __init__(self):
        super(GameView, self).__init__()

        self.setWindowTitle("Gess!")
        self.setCentralWidget(BoardView())