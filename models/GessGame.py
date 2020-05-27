# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Creates an implementation of the Gess game which handles main game logic
#               including making a move, changing turns, resigning, and tracking game state.

# TODO: This should probably be a controller.
from models.IllegalMove import IllegalMove
from models.Board import Board
from models.Player import Player


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

    # TODO: Update the players stones when making a move.
    # TODO: Check the players stones when checking for rings.
    # TODO: Refactor ring check

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

        # self._board.print_board()

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
