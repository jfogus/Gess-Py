# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  The view for a Gess Game Board.


from PySide2.QtWidgets import QGridLayout, QWidget, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from views.SquareView import SquareView


class BoardView(QWidget):
    """ Creates a 20x20 grid of SquareViews. """
    def __init__(self, squares, model, controller):
        super(BoardView, self).__init__()

        # Attach the model and controller
        self._game = model
        self._board = model.get_board()
        self._controller = controller
        self._squares = squares

        # Setup the layout
        layout = QGridLayout()
        layout.setHorizontalSpacing(2)
        layout.setVerticalSpacing(2)

        # Add squares to the layout
        self._board_size = len(self._squares)

        for i in range(self._board_size):
            # Row labels; row numbers decreasing
            row_label = self.create_label(str(self._board_size - i))
            row_label.setAlignment(Qt.AlignRight)
            row_label.setContentsMargins(10, 0, 5, 0)
            layout.addWidget(row_label, i, 0)

            for j in range(self._board_size):
                layout.addWidget(self._squares[i][j], i, j + 1)

                # Connect click event to the controller
                self._squares[i][j].clicked.connect(self._controller.handle_square_click)

        # Column labels
        for i in range(20):
            # ASCII code for 'a' + an offset
            col_label = self.create_label(chr(i + 97))
            col_label.setContentsMargins(0, 0, 0, 10)
            col_label.setAlignment(Qt.AlignHCenter)
            layout.addWidget(col_label, self._board_size, i + 1)

        self.setLayout(layout)

        # Set up the initial state of the board
        self.update_squares()

        # Set up connection to model updates.
        self._game.board_updated.connect(self.update_squares)
        self._board.piece_selected.connect(self.update_selection)
        self._board.piece_deselected.connect(self.clear_selection)

    def get_squares(self):
        """ Returns the squares"""
        return self._squares

    @staticmethod
    def create_label(text):
        """ Returns a QLabel with the passed string. """
        label = QLabel()
        label.setText(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12))

        return label

    def update_squares(self):
        """ Updates the contents of the squares initially and
            when the model updates. """
        model_squares = self._board.get_squares()

        for i in range(self._board_size):
            for j in range(self._board_size):
                square_view = self._squares[i][j]
                # Flips the board so black is at the bottom
                stone = model_squares[i][j]

                # Place the piece in squares
                if stone != "":
                    square_view.place_stone(stone)

                # Clear empty squares
                if stone == "":
                    square_view.remove_stone()

        # Piece is moved; remove selection indicator
        self.clear_selection()

    def update_selection(self, piece):
        """ Updates the appearance of squares when a piece has been selected.
            Piece is a dictionary in the form {(row, col): stone} """
        for square, stone in zip(piece.keys(), piece.values()):
            self._squares[square[0]][square[1]].highlight_as_peripheral()

    def clear_selection(self):
        """ Changes the color of all squares back to the default color. """
        for row in self._squares:
            for square_view in row:
                square_view.remove_highlight()


if __name__ == "__main__":
    pass
