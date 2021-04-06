import PyQt5.QtCore as QtCore

from .ball_count_model import BallCountModel


class SnapshotModel(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._whites = BallCountModel()
        self._reds = BallCountModel()
        self._yellows = BallCountModel()
        self._greens = BallCountModel()
        self._browns = BallCountModel()
        self._blues = BallCountModel()
        self._pinks = BallCountModel()
        self._blacks = BallCountModel()

    @property
    def whites(self) -> BallCountModel:
        """Whites property

        :return: whites
        :rtype: BallCountModel
        """
        return self._whites

    @property
    def reds(self) -> BallCountModel:
        """Reds property

        :return: reds
        :rtype: BallCountModel
        """
        return self._reds

    @property
    def yellows(self) -> BallCountModel:
        """Yellows property

        :return: yellows
        :rtype: BallCountModel
        """
        return self._yellows

    @property
    def greens(self) -> BallCountModel:
        """Greens property

        :return: greens
        :rtype: BallCountModel
        """
        return self._greens

    @property
    def browns(self) -> BallCountModel:
        """Browns property

        :return: browns
        :rtype: BallCountModel
        """
        return self._browns

    @property
    def blues(self) -> BallCountModel:
        """Blues property

        :return: blues
        :rtype: BallCountModel
        """
        return self._blues

    @property
    def pinks(self) -> BallCountModel:
        """Pinks property

        :return: pinks
        :rtype: BallCountModel
        """
        return self._pinks

    @property
    def blacks(self) -> BallCountModel:
        """Blacks property

        :return: blacks
        :rtype: BallCountModel
        """
        return self._blacks
