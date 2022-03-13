import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets


class Ui_Combobox(QtWidgets.QComboBox):
    def __init__(
        self,
        parent=None,
        items=None,
        width=None,
        height=None,
        objectName=None,
        sizePolicy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred),
    ):
        super().__init__(parent)
        if items:
            self.addItems(items)
        if width:
            self.setMaximumWidth(width[0])
            self.setMinimumWidth(width[1])
        if height:
            self.setMaximumHeight(height[0])
            self.setMinimumHeight(height[1])
        if objectName:
            self.setObjectName(objectName)

        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet("padding: .3em")
        self.setSizePolicy(QtWidgets.QSizePolicy(sizePolicy[0], sizePolicy[1]))
