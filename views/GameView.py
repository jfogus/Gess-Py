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
    """ Represents the main window of a Gess game. """
    def __init__(self, model, controller, right_model, right_controller):
        super(GameView, self).__init__()

        self.setWindowTitle("Gess!")
        self.setCentralWidget(BoardView(model, controller))
        self.addDockWidget(Qt.TopDockWidgetArea, StatusView(model))
        self.addDockWidget(Qt.RightDockWidgetArea, HistoryView(right_model, right_controller))