import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class Ui_Slider(QtWidgets.QSlider):
    def __init__(
        self,
        max_range=100,
        parent=None,
        name=None,
        objectName=None,
        width=None,
        height=None,
        orientation=QtCore.Qt.Horizontal,
        sizePolicy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding),
    ):
        super().__init__(parent)
        if width:
            self.setMinimumWidth(width[0])
            self.setMaximumWidth(width[1])
        if height:
            self.setMinimumHeight(height[0])
            self.setMaximumHeight(height[1])
        if objectName:
            self.setObjectName(objectName)
        self.name = name

        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setMaximum(max_range)
        self.setOrientation(orientation)
        self.setSizePolicy(QtWidgets.QSizePolicy(sizePolicy[0], sizePolicy[1]))
