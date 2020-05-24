# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Creates an implementation of the Gess Game


class IllegalMove(Exception):
    """ Represents an illegal move in the Gess Game. """
    pass


class GessGame:
    """ Represents a game of Gess.  Maintains game state, tracks turn,
        maintains players and updates them.  Allows for making a move and resigning.
        Will have a Board object for communicating player input to the Board.  Will have
        2 Player objects for updating and checking their list of rings. Has no parameters. """

    def __init__(self):
        self._board = Board()
        self._game_state = 'UNFINISHED'
        self._players = (Player('b'), Player('w'))
        self._active = 0

    def get_game_state(self):
        """ Has no parameters. Returns the state of the game. For tracking if the
            game has been won. """
        return self._game_state

    def get_active_player(self):
        """ Has no parameters. Returns the active player. For tracking whose turn
            it is. """
        return self._players[self._active]

    def resign_game(self):
        """ Has no parameters. Allows the active player to quit the game with a
            loss.  Updates a player and the game state. Returns nothing. """
        # Removes all rings from the current player
        self.get_active_player().set_rings([])
        self.check_win_condition()

    def make_move(self, origin_square, target_square):
        """ Has 2 parameters both in the form of a letter and number.  The first
            corresponds to the center square of the originating piece, the second
            corresponds to the desired location of the originating piece. Moves
            a piece to a new square.  Returns True if the move was completed.
            Returns False if the move was unable to be completed. """
        if self._game_state != 'UNFINISHED':
            return False

        # Get the active player
        active_player = self._players[self._active]

        # Make the move if legal; return False otherwise; does not check if destroyed last ring
        try:
            moves = self._board.move_piece(active_player, origin_square, target_square)
        except IllegalMove:
            # The move was illegal for one of various reasons
            return False

        # Ensure active player did not destroy their last ring; undo the move and return False otherwise
        try:
            self.update_rings()
        except IllegalMove:
            # Reverse the move
            for move in moves:
                self._board.place_piece(move)
            return False

        self.check_win_condition()
        self.switch_turn()

        self._board.print_board()

        return True

    def update_rings(self):
        """ Has no parameters. Requests all rings from the Board object and updates
            the players lists of rings accordingly. Raises an error if the active
            player is attempting to destroy their last ring. Returns nothing. """
        rings = self._board.check_for_rings()

        active_rings = [pos for pos, stone in rings.items() if stone == self.get_active_player().get_stone()]
        inactive_rings = [pos for pos, stone in rings.items() if stone != self.get_active_player().get_stone()]

        # Prevent the active player from destroying their last rings
        if len(active_rings) == 0:
            raise IllegalMove

        self.get_active_player().set_rings(active_rings)
        self._players[self._active ^ 1].set_rings(inactive_rings)

    def switch_turn(self):
        """ Has no parameters. Switches the active player to facilitate taking
            turns. Returns nothing. """
        self._active ^= 1

    def check_win_condition(self):
        """ Has no parameters. Checks if a player is without rings and updates the status of the game. """
        for i, player in enumerate(self._players):
            # The player has no rings
            if not player.has_rings():
                # Get the color of the opposite player and create the state message
                state = self._players[i ^ 1].get_color() + "_WON"
                self._game_state = state


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

    def get_board_spaces(self):
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
        self.place_piece(origin_piece, target_piece)

        # Remove gutter stones
        self.clear_gutter()

        # Returns the pieces prior to change
        return origin_piece, target_piece

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
        origin_stones = origin_piece.values
        target_squares = target_piece.keys()

        # Place the source stone at the target location
        for i in range(len(origin_stones)):
            self._squares[target_squares[i][0]][target_squares[i][1]] = origin_stones[i]

    def in_gutter(self, square):
        """ Has one parameter, a square, in the form of (row, col).  Determines
            if the square is in the gutter around the edges of the board.
            Returns True if it is in the gutter, returns False otherwise. """
        gutter_indices = (0, len(self._squares))

        # Check if row is in in a gutter row or column is in a gutter column
        if square[0] in gutter_indices or square[1] in gutter_indices:
            return True

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
        for row_num, col_num in zip(range(1, 20), range(1, 20)):
            stone = self._squares[row_num][col_num]
            if stone != "":
                row_1 = self._squares[row_num][col_num:col_num + 3]
                row_2 = self._squares[row_num + 1][col_num:col_num + 3]
                row_3 = self._squares[row_num + 2][col_num:col_num + 3]

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
        if stone_set != {player_stone} or stone_set != {player_stone, ""}:
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

        stones = piece.values()
        # Check if the move direction is legal for the piece
        if delta[0] == 0 and delta[1] > 0 and stones[5] == '':
            # Eastward move
            return False

        if delta[0] == 0 and delta[1] < 0 and stones[3] == '':
            # Westward move
            return False

        if delta[0] > 0 and delta[1] == 0 and stones[1] == '':
            # Northward move
            return False

        if delta[0] < 0 and delta[1] == 0 and stones[7] == '':
            # Southward move
            return False

        if delta[0] > 0 and delta[0] == delta[1] and stones[2] == '':
            # Northeasterly move
            return False

        if delta[0] < 0 and delta[0] == delta[1] and stones[6] == '':
            # Southwesterly move
            return False

        if delta[0] > 0 and (delta[0] + delta[1]) == 0 and stones[0] == '':
            # Northwesterly move
            return False

        if delta[0] < 0 and (delta[0] + delta[1]) == 0 and stones[8] == '':
            # Southeasterly move
            return False

        # The piece can move in the given direction
        return True

    def is_legal_distance(self, piece, delta):
        """ Has 2 parameters, piece and delta, a dictionary in the form
            {(row, col): stone} corresponding to a 3x3 square and a tuple of the
            amount of change in rows and columns in the form (row_delta, col_delta).
            Returns True if the move is a legal distance, returns False otherwise. """
        stones = piece.values()
        locations = piece.keys()
        # Only 8 directions are allowed, the absolute value of any direction is the spaces moved
        distance = abs(delta[0])

        # stones[4] is the center stone;
        if not (stones[4] != '' or distance <= 3):
            return False

        # Get the start and step direction for the range
        row_mod = 1
        col_mod = 1
        if delta[0] < 0:
            row_mod = -1
        if delta[1] < 0:
            col_mod = -1

        # Simulate the movement of the piece, one square at a time to check premature overlap
        # I learned how to iterate over two lists from SO:
        # https://stackoverflow.com/questions/1663807/how-to-iterate-through-two-lists-in-parallel
        # The idea to do it and how it applies is my own.
        for row_delta, col_delta in zip(range(row_mod, delta[0], step=row_mod), range(col_mod, delta[1], step=col_mod)):
            # Checks moved squares up to but not including the final movement
            for location in locations:
                row = location[0] + row_delta
                col = location[1] + col_delta
                stone = self._squares[row][col]
                if (row, col) not in locations and stone != '':
                    # The square is not in the origin piece, the move
                    # is not the last move, and the square has a stone.
                    return False

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


class Player:
    """ Represents a player of the Gess game. Has no knowledge of any other classes.
        Maintains, updates, and provides information on its own list of rings, its
        stone marker, and its own color. Has one parameters, a stone, in the form
        of a character, either 'w' or 'b' """

    def __init__(self, stone):
        self._stone = stone
        self._color = ""
        self._rings = []

        # Sets the initial rings and color for each player
        if stone == "b":
            self._rings.append((2, 11))
            self._color = "BLACK"
        elif stone == "w":
            self._rings.append((17, 11))
            self._color = "WHITE"

    def get_stone(self):
        """ Has no parameters. Returns the player's stone as a string: 'w' or 'b' """
        return self._stone

    def get_color(self):
        """ Has no parameters. Returns the player's color as a string:
            "WHITE" or "BLACK" """
        return self._color

    def get_rings(self):
        """ Has no parameters. Returns a list of tuples indicating the locations of
            the centers of the player's rings in (row, col) format. """
        return self._rings

    def set_rings(self, rings):
        """ Receives a list of tuples indicating the locations of the centers of
            the player's rings in (row, col) format. Entirely replaces the previous
            list of rings with the new list of rings.  Returns nothing. """
        self._rings = rings

    def has_rings(self):
        """ Has no parameters. Returns True if the player has at least one ring,
            otherwise returns False. """
        if len(self._rings) > 0:
            return True

        return False


def main():
    """ This is not meant to be run as a script. Performs simple tests. """
    b = Board()
    p = Player('b')
    b.print_board()
    b.move_piece(p, 'r4', 'p4')
    b.print_board()


if __name__ == '__main__':
    main()

# Board 18 x 18
# Players x2 (b/w)
# each player 43 stones
# pieces (3x3 squares that contain stones of one color)
#  - A piece can extend outside of the board, center must be on the board
# black goes first, turns taken
# The whole piece (all stones w/in) moves as a unit
#  - If stone in center of piece
#    - piece can move any unobstructed distance
#  - If center is empty
#    - Can move <= 3 squares
#  - Regardless of center piece
#    - direction is limited by stones on the perimeter
#    - diagonal is included in directions movable
#  - Movement is halted as soon as the footprint overlaps any other stones (regardless of color)
#    - Overlapped stones of both colors are removed permanently from the game
#  - A piece may move partially beyond the board in which case any stones out of bounds are eliminated
# Footprint of a piece is its 3x3 region (not just where the stones are)
# Pieces are defined by their central square
# The goal is to eliminate the opponent's last ring
#  - A ring is a ring of eight stones around an empty center
#  - Each player starts w/ 1 ring but may make more
# Cannot make a move that breaks your own last ring
