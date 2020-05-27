# Author:  Joshua Fogus
# Date:  5/27/20
# Description:  Creates a board for the Gess Game which maintains all spaces,
#               testing and executing moves.


from models.IllegalMove import IllegalMove


class Board:
    """ Represents a Gess game board.  Handles confirming legal moves, moving pieces,
     and checking for new rings. """

    def __init__(self):
        # 20x20 matrix which includes gutters for 18x18 playable space
        self._squares = [['' for _ in range(20)] for _ in range(20)]

        # There are 3 initial layouts for rows
        row_type_1 = [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17]
        row_type_2 = [1, 2, 3, 5, 7, 8, 9, 10, 12, 14, 16, 17, 18]
        row_type_3 = [2, 5, 8, 11, 14, 17]

        # The layouts for rows by color
        black_rows = {1: row_type_1, 2: row_type_2, 3: row_type_1, 6: row_type_3}
        white_rows = {13: row_type_3, 16: row_type_1, 17: row_type_2, 18: row_type_1}

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

    def move_piece(self, player, origin_square, target_square):
        """ Moves the piece and updates the board if the move is legal. """
        # Convert human readable position into a tuple of indices
        origin_square = self.to_indices(origin_square)
        target_square = self.to_indices(target_square)

        # An center of origin or target is in the gutter results in an illegal move
        if self.in_gutter(origin_square) or self.in_gutter(target_square):
            raise IllegalMove

        # Get the change per square from origin to target
        delta = self.get_delta(origin_square, target_square)

        # Get pieces from indices of center square; sorted to ensure consistency
        origin_piece = self.get_piece(origin_square)
        target_piece = self.get_piece(target_square)

        # Check if the piece belongs to the player
        if not self.is_player_piece(player, origin_piece):
            raise IllegalMove

        # Check if the piece can move in the desired direction
        if not self.is_legal_direction(origin_piece, delta):
            raise IllegalMove

        # Check if the piece can move the desired distance
        if not self.is_legal_distance(origin_piece, delta):
            raise IllegalMove

        # Move the origin piece to the destination, overwriting all stones
        self.remove_piece(origin_piece)
        self.place_piece(origin_piece, target_piece)

        # Remove gutter stones
        self.clear_gutter()

        # Returns the pieces prior to change
        return origin_piece, target_piece

    def remove_piece(self, piece):
        """ Has 1 parameter, piece, in the form {(row, col}: stone}. Removes
            the stones from the board at the locations indicated by the
            piece. Returns nothing. """
        for location in piece.keys():
            self._squares[location[0]][location[1]] = ""

    @staticmethod
    def get_delta(origin_square, target_square):
        """ Has 2 parameters, squares, in the form (row, col).  Calculates
            the number of rows and columns moved.  Returns target - origin
            as a tuple in the form (delta_row, delta_col). """
        return target_square[0] - origin_square[0], target_square[1] - origin_square[1]

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

    def in_gutter(self, square):
        """ Has one parameter, a square, in the form of (row, col).  Determines
            if the square is in the gutter around the edges of the board.
            Returns True if it is in the gutter, returns False otherwise. """
        gutter_indices = (0, len(self._squares) - 1)

        # Check if row is in in a gutter row or column is in a gutter column
        if square[0] in gutter_indices or square[1] in gutter_indices:
            return True

        return False

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

    def print_board(self):
        """ Has no parameters. Prints the board to the console in an
            easily readable format. Returns nothing. """
        # Reverse order for user understanding
        for i in range(len(self._squares) - 1, -1, -1):
            # Print cell divider
            print("|", end="")

            for j in range(len(self._squares)):
                # Empty cells printed as spaces to prevent collapse
                if self._squares[i][j] == "":
                    print(" ", end="|")
                else:
                    # Print stone in the cell
                    print(self._squares[i][j], end="|")

            # print row numbers
            print(i + 1)

        # print column letters with a space prior for alignment
        print(" ", end="")
        for i in range(20):
            print(chr(ord('a') + i), end=" ")

        print("\n")

    @staticmethod
    def is_player_piece(player, piece):
        """ Has 2 parameters, player and piece, in the form of a Player object
            and a dictionary in the form {(row, col): stone} corresponding to
            a 3x3 square. Returns True if all stones in the piece belong to
            player and False otherwise. """
        player_stone = player.get_stone()
        stone_set = set(piece.values())

        # Check stones in the piece for unowned stones or an empty piece
        if not(stone_set == {player_stone} or stone_set == {player_stone, ''}):
            return False

        # The piece belongs to player
        return True

    @staticmethod
    def is_legal_direction(piece, delta):
        """ Has 2 parameters, piece and delta, a dictionary in the form
        {(row, col): stone} corresponding to a 3x3 square and a tuple of the
        amount of change in rows and columns in the form (row_delta, col_delta).
        Returns True if the move is in a legal direction, returns False otherwise."""
        # Check if the move direction is generally legal
        if not (delta[0] == 0 or delta[1] == 0 or abs(delta[0]) == abs(delta[1])):
            # Not horizontal, vertical, or diagonal
            return False

        # Check if no move direction.
        if delta[0] == 0 and delta[1] == 0:
            return False

        stones = list(piece.values())

        # Check if the move direction is legal for the piece
        if delta[0] == 0 and delta[1] > 0 and stones[5] == '':
            # Eastward move
            return False

        if delta[0] == 0 and delta[1] < 0 and stones[3] == '':
            # Westward move
            return False

        if delta[0] > 0 and delta[1] == 0 and stones[7] == '':
            # Northward move
            return False

        if delta[0] < 0 and delta[1] == 0 and stones[1] == '':
            # Southward move
            return False

        if delta[0] > 0 and delta[0] == delta[1] and stones[8] == '':
            # Northeasterly move
            return False

        if delta[0] < 0 and delta[0] == delta[1] and stones[0] == '':
            # Southwesterly move
            return False

        if delta[0] > 0 and (delta[0] + delta[1]) == 0 and stones[6] == '':
            # Northwesterly move
            return False

        if delta[0] < 0 and (delta[0] + delta[1]) == 0 and stones[2] == '':
            # Southeasterly move
            return False

        # The piece can move in the given direction
        return True

    def is_legal_distance(self, piece, delta):
        """ Has 2 parameters, piece and delta, a dictionary in the form
            {(row, col): stone} corresponding to a 3x3 square and a tuple of the
            amount of change in rows and columns in the form (row_delta, col_delta).
            Returns True if the move is a legal distance, returns False otherwise. """
        stones = list(piece.values())
        locations = list(piece.keys())
        # Only 8 directions are allowed, the absolute value of any direction is the spaces moved
        distance = abs(delta[0])

        # stones[4] is the center stone;
        if not (stones[4] != '' or distance <= 3):
            return False

        # Get the series of steps taken to get to the full move
        if delta[0] > 0:
            row_steps = range(1, delta[0])
        elif delta[0] < 0:
            row_steps = range(-1, delta[0], -1)
        else:
            row_steps = [0 for _ in range(abs(delta[1]))]

        if delta[1] > 0:
            col_steps = range(1, delta[1])
        elif delta[1] < 0:
            col_steps = range(-1, delta[1], -1)
        else:
            col_steps = [0 for _ in range(abs(delta[0]))]

        # Simulate the movement of the piece, one square at a time to check premature overlap
        # I learned how to iterate over two lists from SO:
        # https://stackoverflow.com/questions/1663807/how-to-iterate-through-two-lists-in-parallel
        # The idea to do it and how it applies is my own.
        for row_delta, col_delta in zip(row_steps, col_steps):
            # Checks moved squares up to but not including the final movement
            for location in locations:
                row = location[0] + row_delta
                col = location[1] + col_delta
                stone = self._squares[row][col]
                if (row, col) not in locations and stone != '':
                    # The square is not in the origin piece, the move
                    # is not the last move, and the square has a stone.
                    return False

        return True

    @staticmethod
    def to_indices(position):
        """ Static method. Has 1 parameter in the form of a string. The string
            must be a letter followed by a number. Converts a position in
            letter/number format to indices corresponding to the board's
            squares. Returns the indices in the form (row, col). """
        row = int(position[1:]) - 1

        # Get the row and column number; the offset from A is the row number
        col_letter = position[0].upper()
        col = ord(col_letter) - ord('A')

        return row, col

    def get_piece(self, square):
        """ Has 1 parameter, a square, in the form of (row, col). Collects with it
            the surrounding 8 squares.  Returns all 9 squares as a dictionary in
            the form {(row, col): stone} """
        # Get the SW corner of the 3x3 square.
        sw_corner = square[0] - 1, square[1] - 1

        # Get a 3x3 dictionary of the coordinates of squares and their stones
        piece = {}
        for row in range(3):
            for col in range(3):
                # Position on the board
                square = sw_corner[0] + row, sw_corner[1] + col
                piece[square[0], square[1]] = self._squares[square[0]][square[1]]

        # Sorted to ensure consistency in use
        return piece


def main():
    """ Not meant to be run as a script. Performs a simple test. """
    b = Board()
    piece = b.get_piece((2, 2))
    print("Piece at C3:", str(piece))


if __name__ == "__main__":
    main()
