from typing import List

import PyQt5.QtCore as QtCore


class BallsPottedListModel(QtCore.QAbstractListModel):
    def __init__(self, balls_potted: List[str]=None):
        """Creates an instance of this class that stores the balls potted,
        as reported from the ball tracker

        :param balls_potted: list of balls potted, defaults to None
        :type balls_potted: List[str], optional
        """
        super().__init__()
        self._balls_potted = balls_potted or []

    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole) -> str:
        """Get ball potted for index row

        :param index: model index
        :type index: QtCore.QModelIndex
        :param role: display role
        :type role: QtCore.Qt.DisplayRole
        :return: ball potted
        :rtype: str
        """
        if role == QtCore.Qt.DisplayRole:
            text = self._balls_potted[index.row()]
            return text
        return None

    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        """Get count of items in balls potted list

        :param index: model index
        :type index: QtCore.QModelIndex
        :return: length of balls potted list
        :rtype: int
        """
        return len(self._balls_potted)

    def addPottedBall(self, potted_ball: str):
        """Append potted ball to balls potted list

        :param potted_ball: ball potted
        :type potted_ball: str
        """
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._balls_potted.append(potted_ball)
        self.endInsertRows()
        self.layoutChanged.emit()

    def clear(self):
        """Clear balls potted list"""
        self._balls_potted.clear()
        self.layoutChanged.emit()
