# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  The view for a Gess Game Board.


import sys
from PySide2.QtWidgets import QApplication, QGridLayout, QWidget
from models.Board import Board
from views.SquareView import SquareView


class BoardView(QWidget):
    def __init__(self):
        super(BoardView, self).__init__()

        # Attach model
        self.squares = [[SquareView((i, j)) for j in range(20)] for i in range(20)]
        self.model = Board()

        # Will be updated with a tuple indicating the center of a piece.
        self._selected = None
        self._movable_spaces = None

        # Setup layout
        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        # Place initial stones and attach to the layout
        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                stone = self.model.get_squares()[i][j]

                # Attach click handler
                square.clicked.connect(self.handle_square_click)

                if stone != "":
                    square.place_stone(stone)

                layout.addWidget(square, i, j)

        self.setLayout(layout)

    def handle_square_click(self, coords):
        """ Updates the display of the board when a square is clicked. """
        # If no piece is selected, select the piece
        if self._selected is None:
            self.select_piece(coords)
        # If selected and coords is the selected square, deselect the piece
        elif self._selected == coords:
            self.clear_selection()
        elif None not in (self._selected, self._movable_spaces):
            if coords in self._movable_spaces:
                # If selected and coords in movable space, move the piece
                self.move_piece()
            else:
                # If selected and coords not in movable space, error
                self.handle_illegal_move()

    def select_piece(self, center):
        """ Changes the color of a cell and its peripheral cells
            indicating a piece on the board. """
        self._selected = center
        # Loops over the piece from the SW corner
        for i in range(-1, 2):
            for j in range(-1, 2):
                square = self.squares[center[0] + i][center[1] + j]
                if (i, j) == (0, 0):
                    square.highlight_as_center()
                else:
                    square.highlight_as_peripheral()

        # TODO: Check settings for if guides should be shown
        self.show_guides()

    def show_guides(self):
        """ Highlights all legal moves. """
        # TODO: Fill this in.
        pass

    def clear_selection(self):
        """ Changes the color of all squares back to the default color. """
        self._selected = None
        self._movable_spaces = None

        for row in self.squares:
            for square in row:
                square.remove_highlight()

    def move_piece(self):
        """ Move the piece from the previously selected square to
            the newly selected square. """
        # TODO: Fill this in.
        pass

    def handle_illegal_move(self):
        """ Handles an illegal move. """
        pass


def main():
    """ Not meant to be run as a script. Performs a simple test. """
    app = QApplication(sys.argv)

    widget = BoardView()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
