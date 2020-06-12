# Author:  Joshua Fogus
# Date:  5/27/20
# Description:  Creates a board for the Gess Game which maintains all spaces,
#               testing and executing moves.


from PySide2.QtCore import Signal
from PySide2.QtCore import QObject


class Board(QObject):
    """ Represents a Gess game board.  Handles moving pieces,
     and checking for new rings. """
    piece_selected = Signal(dict)
    piece_deselected = Signal()

    def __init__(self):
        super(Board, self).__init__()
        # 20x20 matrix which includes gutters for 18x18 playable space
        self._squares = [['' for _ in range(20)] for _ in range(20)]
        self._selected = None

        # TODO: Move this to and load from a data file
        # There are 3 initial layouts for rows
        row_type_1 = [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17]
        row_type_2 = [1, 2, 3, 5, 7, 8, 9, 10, 12, 14, 16, 17, 18]
        row_type_3 = [2, 5, 8, 11, 14, 17]

        # TODO: Move this to and load from a data file
        # The layouts for rows by color
        white_rows = {1: row_type_1, 2: row_type_2, 3: row_type_1, 6: row_type_3}
        black_rows = {13: row_type_3, 16: row_type_1, 17: row_type_2, 18: row_type_1}

        # TODO: Move this to and load from a data file
        # Initial placement of stones on the board
        for row_num, row_type in black_rows.items():
            for col_num in row_type:
                self._squares[row_num][col_num] = 'b'
        for row_num, row_type in white_rows.items():
            for col_num in row_type:
                self._squares[row_num][col_num] = 'w'

    def get_squares(self):
        """ Has no parameters.  Returns the squares on the board in the
            form of a 20x20 matrix. """
        return self._squares

    def get_selected(self):
        """ Returns the currently selected piece. """
        return self._selected

    def set_selected(self, piece):
        """ Sets the currently selected piece. """
        self._selected = piece
        if self._selected is not None:
            # noinspection PyUnresolvedReferences
            self.piece_selected.emit(piece)
        else:
            # noinspection PyUnresolvedReferences
            self.piece_deselected.emit()

    def move_piece(self, origin_piece, target_piece):
        """ Moves the piece and updates the board if the move is legal. """
        # Move the origin piece to the destination, overwriting all stones
        self.remove_piece(origin_piece)
        self.place_piece(origin_piece, target_piece)

    def remove_piece(self, piece):
        """ Has 1 parameter, piece, in the form {(row, col}: stone}. Removes
            the stones from the board at the locations indicated by the
            piece. Returns nothing. """
        for location in piece.keys():
            self._squares[location[0]][location[1]] = ""

    def place_piece(self, origin_piece, target_piece=None):
        """ Has 2 parameters, pieces, in the form {(row, col): stone}.
            If only one argument given, places the stones in the locations of the
            single parameter. Places the stones from the source_piece into the
            locations of the target piece.  Returns nothing. """
        # Copies stones to its own locations if only one argument given
        if target_piece is None:
            target_piece = origin_piece

        # Get origin stones and target squares
        origin_stones = list(origin_piece.values())
        target_squares = list(target_piece.keys())

        # Place the source stone at the target location
        for i in range(len(origin_stones)):
            self._squares[target_squares[i][0]][target_squares[i][1]] = origin_stones[i]

    def clear_gutter(self):
        """ Has no parameters. Clears the gutters of stones. Returns nothing. """
        # The board is a square so any length is ok for rows and columns
        length = len(self._squares) - 1

        # Clear the first and last row and column
        for i in range(length):
            self._squares[0][i] = ""
            self._squares[i][0] = ""
            self._squares[length][i] = ""
            self._squares[i][length] = ""

    def check_for_rings(self):
        """ Has no parameters. Checks the entire board for any players rings.
            Returns a dictionary of rings in the form {(row, col}: stone}
            corresponding to the center of the ring. """
        rings = {}
        # Returns rings in the form {(center_row, center_col): color}
        # Only goes up to 18 to prevent list out of index
        for row_num in range(1, 18):
            for col_num in range(1, 18):
                stone = self._squares[row_num][col_num]
                if stone != "":
                    # Starts at the southwest corner and checks a "piece" for a ring
                    row_1 = self._squares[row_num][col_num:col_num + 3]
                    row_2 = self._squares[row_num + 1][col_num:col_num + 3]
                    row_3 = self._squares[row_num + 2][col_num:col_num + 3]

                    # Makes sure the stones form a ring and are all the same kind
                    if row_1 == [stone, stone, stone] and \
                            row_2 == [stone, "", stone] and \
                            row_3 == [stone, stone, stone]:
                        rings[row_num + 1, col_num + 1] = stone

        return rings


if __name__ == "__main__":
    pass
