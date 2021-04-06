import PyQt5.QtCore as QtCore


class BallsPottedListModel(QtCore.QAbstractListModel):
    def __init__(self, balls_potted=None):
        super().__init__()
        self._balls_potted = balls_potted or []

    def data(self, index: QtCore.QModelIndex, role: QtCore.Qt.DisplayRole) -> str:
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

    def rowCount(self, index: QtCore.QModelIndex) -> int:
        """Get count of items in balls potted list

        :param index: model index
        :type index: QtCore.QModelIndex
        :return: length of balls potted list
        :rtype: int
        """
        return len(self._balls_potted)

    def appendData(self, data: str):
        """Append data to balls potted list

        :param data: ball potted
        :type data: str
        """
        self._balls_potted.append(data)
        self.layoutChanged.emit()

    def clear(self):
        """Clear balls potted list"""
        self._balls_potted.clear()
        self.layoutChanged.emit()
