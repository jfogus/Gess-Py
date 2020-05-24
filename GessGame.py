# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Creates an implementation of the Gess Game


class IllegalMove(Exception):
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
        self._turn = 0

    def get_game_state(self):
        """ Has no parameters. Returns the state of the game. For tracking if the
            game has been won. """
        return self._game_state

    def get_active_player(self):
        """ Has no parameters. Returns the active player. For tracking whose turn
            it is. """
        return self._players[self._turn]

    def resign_game(self):
        """ Has no parameters. Allows the active player to quit the game with a
            loss.  Updates a player and the game state. Returns nothing. """
        # Removes all rings from the current player
        self.get_active_player().resign()
        self.check_win_condition()

    def make_move(self, old_center, new_center):
        """ Has 2 parameters both in the form of a letter and number.  The first
            corresponds to the center square of the originating piece, the second
            corresponds to the desired location of the originating piece. Moves
            a piece to a new square.  Returns True if the move was completed.
            Returns False if the move was unable to be completed. """
        if self._game_state != 'UNFINISHED':
            return False

        # Get the active player
        active_player = self._players[self._turn]

        # Make the move if legal; does not check if destroyed last ring
        try:
            move = self._board.move_piece(active_player, old_center, new_center)
        except IllegalMove:
            # The move was illegal for one of various reasons
            return False

        # Ensure active player still has a ring, otherwise undo the move
        self.update_rings()
        if not active_player.has_rings():
            self._board.reverse_move(move)
            self.update_rings()

        self.check_win_condition()
        self.switch_turn()

        self._board.print_board()

        return True

    def update_rings(self):
        """ Has no parameters. Checks the playable board spaces for any rings
            and updates the players lists of rings accordingly. Returns nothing. """
        rings = self._board.check_for_rings()

        black_rings = []
        white_rings = []

        for pos, color in rings.items():
            if color == 'b':
                black_rings.append(pos)
            elif color == 'w':
                white_rings.append(pos)

        for player in self._players:
            if player.get_color() == 'b':
                player.set_rings(black_rings)
            elif player.get_color() == 'w':
                player.set_rings(white_rings)

    def switch_turn(self):
        """ Has no parameters. Switches the active player to facilitate taking
            turns. Returns nothing. """
        self._turn ^= 1

    def check_win_condition(self):
        """ Has no parameters. Checks if a player is without rings and updates the status of the game. """
        for i, player in enumerate(self._players):
            # The player has no rings
            if not player.has_rings():
                # Get the color of the opposite player and create the state message
                state = self._players[i ^ 1].get_long_form_color() + "_WON"
                self._game_state = state


class Board:
    """ Represents a Gess game board.  Handles confirming legal moves, moving pieces,
     and checking for new rings. """

    def __init__(self):
        # 20x20 matrix which includes gutters for 18x18 playable space
        self._spaces = [['' for _ in range(20)] for _ in range(20)]

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
                self._spaces[row_num][col_num] = 'b'
        for row_num, row_type in white_rows.items():
            for col_num in row_type:
                self._spaces[row_num][col_num] = 'w'

    def get_board_spaces(self):
        return self._spaces

    def move_piece(self, player, old_center, new_center):
        """ Moves the piece and updates the board if the move is legal. """
        # Convert human readable position into a list of indices
        old_center = self.convert_position_to_indices(old_center)
        new_center = self.convert_position_to_indices(new_center)

        # An old center in the gutter results in an illegal move
        last_row = len(self._spaces)
        if old_center[0] in (0, last_row) or old_center[1] in (0, last_row):
            raise IllegalMove

        # A new center in the gutter results in an illegal move
        if new_center[0] in (0, last_row) or old_center[1] in (0, last_row):
            raise IllegalMove

        # Get spaces moved in the form [rows, columns]
        move = [new_center[0] - old_center[0], new_center[1] - old_center[1]]

        # Get pieces from indices of center square; sorted to ensure consistency
        old_piece = self.get_piece_from_center(old_center)
        new_piece = self.get_piece_from_center(new_center)

        # Check if move is legal in various ways
        if not self.is_legal_move(player, old_piece, new_piece):
            raise IllegalMove

        # Get the old piece and new piece each in the form {(row, col): stone} for returning
        old_squares = {}
        new_squares = {}

        # Get stones of the pieces
        old_stones = [self._spaces[row][col] for row, col in old_piece]
        new_stones = [self._spaces[row][col] for row, col in new_piece]

        # Populate old_squares and new_squares
        for i, space in enumerate(old_piece):
            old_squares[space[0]][space[1]] = old_stones[i]

        for i, space in enumerate(new_piece):
            new_squares[space[0]][space[1]] = new_stones[i]

        # Remove captured stones and move the piece
        old_piece = self.remove_piece(old_piece)
        self.place_piece(old_piece, move)

        # Remove gutter stones
        self.clear_gutter()

        # Returns the old piece
        return old_squares, new_squares

    def reverse_move(self, moves):
        """ Replaces the stones from a move that had been made. """
        for move in moves:
            for pos, stone in move.items():
                self._spaces[pos[0]][pos[1]] = stone

    def remove_piece(self, squares):
        """ Removes a piece from the board and returns it. """
        piece = {}

        for square in squares:
            # Creates a dictionary with tuple keys identifying board location
            # and value of the stone at that location
            piece[square[0], square[1]] = self._spaces[square[0]][square[1]]
            self._spaces[square[0]][square[1]] = ""

        return piece

    def place_piece(self, squares, move):
        """ Places a piece on the board. """
        for location, stone in squares.items():
            new_space = location[0] + move[0], location[1] + move[1]
            self._spaces[new_space[0]][new_space[1]] = stone

    def clear_gutter(self):
        """ Clears the gutters of stones. """
        # The board is a square so any length is ok for rows and columns
        length = len(self._spaces) - 1

        # Clear the first and last row and column
        for i in range(length):
            self._spaces[0][i] = ""
            self._spaces[i][0] = ""
            self._spaces[length][i] = ""
            self._spaces[i][length] = ""

    def check_for_rings(self):
        rings = {}
        # Returns rings in the form {(center_row, center_col): color}
        for row_num in range(1, 20):
            for col_num in range(1, 20):
                stone = self._spaces[row_num][col_num]
                if stone != "":
                    row_1 = self._spaces[row_num][col_num:col_num + 3]
                    row_2 = self._spaces[row_num + 1][col_num:col_num + 3]
                    row_3 = self._spaces[row_num + 2][col_num:col_num + 3]

                    if row_1 == [stone, stone, stone] and \
                            row_2 == [stone, "", stone] and \
                            row_3 == [stone, stone, stone]:
                        rings[row_num + 1, col_num + 1] = stone

        return rings

    def print_board(self):
        """ Prints the board. """
        # Reverse order for user understanding
        for i in range(len(self._spaces) - 1, -1, -1):
            # Print cell divider
            print("|", end="")

            for j in range(len(self._spaces)):
                # Empty cells printed as spaces to prevent collapse
                if self._spaces[i][j] == "":
                    print(" ", end="|")
                else:
                    # Print stone in the cell
                    print(self._spaces[i][j], end="|")

            # print row numbers
            print(i + 1)

        # print column letters with a space prior for alignment
        print(" ", end="")
        for i in range(20):
            print(chr(ord('a') + i), end=" ")

        print("\n")

    def is_legal_move(self, player, old_piece, new_piece):
        """ Returns true if the move from the old center to the new center is a legal move. """
        # Check if the piece only contains a single color or if no stones
        piece_color = self.get_single_color_piece(old_piece)
        if piece_color is None:
            return False

        # Check if the color of the piece is the appropriate color's turn
        color = player.get_color()
        if piece_color != color:
            return False

        # In the flag matrix of the piece, 4 is the index of the center
        old_center = old_piece[4]
        new_center = new_piece[4]

        # Check if the move is in a legal direction
        direction = self.get_valid_move(old_center, new_center)

        if direction is None:
            return False

        # Check if the piece can move in the desired direction
        direction_stone = old_center[0] + direction[0], old_center[1] + direction[1]
        center_stone = self._spaces[old_center[0]][old_center[1]]

        if not self._spaces[direction_stone[0]][direction_stone[1]] == color:
            return False

        # Check if the piece can move the desired distance
        # Any nonzero distance is sufficient since movement is only in 8 directions
        if old_center[0] != new_center[0]:
            distance = new_center[0] - old_center[0]
        else:
            distance = new_center[1] - old_center[1]

        if not (center_stone == color or abs(distance) <= 3):
            return False

        # Simulate the movement of the piece, one square at a time to check premature overlap
        for delta in range(distance):
            # Checks moved squares up to but not including the final movement
            movement = delta * direction[0], delta * direction[1]

            for square in old_piece:
                # Look at each square of movement to see if there is premature overlap
                delta_square = square[0] + movement[0], square[1] + movement[1]
                stone = self._spaces[delta_square[0]][delta_square[1]]

                # Make sure there is not another stone in the path of the move
                if delta_square not in old_piece and stone != color and stone != "":
                    return False

        return True

    @staticmethod
    def get_valid_move(old_center, new_center):
        """ Returns the offset from center of the piece's determining square or None if invalid. """
        vertical_move = new_center[0] - old_center[0]
        horizontal_move = new_center[1] - old_center[1]

        # North is - direction, South is + direction
        offset = None

        if vertical_move == 0 and horizontal_move > 0:
            # Eastward move
            offset = 0, 1

        elif vertical_move == 0 and horizontal_move < 0:
            # Westward move
            offset = 0, -1

        elif vertical_move > 0 and horizontal_move == 0:
            # Northward move
            offset = 1, 0

        elif vertical_move < 0 and horizontal_move == 0:
            # Southward move
            offset = -1, 0

        elif vertical_move > 0 and vertical_move == horizontal_move:
            # Northeasterly move
            offset = 1, 1

        elif vertical_move < 0 and vertical_move == horizontal_move:
            # Southwesterly move
            offset = -1, -1

        elif vertical_move > 0 and (vertical_move + horizontal_move) == 0:
            # Northwesterly move
            offset = 1, -1

        elif vertical_move < 0 and (vertical_move + horizontal_move) == 0:
            # Southeasterly move
            offset = -1, 1

        return offset

    def get_single_color_piece(self, squares):
        """ Gets the single color in a piece, None if multiple colors"""
        color = None

        for square in squares:
            stone = self._spaces[square[0]][square[1]]

            if stone != "" and color is None:
                # Gets the color of the stone
                color = stone
            elif stone != "" and stone != color:
                # There are two color stones in the piece
                return None

        return color

    @staticmethod
    def convert_position_to_indices(position):
        """ Converts a position in letter/number format to indices. """
        row = int(position[1:]) - 1

        # Get the row and column number; the offset from A is the row number
        col_letter = position[0].upper()
        col = ord(col_letter) - ord('A')

        return row, col

    @staticmethod
    def get_piece_from_center(center):
        """ Gets the set of 9 squares corresponding to the center square as a list of tuples. """
        sw_corner = center[0] - 1, center[1] - 1

        # row + (0 to 3), col + (0 to 3)
        return sorted([(sw_corner[0] + i, sw_corner[1] + j) for j in range(3) for i in range(3)])


class Player:
    """ Represents a player of the Gess game.  Maintains and updates a personal
     list of rings and its own color. """

    def __init__(self, color):
        self._color = color
        self._rings = []
        self._long_form_color = ""

        # Sets the initial rings and long form color for each player
        if color == "b":
            self._rings.append((2, 11))
            self._long_form_color = "BLACK"
        elif color == "w":
            self._rings.append((17, 11))
            self._long_form_color = "WHITE"

    def get_color(self):
        """ Returns the player's color as a char. """
        return self._color

    def get_long_form_color(self):
        """ Gets a long text form of the player's color. """
        return self._long_form_color

    def get_rings(self):
        """ Returns the locations of the centers of players rings. """
        return self._rings

    def has_rings(self):
        """ Returns true if the player has any rings. """
        if len(self._rings) > 0:
            return True

        return False

    def set_rings(self, rings):
        """ Replaces the previous list of rings with a new list of rings. """
        self._rings = rings

    def resign(self):
        """ Removes all of the players rings. """
        self._rings = []


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
