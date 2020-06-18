# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Maintains a list of moves throughout the game.


from PySide2.QtCore import QObject, Signal


class History(QObject):
    move_added = Signal(dict, dict)

    def __init__(self, game):
        super(History, self).__init__()

        self._game = game

        # Move history is a stack in the form [(origin, destination)]
        # Origin and destination are in the form {(row, col): stone}
        self._history = []

        # Connect to game's update signal
        self._game.board_updated.connect(self.add_move)

    def get_history(self):
        """ Returns the history stack. """
        return self._history

    def add_move(self, origin, destination):
        """ Adds a move to the list of historical moves. """
        self._history.append((origin, destination))

        # noinspection PyUnresolvedReferences
        self.move_added.emit(origin, destination)

    def remove_move(self):
        del self._history[-1]

    @staticmethod
    def center_from_piece(piece):
        """ Returns coordinates for the center square of a piece. """
        return list(piece.keys())[4]

    @staticmethod
    def to_printable_coords(coords):
        """ Converts matrix indices to human readable coordinates. """
        return chr(coords[1] + 97) + str(coords[0] + 1)
