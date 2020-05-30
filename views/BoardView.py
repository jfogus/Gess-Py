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
        self.squares = [[SquareView() for _ in range(20)] for _ in range(20)]
        self.model = Board()

        # Setup layout
        layout = QGridLayout()
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        # Place initial stones and attach to the layout
        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                stone = self.model.get_squares()[i][j]

                if stone != "":
                    square.place_stone(stone)

                layout.addWidget(square, i, j)

        self.setLayout(layout)

    def handle_square_click(self):
        """ Updates the display of the board when a square is clicked. """
        pass

    def select_piece(self):
        """ Changes teh color of a cell and its peripheral cells
            indicating a piece on the board. """
        # TODO: Fill this in
        pass

    def deselect(self):
        """ Changes the color of a cell and its peripheral cells
            back to the default color. """
        # TODO: Fill this in
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
