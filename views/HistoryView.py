# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Creates a view which displays the games completed moves.


from PySide2.QtWidgets import (QDockWidget, QGridLayout,
                               QVBoxLayout, QLabel, QWidget)
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt, QSize


# TODO: At the end of the game, it should show a button to save the history
class HistoryView(QDockWidget):
    """ Displays the history of moves in the game. """
    def __init__(self, model, controller):
        super(HistoryView, self).__init__()

        self.setFixedWidth(175)

        self._history = model
        self._controller = controller

        # Set up container
        layout = QGridLayout()

        container = QWidget()
        container.setLayout(layout)

        self.setTitleBarWidget(QWidget())

        # Add title
        title = QLabel()
        title.setText("Notation")
        title.setFont(QFont("Arial", 14))
        title.setAlignment(Qt.AlignHCenter)
        title.setContentsMargins(5, 0, 10, 0)

        # Setup the title section
        layout.addWidget(title, 0, 0, 1, 3)
        layout.setAlignment(Qt.AlignTop)

        self.setWidget(container)

        self._history.move_added.connect(self.add_move)

    def add_move(self, origin, destination):
        """ Responds to the updated model; adds a move to the history list. """
        origin = self.piece_to_indices(origin)
        destination = self.piece_to_indices(destination)
        container = self.widget().layout()
        rows = container.rowCount()

        # TODO: Add new columns when notation goes past ~ 20 rows
        #       with pagination

        # Create the move notation
        move = QLabel()
        move.setFixedHeight(16)
        move.setText(origin + " - " + destination)

        # Add the notation to the correct cell
        if len(self._history.get_history()) % 2 != 0:
            count = QLabel(str(rows) + ".")
            count.setFixedWidth(15)
            container.addWidget(count, rows, 0)

            container.addWidget(move, rows, 1)
        else:
            container.addWidget(move, rows - 1, 2)

    @staticmethod
    def piece_to_indices(piece):
        """ Converts a piece in the form {(row, col): stone} to a letter, number
            combination, indicating a center square on the board. """
        # TODO: Add this and others like it to a utility module
        center = list(piece.keys())[4]

        # Convert to lower case column letter and row number
        col = chr(center[1] + 97)
        row = 20 - center[0]

        return col + str(row)