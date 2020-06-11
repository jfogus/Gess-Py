# Author:  Joshua Fogus
# Date:  6/5/20
# Description:  Accepts user input from the Board View.


from PySide2.QtCore import QObject, Signal


class BoardController(QObject):
    """ Receives the users input from the Board view, validates,
        and sends requests to the model. """
    move_legal = Signal(dict, dict)
    status_update = Signal(str)

    def __init__(self, model):
        super(BoardController, self).__init__()

        self._model = model
        self._board = model.get_board()

        # noinspection PyUnresolvedReferences
        self.move_legal.connect(self._model.make_move)

    def handle_square_click(self, coords):
        """ Validates a piece selection or move
            updates the Board. """
        source = self._board.get_selected()
        target = self.get_piece(coords)

        if self._model.get_game_state() != 'UNFINISHED':
            # The game is over; no more clicks handled; status message updated by game
            return

        # If no piece is selected, select the piece
        if source is None:
            if not self.is_piece_empty(target):
                self._board.set_selected(target)
                # Clear the status message
                # noinspection PyUnresolvedReferences
                self.status_update.emit("")
            else:
                # noinspection PyUnresolvedReferences
                self.status_update.emit("This piece has no stones.")
                pass

        # If selected and coords is the selected square, deselect the piece
        elif source == target:
            self._board.set_selected(None)

        # Move the piece and update the game
        elif self.is_legal_move(source, target):
            # noinspection PyUnresolvedReferences
            self.move_legal.emit(source, target)

        # Illegal move; nothing to do
        return

    def get_piece(self, center):
        """ Takes a center coordinate as a tuple in the form (row, col) and
            returns a dictionary of the piece's squares in the form
            {(row, col): stone}. """
        piece = {}
        sw_corner = center[0] - 1, center[1] - 1

        # From SW corner, all other squares of the piece are positive offsets away
        for row in range(3):
            for col in range(3):
                # Position on the board (row, col)
                square = sw_corner[0] + row, sw_corner[1] + col
                piece[square[0], square[1]] = self._board.get_squares()[square[0]][square[1]]

        return piece

    def is_legal_move(self, source, target):
        """ Checks the various rules of the Gess game to determine
            if the move is legal. """
        delta = self.get_delta(source, target)

        if self.in_gutter(source) or self.in_gutter(target):
            # noinspection PyUnresolvedReferences
            self.status_update.emit("Cannot select a piece in the gutter.")
            return False

        if not self.is_player_piece(self._model.get_active_player(), source):
            # noinspection PyUnresolvedReferences
            self.status_update.emit("This piece is not the active player's.")
            return False

        if not self.is_legal_direction(source, delta):
            # noinspection PyUnresolvedReferences
            self.status_update.emit("This is not a legal direction.")
            return False

        if not self.is_legal_distance(source, delta):
            # noinspection PyUnresolvedReferences
            self.status_update.emit("This is not a legal distance.")
            return False

        # TODO: Check if last ring is broken by the move; previously made the move
        #       check the rings, then reversed the move if necessary

        return True

    def in_gutter(self, piece):
        """ Determines if a pieces center is in the gutter. """
        # The forth element in the piece is the center square
        center = list(piece.keys())[4]
        gutter_indices = (0, len(self._board.get_squares()) - 1)

        # Check if row is in in a gutter row or column is in a gutter column
        if center[0] in gutter_indices or center[1] in gutter_indices:
            return True

        return False

    @staticmethod
    def is_piece_empty(piece):
        """ Returns True if the piece is empty; otherwise, False. """
        for stone in list(piece.values()):
            if stone != "":
                # The piece has a stone
                return False

        # The piece has no stones
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
        # TODO: Make this more readable
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
        for row_delta, col_delta in zip(row_steps, col_steps):
            # Checks moved squares up to but not including the final movement
            for location in locations:
                row = location[0] + row_delta
                col = location[1] + col_delta
                stone = self._board.get_squares()[row][col]
                if (row, col) not in locations and stone != '':
                    # The square is not in the origin piece, the move
                    # is not the last move, and the square has a stone.
                    return False

        return True

    @staticmethod
    def is_player_piece(player, piece):
        """ Has 2 parameters, player and piece, in the form of a Player object
            and a dictionary in the form {(row, col): stone} corresponding to
            a 3x3 square. Returns True if all stones in the piece belong to
            player and False otherwise. """
        player_stone = player.get_stone()
        stone_set = set(piece.values())

        # Check stones in the piece for unowned stones or an empty piece
        if not (stone_set == {player_stone} or stone_set == {player_stone, ''}):
            return False

        # The piece belongs to player
        return True

    @staticmethod
    def get_delta(origin, target):
        """ Has 2 parameters, pieces, in the form {(row, col): stone}.  Calculates
            the number of rows and columns moved.  Returns target - origin
            as a tuple in the form (delta_row, delta_col). """
        origin_square = next(iter(origin.keys()))
        target_square = next(iter(target.keys()))

        return target_square[0] - origin_square[0], target_square[1] - origin_square[1]


if __name__ == "__main__":
    pass
