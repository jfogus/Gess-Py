# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Handles input and triggers model updates for the game history.


from PySide2.QtCore import QObject


class HistoryController(QObject):
    def __init__(self, model):
        super(HistoryController, self).__init__()

        self._history = model
