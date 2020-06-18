# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  The main view for the Gess game.  Contains the grid, a title,
#               a status indicator, and a history of moves.


from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Qt
from views.BoardView import BoardView
from views.StatusView import StatusView
from views.HistoryView import HistoryView


class GameView(QMainWindow):
    """ Composite view representing the main window of a Gess game. """
    def __init__(self, board_view, status_view, history_view):
        super(GameView, self).__init__()

        self.setWindowTitle("Gess!")
        self.setCentralWidget(board_view)
        self.addDockWidget(Qt.TopDockWidgetArea, status_view)
        self.addDockWidget(Qt.RightDockWidgetArea, history_view)