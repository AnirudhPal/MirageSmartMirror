import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPolygon
from PyQt5.QtCore import *

class Groom(QWidget):
    def __init__ (self, screenWindow):
        super().__init__()
        # self.qt = QWidget()
        self.qt = screenWindow
        self.init_ui()

    def init_ui(self):
        # self.qt.showFullScreen()

        # self.qt.resize(800, 800)

        # Set background black
        self.darkPalette = QPalette()
        self.darkPalette.setColor(QPalette.Background, Qt.black)
        self.qt.setPalette(self.darkPalette)

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 0)
        effect.setBlurRadius(300)
        effect.setColor(QColor(255,255,255))


        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(15)
        frame.setMidLineWidth(5)
        frame.setFrameShadow(QFrame.Raised)
        frame.setGraphicsEffect(effect)

        # self.qt.vbox = QVBoxLayout()
        self.qt.vbox = self.qt.layout()
        self.qt.vbox.addWidget(frame)
        self.qt.vbox.setContentsMargins(0,0,0,0)

        self.qt.setLayout(self.qt.vbox)



        # self.qt.setStyleSheet("background-color: solid black")
        # #
        # self.qt.b = QPushButton('Update time')
        # self.qt.l = QLabel()
        #
        # self.qt.space = QHBoxLayout()
        #
        # self.qt.space.addWidget(self.qt.l)
        #
        #
        # self.qt.vbox = QVBoxLayout()
        # # self.qt.vbox.addWidget(self.qt.b)
        # # self.qt.vbox.addLayout(self.qt.space)
        # self.qt.vbox.addSpacing(150)
        # self.qt.vbox.addLayout(self.qt.analogclock)
        # self.qt.vbox.addLayout(self.qt.digitaltime)
        # self.qt.vbox.addSpacing(50)
        # self.qt.vbox.addLayout(self.qt.welcomebox)


        # self.qt.setLayout(self.qt.vbox)
        self.qt.setWindowTitle('Grooming mode')

        # self.qt.b.clicked.connect(self.btn_click)

        self.qt.showFullScreen()

    # def btn_click(self):
    #     datetime = QDateTime.currentDateTime()
    #     self.qt.time.setText("<font color='white'>" + datetime.toString() + "</font")

    # def init_timer(self):
    #     self.timer = QTimer()
    #     self.timer.timeout.connect(self.update_time)
    #     self.timer.start(1000)
    #
    # def update_time(self):
    #     datetime = QDateTime.currentDateTime()
    #     self.qt.time.setText("<font color='white'>" + datetime.toString() + "</font")

# app = QApplication(sys.argv)
# a_window = Groom()
# sys.exit(app.exec_())
