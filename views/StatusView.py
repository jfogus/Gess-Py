# Author:  Joshua Fogus
# Date:  6/9/20
# Description:  An indicator of the status of the game and any
#               errors that arise.


from PySide2.QtWidgets import QDockWidget, QWidget, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont


class StatusView(QDockWidget):
    def __init__(self, model):
        super(StatusView, self).__init__()

        self._game = model

        # Place the bar, and remove title bar and features
        self.setAllowedAreas(Qt.TopDockWidgetArea)
        self.setFeatures(self.NoDockWidgetFeatures)
        self.setTitleBarWidget(QWidget())

        # Add the status indicator and styles
        self._status = QLabel()
        self._status.setAlignment(Qt.AlignCenter)
        self._status.setContentsMargins(0, 12, 0, 0)
        self._status.setFont(QFont("Arial", 16))
        self.setWidget(self._status)

        self.update_message()

        self._game.status_updated.connect(self.update_message)

    def update_message(self):
        """ Updates the text of the label with a message. """
        # Add a separator as necessary
        turn_msg = self.get_turn_msg()
        status_msg = self._game.get_status_message()

        # Add conditional punctuation
        if turn_msg != "" and status_msg != "":
            turn_msg += "; "

        self._status.setText(turn_msg + status_msg)

    def get_turn_msg(self):
        """ Creates a message indicating the player's turn. """
        if self._game.get_game_state() == "UNFINISHED":
            message = "{}'s Turn".format(self._game.get_active_player().get_color().title())
        else:
            message = ""

        return message
