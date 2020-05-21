# Author:  Joshua Fogus
# Date:  4/30/20
# Description:  Creates an implementation of the Gess Game


class GessGame:
    """ Represents a game of Gess.  Contains main game logic. """
    def __init__(self):
        self._board = Board()
        self._game_state = 'UNFINISHED'
        self._players = (Player('b'), Player('w'))
        self._turn = self._players[0]

    def get_game_state(self):
        """ Returns the state of the game. """
        return self._game_state

    def resign_game(self):
        """ Allows the current player to quit the game with a loss. """
        # Removes all rings from the current player
        self._turn.resign()
        self.check_win_condition()

    def make_move(self, old_center, new_center):
        """ Moves a piece defined by it's center to a new square defined by it's center. """
        if self._game_state != 'UNFINISHED':
            return False
        if not self._board.is_legal_move(self._turn, old_center, new_center):
            return False

        self._board.move_piece(old_center, new_center)
        self.check_win_condition()
        self.switch_turn()
        # TODO: check old rings
        # TODO: check for new rings
        # TODO: update state as necessary
        self._board.print_board()

        return True

    def switch_turn(self):
        """ Switches the players turn. """
        if self._turn == self._players[0]:
            self._turn = self._players[1]
        else:
            self._turn = self._players[0]

    def check_win_condition(self):
        """ Checks if a player is without rings and updates the status of the game. """
        if not self._players[0].has_rings():
            self._game_state = 'WHITE_WON'
        elif not self._players[1].has_rings():
            self._game_state = 'BLACK_WON'


class Board:
    """ Represents a Gess game board. """
    def __init__(self):
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

    def move_piece(self, old_center, new_center):
        """ Moves the piece and updates the board. """
        # Convert human readable position into list indices
        old_center = self._convert_position_to_indices(old_center)
        new_center = self._convert_position_to_indices(new_center)

        # Get spaces moved in the form [rows, columns]
        move = [new_center[0] - old_center[0], new_center[1] - old_center[1]]

        # Get pieces from indices of center square
        old_piece = self._get_piece_from_center(old_center)

        # Remove captured stones and move the piece
        old_piece = self._remove_piece(old_piece)
        self._place_piece(old_piece, move)

        # Remove gutter stones
        self._clear_gutter()

    def _remove_piece(self, squares):
        """ Removes a piece from the board. """
        piece = {}

        for square in squares:
            # Creates a dictionary with tuple keys identifying board location
            # and value of the stone at that location
            piece[square[0], square[1]] = self._spaces[square[0]][square[1]]
            self._spaces[square[0]][square[1]] = ""

        return piece

    def _place_piece(self, squares, move):
        """ Places a piece on the board. """
        for location, stone in squares.items():
            new_space = location[0] + move[0], location[1] + move[1]
            self._spaces[new_space[0]][new_space[1]] = stone

    def _clear_gutter(self):
        """ Clears the gutters of stones. """
        # The board is a square so any length is ok for rows and columns
        length = len(self._spaces) - 1

        # Clear the first and last row and column
        for i in range(length):
            self._spaces[0][i] = ""
            self._spaces[i][0] = ""
            self._spaces[length][i] = ""
            self._spaces[i][length] = ""

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

    def is_legal_move(self, player, old_center, new_center):
        """ Returns true if the move from the old center to the new center is a legal move. """
        # Get pieces
        old_center = self._convert_position_to_indices(old_center)
        new_center = self._convert_position_to_indices(new_center)
        old_piece = self._get_piece_from_center(old_center)
        new_piece = self._get_piece_from_center(new_center)

        # Check if the piece only contains a single color
        piece_color = self.get_single_color_piece(old_piece)
        if piece_color is None:
            return False

        # Check if the color of the piece is the appropriate color's turn
        color = player.get_color()
        if piece_color != color:
            return False

        # Check if the move is in a legal direction
        direction = self._get_valid_move(old_center, new_center)
        if direction is None:
            return False

        # Check if the piece can move in the desired direction
        direction_stone = old_center[0] + direction[0], old_center[1] + direction[1]
        center_stone = self._spaces[old_center[0]][old_center[1]]
        if not (center_stone == color or self._spaces[direction_stone[0]][direction_stone[1]] == color):
            return False

        # Check if the piece can move the desired distance
        # Any nonzero distance is sufficient since movement is only in 8 directions
        if old_center[0] != new_center[0]:
            distance = new_center[0] - old_center[0]
        else:
            distance = new_center[1] - old_center[1]

        if not (center_stone == color or abs(distance) <= 3):
            return False

        # TODO: Check that the move would not destroy the last of turn's color
        broken_rings = []
        for ring_center in player.get_rings():
            ring = self._get_piece_from_center(ring_center)

            for ring_square in ring:
                if ring_square in old_piece and ring_square in new_piece:
                    # Ring may not be broken if the move maintains the ring
                    # TODO: Test if the ring is broken
                    pass
                elif ring_square in old_piece or ring_square in new_piece:
                    # TODO: This may not be the case for new_piece
                    # Ring is broken
                    broken_rings.append(ring_center)

        # All of players rings will be broken; sorted to ensure proper comparison
        if sorted(broken_rings) == sorted(player.get_rings()):
            return False

        return True

    @staticmethod
    def _get_valid_move(old_center, new_center):
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
            offset = -1, 0

        elif vertical_move < 0 and horizontal_move == 0:
            # Southward move
            offset = 1, 0

        elif vertical_move > 0 and vertical_move == horizontal_move:
            # Northeasterly move
            offset = -1, 1

        elif vertical_move < 0 and vertical_move == horizontal_move:
            # Southwesterly move
            offset = 1, -1

        elif vertical_move > 0 and sum(vertical_move, horizontal_move) == 0:
            # Northwesterly move
            offset = -1, -1

        elif vertical_move < 0 and sum(vertical_move, horizontal_move) == 0:
            # Southeasterly move
            offset = 1, 1

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
    def _convert_position_to_indices(position):
        """ Converts a position in letter/number format to indices. """
        row = int(position[1:]) - 1

        # Get the row and column number; the offset from A is the row number
        col_letter = position[0].upper()
        col = ord(col_letter) - ord('A')

        return row, col

    @staticmethod
    def _get_piece_from_center(center):
        """ Gets the set of 9 squares corresponding to the center square as a list of tuples. """
        nw_corner = center[0] - 1, center[1] - 1

        # row + (0 to 3), col + (0 to 3)
        return [(nw_corner[0] + i, nw_corner[1] + j) for j in range(3) for i in range(3)]


class Player:
    """ Represents a player of the Gess game. """
    def __init__(self, color):
        self._color = color
        self._rings = []

        # Sets the initial rings for each player
        if color == "b":
            self._rings.append((2, 11))
        elif color == "w":
            self._rings.append((17, 11))

    def get_color(self):
        """ Returns the player's color as a char. """
        return self._color

    def get_rings(self):
        """ Returns the locations of the centers of players rings. """
        return self._rings

    def has_rings(self):
        """ Returns true if the player has any rings. """
        if len(self._rings) > 0:
            return True

        return False

    def add_ring(self, location):
        """ Adds a location for the center of a ring. """
        self._rings.append(location)

    def remove_ring(self, location):
        """ Removes a ring that had a center at the location. """
        # Removes the specified ring
        for index, ring_center in enumerate(self._rings):
            if ring_center == location:
                del self._rings[index]

    def resign(self):
        """ Removes all of the players rings. """
        self._rings = []


def main():
    """ This is not meant to be run as a script. Performs simple tests. """
    b = Board()
    b.print_board()
    b.move_piece('r4', 'p4')
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
