from __future__ import annotations

import PyQt5.QtCore as QtCore


class BallsPotted(QtCore.QAbstractListModel):
    def __init__(self, balls_potted: list[str] | None = None):
        """Creates an instance of this class that stores the balls potted,
        as reported from the ball tracker

        :param balls_potted: list of balls potted, defaults to None
        """
        super().__init__()
        self._balls_potted = balls_potted or []

    def data(
        self,
        index: QtCore.QModelIndex,
        role: int = QtCore.Qt.DisplayRole,
    ) -> str | None:
        """Get ball potted for index row

        :param index: model index
        :param role: display role
        :return: ball potted
        """
        if role == QtCore.Qt.DisplayRole:
            text = self._balls_potted[index.row()]
            return text
        return None

    def rowCount(self, parent: QtCore.QModelIndex = QtCore.QModelIndex()) -> int:
        """Get count of items in balls potted list

        :param index: model index
        :return: length of balls potted list
        """
        return len(self._balls_potted)

    def addPottedBall(self, potted_ball: str) -> None:
        """Append potted ball to balls potted list

        :param potted_ball: ball potted
        """
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._balls_potted.append(potted_ball)
        self.endInsertRows()
        self.layoutChanged.emit()  # type: ignore[attr-defined]

    def clear(self) -> None:
        """Clear balls potted list"""
        self._balls_potted.clear()
        self.layoutChanged.emit()  # type: ignore[attr-defined]
