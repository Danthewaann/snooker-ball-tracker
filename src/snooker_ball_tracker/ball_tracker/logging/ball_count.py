import PyQt5.QtCore as QtCore


class BallCount(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that keeps track of the count of balls
        for a specific colour"""
        super().__init__()
        self._count = 0

    @property
    def count(self) -> int:
        """Count of balls

        :return: count
        :rtype: int
        """
        return self._count

    countChanged = QtCore.pyqtSignal(int)

    @count.setter
    def count(self, value: int):
        """Count setter

        :param value: value to set
        :type value: int
        """
        self._count = value
        self.countChanged.emit(self._count)
