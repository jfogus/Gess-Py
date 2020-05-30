# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  The view for the squares of the board.  Can fill with or empty
#               of a stone and change color indicating selection.


from PySide2.QtWidgets import QLabel
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPixmap, QMouseEvent


class SquareView(QLabel):
    """ Represents a square on a Gess board. """
    # TODO: Move stones from instance variable to class variable

    def __init__(self):
        super(SquareView, self).__init__()

        # Set default appearance
        self.setFixedSize(20, 20)
        # self.setFrameStyle(QFrame.Panel)
        self.setAlignment(Qt.AlignCenter)

        # Set styles
        # TODO: Factor styles into a separate file.
        # 00: default; 01: center; 10: peripheral
        self.styles = {
            "default": "border: 1px solid #A9A9A9;",
            "center": "border: 1px solid #221CD9;",
            "peripheral": "border: 1px solid #1BCF6C;"
        }

        self.setStyleSheet(self.styles["default"])

        # Load stone images
        self.stones = {
            'w': QPixmap("assets/white_circle.png"),
            'b': QPixmap("assets/black_circle.png")
        }

    def on_click(self):
        """ Emits a click event. """
        Signal("")

    def highlight_as_center(self):
        """ Changes the color of a cell to indicate it as the center
            of a piece. """
        self.setStyleSheet(self.styles["center"])

    def highlight_as_peripheral(self):
        """ Changes the color of a cell to indicate it as a peripheral
            member of a piece. """
        self.setStyleSheet(self.styles["peripheral"])

    def remove_highlight(self):
        """ Changes the color of the cell to its default color. """
        self.setStyleSheet(self.styles["default"])

    def place_stone(self, stone):
        """ Receives a string indicating what color stone to place.
            'b' or 'w' Places a stone with the corresponding color
             in the square. """
        self.setPixmap(self.stones[stone])

    def remove_stone(self):
        """ Clears the square of any stone. """
        self.setText("")


if __name__ == "__main__":
    pass
