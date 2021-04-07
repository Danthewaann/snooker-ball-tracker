import PyQt5.QtCore as QtCore

from .ball_count import BallCount


class Snapshot(QtCore.QObject):
    def __init__(self):
        """Creates an instance of this class that contains ball counts for all
        possible ball colours"""
        super().__init__()
        self._whites = BallCount()
        self._reds = BallCount()
        self._yellows = BallCount()
        self._greens = BallCount()
        self._browns = BallCount()
        self._blues = BallCount()
        self._pinks = BallCount()
        self._blacks = BallCount()

    @property
    def whites(self) -> BallCount:
        """Whites property

        :return: whites
        :rtype: BallCountModel
        """
        return self._whites

    @property
    def reds(self) -> BallCount:
        """Reds property

        :return: reds
        :rtype: BallCountModel
        """
        return self._reds

    @property
    def yellows(self) -> BallCount:
        """Yellows property

        :return: yellows
        :rtype: BallCountModel
        """
        return self._yellows

    @property
    def greens(self) -> BallCount:
        """Greens property

        :return: greens
        :rtype: BallCountModel
        """
        return self._greens

    @property
    def browns(self) -> BallCount:
        """Browns property

        :return: browns
        :rtype: BallCountModel
        """
        return self._browns

    @property
    def blues(self) -> BallCount:
        """Blues property

        :return: blues
        :rtype: BallCountModel
        """
        return self._blues

    @property
    def pinks(self) -> BallCount:
        """Pinks property

        :return: pinks
        :rtype: BallCountModel
        """
        return self._pinks

    @property
    def blacks(self) -> BallCount:
        """Blacks property

        :return: blacks
        :rtype: BallCountModel
        """
        return self._blacks
