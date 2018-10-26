import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPolygon
from PyQt5.QtCore import *

class DateTime(QWidget):
    def __init__ (self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # self.qt.showFullScreen()

        # self.qt.resize(800, 800)

        datetime = QDateTime.currentDateTime()

        font = QFont('Helvetica', 18)
        font.setWeight(1)

        # Set background black
        # self.darkPalette = QPalette()
        # self.darkPalette.setColor(QPalette.Background, Qt.black)
        # self.qt.setPalette(self.darkPalette)

        # effect = QGraphicsDropShadowEffect()
        # effect2 = QGraphicsDropShadowEffect()
        # effect.setOffset(1, 1)
        # effect2.setOffset(1, 1)
        # effect.setBlurRadius(30)
        # effect.setColor(QColor(255,255,255))
        # effect2.setBlurRadius(20)
        # effect2.setColor(QColor(255,255,255))
        # self.qt.setGraphicsEffect(effect)

        #
        # self.qt.b = QPushButton('Update time')
        # self.qt.l = QLabel()
        # self.qt.time = QLabel("<font color='white'>" + datetime.toString() + "</font")
        # self.qt.time.setFont(font)
        # self.analog.setGraphicsEffect(effect)
        # self.qt.time.setGraphicsEffect(effect2)

        # self.timeBox = QVBoxLayout()
        self.timeBox = QVBoxLayout()
        # self.timeWeatherBox = QHBoxLayout()
        # self.timeBox.setAlignment(Qt.AlignRight)

        self.day = QLabel()
        self.day.setAlignment(Qt.AlignRight)
        self.day.setFont(font)
        self.day.setText("<font color='white'>" + datetime.toString("dddd") + "</font")

        self.date = QLabel()
        self.date.setAlignment(Qt.AlignRight)
        self.date.setFont(font)
        self.date.setText("<font color='white'>" + datetime.toString("MMM d, yyyy") + "</font")

        self.time = QLabel()
        self.time.setAlignment(Qt.AlignRight)
        self.time.setFont(font)
        self.time.setText("<font color='white'>" + datetime.toString("h:mm AP") + "</font")

        self.timeBox.addWidget(self.day)
        self.timeBox.addWidget(self.date)
        self.timeBox.addWidget(self.time)

        self.timeBox.setAlignment(Qt.AlignRight)

        self.setLayout(self.timeBox)

        # self.timeWeatherBox.addLayout(self.timeBox)

        # self.timeBox.setFixedHeight(300)

        # oldLayout.addLayout(self.timeWeatherBox)






        # self.qt.setLayout(oldLayout)
        # self.qt.setWindowTitle('Main screen')

        # self.qt.digitaltime.setAlignment(Qt.AlignCenter)

        # self.qt.b.clicked.connect(self.btn_click)

        self.init_timer()


        # self.qt.showFullScreen()

        # self.clearLayout(self.qt.analogclock)

    # def btn_click(self):
        # datetime = QDateTime.currentDateTime()
        # self.qt.time.setText("<font color='white'>" + datetime.toString() + "</font")
        # self.clearLayout(self.qt.analogclock)
        # self.clearLayout(self.qt.digitaltime)
        # self.clearLayout(self.qt.h_box)
        # self.timer.stop()
        # self.clearLayout(self.qt.v_box)
        # self.qt.v_box.deleteLater()
        # self.gr = groom.Groom(self.qt)


    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        datetime = QDateTime.currentDateTime()
        if self.timeBox != None:
            self.day.setText("<font color='white'>" + datetime.toString("dddd") + "</font")
            self.date.setText("<font color='white'>" + datetime.toString("MMM d, yyyy") + "</font")
            self.time.setText("<font color='white'>" + datetime.toString("h:mm AP") + "</font")

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
    # def clearLayout(self, layout):
        # for i in reversed(range(layout.count())):
        #     widget = layout.itemAt(i).widget()
        #     if widget != None:
        #         widget.deleteLater()
