# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Creates an implementation of the Gess game which handles main game logic
#               including making a move, changing turns, resigning, and tracking game state.


from models.Board import Board
from models.Player import Player
from models.IllegalMove import IllegalMove
from PySide2.QtCore import Signal, QObject


class Game(QObject):
    """ Represents a game of Gess.  Maintains game state, tracks turn,
        maintains players and updates them.  Allows for making a move and resigning.
        Will have a Board object for communicating player input to the Board.  Will have
        2 Player objects for updating and checking their list of rings. Has no parameters. """
    board_updated = Signal()
    status_updated = Signal()

    def __init__(self):
        super(Game, self).__init__()

        self._board = Board()
        self._status_message = ""
        self._game_state = 'UNFINISHED'
        self._players = (Player('b'), Player('w'))
        self._active = 0

    def get_board(self):
        """ Returns the 20x20 board. """
        return self._board

    def get_status_message(self):
        """ Returns the status message. """
        return self._status_message

    def set_status_message(self, msg):
        """ Sets the status message with a new string. """
        self._status_message = msg
        # noinspection PyUnresolvedReferences
        self.status_updated.emit()

    def get_game_state(self):
        """ Has no parameters. Returns the state of the game. For tracking if the
            game has been won. """
        return self._game_state

    def get_active_player(self):
        """ Has no parameters. Returns the active player. For tracking whose turn
            it is. """
        return self._players[self._active]

    def make_move(self, source, target):
        """ Moves the piece and updates the state of the game. """
        self._board.move_piece(source, target)

        # Remove gutter stones
        self._board.clear_gutter()

        # If the move breaks the player's final ring, undo the move
        try:
            self.update_rings()
        except IllegalMove:
            self._status_message = "Unable to break last ring"
            # noinspection PyUnresolvedReferences
            self.status_updated.emit()
            for piece in (source, target):
                self._board.place_piece(piece)
            return

        self._board.set_selected(None)
        self.check_win_condition()
        self.switch_turn()

        # Signals the board is updated
        # noinspection PyUnresolvedReferences
        self.board_updated.emit()

    def resign_game(self):
        """ Has no parameters. Allows the active player to quit the game with a
            loss.  Updates a player and the game state. Returns nothing. """
        # Removes all rings from the current player
        self.get_active_player().set_rings([])
        self.check_win_condition()

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

        # noinspection PyUnresolvedReferences
        self.status_updated.emit()

    def check_win_condition(self):
        """ Has no parameters. Checks if a player is without rings and updates the status of the game. """
        for i, player in enumerate(self._players):
            # The player has no rings
            if not player.has_rings():
                # Get the color of the opposite player and create the state message
                state = self._players[i ^ 1].get_color() + "_WON"
                self._game_state = state

                # Update the status message
                self._status_message = self._game_state.title().replace("_", " ")
                # noinspection PyUnresolvedReferences
                self.status_updated.emit()
