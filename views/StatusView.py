# Author:  Joshua Fogus
# Date:  6/9/20
# Description:  An indicator of the status of the game and any
#               errors that arise.


from PySide2.QtWidgets import QDockWidget, QWidget, QLabel
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont


class StatusView(QDockWidget):
    def __init__(self, model, controller):
        super(StatusView, self).__init__()

        self._model = model
        self._controller = controller
        self._text = self._model.get_game_state()

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

        self.update_turn()

        self._model.turn_changed.connect(self.update_turn)
        self._controller.status_update.connect(self.update_message)

    def update_message(self, msg):
        """ Updates the text of the label with a message. """
        # Add a separator as necessary
        if msg != "":
            msg = "; " + msg

        self._status.setText(self.get_turn_msg() + msg)

    def update_turn(self):
        """ Updates the label with a message indicating the active
            player's turn. """
        self._status.setText(self.get_turn_msg())

    def get_turn_msg(self):
        """ Creates a message indicating the player's turn. """
        message = "{}'s turn".format(self._model.get_active_player().get_color().title())

        return message
