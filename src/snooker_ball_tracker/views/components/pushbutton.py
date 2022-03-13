import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class Ui_PushButton(QtWidgets.QPushButton):
    def __init__(
        self,
        name,
        parent=None,
        objectName=None,
        width=None,
        height=None,
        sizePolicy=None,
    ):
        super().__init__(name, parent)
        if width:
            self.setMinimumWidth(width[0])
            self.setMaximumWidth(width[1])
        if height:
            self.setMinimumHeight(height[0])
            self.setMaximumHeight(height[1])
        if objectName:
            self.setObjectName(objectName)
        if sizePolicy:
            self.setSizePolicy(sizePolicy)
        self.setStyleSheet("padding: .3em")

        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
