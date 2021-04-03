import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import snooker_ball_tracker.settings as s

from collections import OrderedDict
from snooker_ball_tracker.models.settings.ball_detection import BallDetectionTabModel, BallDetectionSettingGroupModel
from snooker_ball_tracker.models.observer import Observer
from .components.radiobutton import Ui_RadioButton
from .components.slider import Ui_Slider
from .components.label import Ui_Label
from .components.pushbutton import Ui_PushButton


class Ui_BallDetectionTab(QtWidgets.QWidget):
    def __init__(self, model: BallDetectionTabModel):
        super().__init__()
        self.model = model

        self.layout = QtWidgets.QGridLayout(self)

        self.groups = OrderedDict([
            ("convexity", Ui_BallDetectionSettingGroupBox("Convexity", BallDetectionSettingGroupModel("convexity"))),
            ("inertia", Ui_BallDetectionSettingGroupBox("Inertia", BallDetectionSettingGroupModel("inertia"))),
            ("circularity", Ui_BallDetectionSettingGroupBox("Circularity", BallDetectionSettingGroupModel("circularity"))),
            ("area", Ui_BallDetectionSettingGroupBox("Area", BallDetectionSettingGroupModel("area", multiplier=1), max_range=2000)),
        ])

        self.layout.addWidget(self.groups["convexity"], 0, 0)
        self.layout.addWidget(self.groups["inertia"], 0, 1)
        self.layout.addWidget(self.groups["circularity"], 1, 0)
        self.layout.addWidget(self.groups["area"], 1, 1)


class Ui_BallDetectionSettingGroupBox(QtWidgets.QGroupBox):
    def __init__(self, name, model: BallDetectionSettingGroupModel, max_range=100):
        super().__init__(name)
        self.model = model

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        self.filterBy_label = Ui_Label("Filter By", self, width=(120, 120), alignment=QtCore.Qt.AlignCenter)
        self.filterBy_yradio = Ui_RadioButton("Yes", value=True, parent=self, width=(50, 50))
        self.filterBy_nradio = Ui_RadioButton("No", value=False, checked=True, parent=self, width=(50, 50))

        self.minVal_label = Ui_Label("Minimum Value", self, width=(120, 120), alignment=QtCore.Qt.AlignCenter, 
                                     sizePolicy=(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.minVal_value = Ui_Label("0", self, alignment=QtCore.Qt.AlignCenter, width=(50, 50),
                              sizePolicy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.minVal_slider = Ui_Slider(max_range=max_range, parent=self, objectName="minVal_slider")

        self.maxVal_label = Ui_Label("Maximum Value", self, width=(120, 120), alignment=QtCore.Qt.AlignCenter,
                                    sizePolicy=(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        self.maxVal_value = Ui_Label("0", self, alignment=QtCore.Qt.AlignCenter, width=(50, 50),
                              sizePolicy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.maxVal_slider = Ui_Slider(max_range=max_range, parent=self, objectName="maxval_slider")

        self.reset_btn = Ui_PushButton("Reset", self, width=(0, 100), objectName="reset_btn")

        self.layout.addWidget(self.filterBy_label,  0, 0, 1, 1)
        self.layout.addWidget(self.filterBy_yradio, 0, 2, 1, 1)
        self.layout.addWidget(self.filterBy_nradio, 0, 3, 1, 1)
        self.layout.addWidget(self.minVal_label,    1, 0, 1, 1)
        self.layout.addWidget(self.minVal_value,    1, 1, 1, 1)
        self.layout.addWidget(self.minVal_slider,   1, 2, 1, 2)
        self.layout.addWidget(self.maxVal_label,    2, 0, 1, 1)
        self.layout.addWidget(self.maxVal_value,    2, 1, 1, 1)
        self.layout.addWidget(self.maxVal_slider,   2, 2, 1, 2)
        self.layout.addWidget(self.reset_btn,       3, 3, 1, 1, alignment=QtCore.Qt.AlignRight)

        self.group_observers = [
            Observer([(self.filterBy_yradio, "state"), (self.filterBy_nradio, "state"), (self.model, "filter_by")])
        ]

        # self.model.filterBy_valueChanged.connect(self.filterBy_yradio.setValue)
        # self.model.filterBy_valueChanged.connect(self.filterBy_nradio.setValue)
        # self.model.min_valueChanged.connect(self.minVal_slider.setValue)
        # self.model.max_valueChanged.connect(self.maxVal_slider.setValue)
        
        # QtCore.QMetaObject.connectSlotsByName(self)

        # self.model.setMinValue(s.BLOB_DETECTOR["MIN_" + self.model.name.upper()] * self.model.multiplier)
        # self.model.setMaxValue(s.BLOB_DETECTOR["MAX_" + self.model.name.upper()] * self.model.multiplier)
        # self.model.setFilterBy(s.BLOB_DETECTOR["FILTER_BY_" + self.model.name.upper()])

    @QtCore.pyqtSlot(bool)
    def on_filterBy_yradio_toggled(self, checked):
        if checked:
            self.model.setFilterBy(True)

    @QtCore.pyqtSlot(bool)
    def on_filterBy_nradio_toggled(self, checked):
        if checked:
            self.model.setFilterBy(False)

    @QtCore.pyqtSlot(int)
    def on_minVal_slider_valueChanged(self, value):
        self.minVal_value.setNum(value)
        self.model.setMinValue(value)

    @QtCore.pyqtSlot(int)
    def on_maxVal_slider_valueChanged(self, value):
        self.maxVal_value.setNum(value)
        self.model.setMaxValue(value)

    @QtCore.pyqtSlot()
    def on_reset_btn_pressed(self):
        self.model.reset()
