# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  The view for a Gess Game Board.


from PySide2.QtWidgets import QGridLayout, QWidget
from views.SquareView import SquareView


class BoardView(QWidget):
    """ Creates a 20x20 grid of SquareViews. """
    def __init__(self, model, controller):
        super(BoardView, self).__init__()

        # Attach the model and controller
        self._board_model = model
        self._board_controller = controller

        # Setup the layout
        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        # Construct the view hierarchy
        model_squares = self._board_model.squares

        for i in range(model_squares):
            for j in range(model_squares[0]):
                self._squares[i][j] = SquareView((i, j))
                layout.addWidget(self._squares[i][j], i, j)

                # Connect click event to the controller
                self._squares[i][j].clicked.connect(self._baord_controller.handle_square_click)

        self.setLayout(layout)

        # Set up the initial state of the board
        self.update_squares()

        # Set up connection to model updates.
        self._board_model.piece_moved.connect(self.update_squares)
        self._board_model.piece_selected.connect(self.update_selection)

    @property
    def squares(self):
        """ Returns the squares"""
        return self._squares

    def update_squares(self):
        """ Updates the contents of the squares initially and
            when the model updates. """
        model_squares = self._board_model.squares

        for i in range(model_squares):
            for j in range(model_squares[0]):
                square_view = self._squares[i][j]
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
            self._squares[square[0], square[1]].highlight_as_peripheral()

    def clear_selection(self):
        """ Changes the color of all squares back to the default color. """
        for row in self._squares:
            for square_view in row:
                square_view.remove_highlight()


if __name__ == "__main__":
    pass
