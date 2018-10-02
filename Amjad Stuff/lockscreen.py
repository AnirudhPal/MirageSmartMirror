import sys
import time
import groom
import DateTime
import weather
import feeds
from PyQt5.QtWidgets import *#QApplication, QWidget, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QSpacerItem, QGridLayout, QFormLayout
from PyQt5.QtGui import *#QFont, QPalette, QColor, QPainter, QPolygon
from PyQt5.QtCore import *


'''
<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
'''


font = QFont('Helvetica', 24)
font.setWeight(1)

class Window(QWidget):
    def __init__ (self):
        super().__init__()
        self.qt = QWidget()
        self.init_ui()
        # self.currentWidget = None

    def init_ui(self):
        # self.qt.showFullScreen()
        self.analog = AnalogClock()

        self.qt.resize(800, 800)

        datetime = QDateTime.currentDateTime()

        font = QFont('Helvetica', 18)
        font.setWeight(1)

        # Set background black
        self.darkPalette = QPalette()
        self.darkPalette.setColor(QPalette.Background, Qt.black)
        self.qt.setPalette(self.darkPalette)

        effect = QGraphicsDropShadowEffect()
        effect2 = QGraphicsDropShadowEffect()
        effect.setOffset(1, 1)
        effect2.setOffset(1, 1)
        effect.setBlurRadius(30)
        effect.setColor(QColor(255,255,255))
        effect2.setBlurRadius(20)
        effect2.setColor(QColor(255,255,255))
        # self.qt.setGraphicsEffect(effect)

        #
        self.qt.msb = QPushButton('Main screen')
        self.qt.gmb = QPushButton('Groom mode')
        self.qt.lsb = QPushButton('Lock screen')
        self.qt.l = QLabel()
        self.qt.time = QLabel("<font color='white'>" + datetime.toString("MMM d, yyyy hh:mm:ss AP") + "</font")
        self.qt.time.setFont(font)
        self.analog.setGraphicsEffect(effect)
        self.qt.time.setGraphicsEffect(effect2)

        # Main screen layout
        self.TimeWeatherBox = QHBoxLayout()
        self.welcomeBox = QHBoxLayout()
        self.appListBox = QHBoxLayout()
        self.appBox = QHBoxLayout()

        ###
        self.weather = weather.Weather()
        self.weather.weatherBox.setAlignment(Qt.AlignLeft)
        self.weather.setFixedHeight(150)
        self.TimeWeatherBox.addWidget(self.weather)

        self.datetime = DateTime.DateTime()
        self.datetime.setFixedHeight(150)
        self.TimeWeatherBox.addWidget(self.datetime)

        ###
        self.welcomeLabel = QLabel("<font color='white'>" + "Welcome, Amjad!" + "</font")
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setFixedHeight(100)
        self.welcomeBox.addWidget(self.welcomeLabel)

        ###
        self.feed = feeds.Feeds()
        self.appBox.addWidget(self.feed)

        ###
        self.appList = []
        self.news = QPushButton('News')
        self.calendar = QPushButton('Calendar')
        self.notifications = QPushButton('Notifications')
        self.appList.append(self.news)
        self.appList.append(self.calendar)
        self.appList.append(self.notifications)


        # grid = QGridLayout()
        # for i in range(3):
        #     grid.addWidget(self.appList[i],0,i)
        #     # self.appListBox.addWidget(app)
        # self.appListBox.addLayout(grid)
        for app in self.appList:
            self.appListBox.addWidget(app)





        self.qt.digitaltime = QHBoxLayout()
        self.qt.analogclock = QHBoxLayout()



        # self.qt.welcomebox = QHBoxLayout()

        self.qt.digitaltime.addWidget(self.qt.time)
        self.qt.analogclock.addWidget(self.analog)
        # self.qt.feedBox.addWidget(self.qt.l)

        self.qt.h_box = QHBoxLayout()
        # self.qt.h_box.addStretch()
        self.qt.h_box.addWidget(self.qt.msb)
        self.qt.h_box.addWidget(self.qt.gmb)
        # self.qt.h_box.addStretch()

        self.qt.v_box = QVBoxLayout()
        # self.qt.v_box.addWidget(self.qt.msb)
        self.qt.v_box.addLayout(self.qt.h_box)
        # self.qt.spacer = QSpacerItem(150, 150)
        # self.qt.v_box.addSpacerItem(self.qt.spacer)
        self.qt.v_box.addSpacing(150)
        self.qt.v_box.addLayout(self.qt.analogclock)
        self.qt.v_box.addLayout(self.qt.digitaltime)
        # self.qt.v_box.addSpacing(50)
        # self.qt.v_box.addLayout(self.qt.welcomebox)


        self.qt.setLayout(self.qt.v_box)
        self.qt.setWindowTitle('Lock screen')

        self.qt.digitaltime.setAlignment(Qt.AlignCenter)

        self.qt.msb.clicked.connect(self.msd)
        self.qt.gmb.clicked.connect(self.gmd)
        self.qt.lsb.clicked.connect(self.lsd)
        self.news.clicked.connect(self.news_headlines)
        self.calendar.clicked.connect(self.calendar_events)

        self.init_timer()


        self.qt.showFullScreen()

        # self.clearLayout(self.qt.analogclock)

    def msd(self):
    #     datetime = QDateTime.currentDateTime()
    #     self.qt.time.setText("<font color='white'>" + datetime.toString() + "</font")
        # self.clearLayout(self.qt.analogclock)
        # self.clearLayout(self.qt.digitaltime)
        # self.clearLayout(self.qt.h_box)
        self.timer.stop()
        self.clearLayout(self.qt.v_box)
        # self.qt.v_box.deleteLater()
        # self.gr = groom.Groom(self.qt)
        self.qt.setWindowTitle('Main screen')
        self.qt.v_box.addWidget(self.qt.lsb)
        self.qt.v_box.addLayout(self.TimeWeatherBox)
        # self.qt.v_box.addSpacing(400)
        self.qt.v_box.addLayout(self.appBox)
        self.qt.v_box.addLayout(self.welcomeBox)
        self.qt.v_box.addLayout(self.appListBox)

    def gmd(self):
        self.timer.stop()
        self.clearLayout(self.qt.v_box)
        # self.qt.v_box.deleteLater()
        # self.gr = groom.Groom(self.qt)
        # self.qt.v_box.addLayout(self.TimeWeatherBox)
        self.qt.v_box.addWidget(self.qt.lsb)
        self.qt.v_box.addWidget(groom.Groom().frame)
        self.qt.v_box.setContentsMargins(0,0,0,0)
        # self.qt.v_box.addSpacing(400)
        # self.qt.v_box.addLayout(self.welcomeBox)
        # self.qt.v_box.addLayout(self.appListBox)

    def lsd(self):
        self.datetime.timer.stop()
        self.clearLayout(self.qt.v_box)
        self.qt.v_box.deleteLater()
        new_widget = QWidget()
        self.qt = new_widget
        self.init_ui()
        # self.qt.v_box.addLayout(self.TimeWeatherBox)
        # self.qt.v_box.addSpacing(400)
        # self.qt.v_box.addLayout(self.welcomeBox)
        # self.qt.v_box.addLayout(self.appListBox)

    def news_headlines(self):
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        self.calendar.setEnabled(True)
        self.news.setEnabled(False)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "News Headlines" + "</font")

        for i in range(6):
            temp1 = QLabel("<font color='white'>" + "News Headline " + str(i+1) + "</font")
            temp1.setAlignment(Qt.AlignLeft)
            self.feed.feedForm.addRow(temp1)



    def calendar_events(self):
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        self.calendar.setEnabled(False)
        self.news.setEnabled(True)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "Calendar Events" + "</font")

        for i in range(6):
            temp1 = QLabel("<font color='white'>" + "Calendar Events " + str(i+1) + "</font")
            temp1.setAlignment(Qt.AlignLeft)
            self.feed.feedForm.addRow(temp1)


    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        datetime = QDateTime.currentDateTime()
        if self.qt.digitaltime != None:
            self.qt.time.setText("<font color='white'>" + datetime.toString("MMM d, yyyy hh:mm:ss AP") + "</font")

    # def fade(self):
    #     self.fadeTimer = QTimer()
    #     self.fadeTimer.timeout.connect(self.opacity)
    #     self.fadeTimer.start(50)
    #
    # def opacity(self):
    #     if(self.currentWidget is None) or (self.currentWidget.windowOpacity() <= 0):
    #         self.fadeTimer.stop()
    #         self.currentWidget.deleteLater()
    #         self.currentWidget = None
    #     else:
    #         self.currentWidget.setWindowOpacity(self.currentWidget.windowOpacity() - 0.1)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
                # self.currentWidget = child.widget()
                # self.fade()
            elif child.layout() is not None:
                self.clearLayout(child.layout())
    # def clearLayout(self, layout):
        # for i in reversed(range(layout.count())):
        #     widget = layout.itemAt(i).widget()
        #     if widget != None:
        #         widget.deleteLater()







class AnalogClock(QWidget):
    hourHand = QPolygon([
        QPoint(2, -2),
        QPoint(-2, -2),
        QPoint(-2, -55),
        QPoint(2, -55)
    ])

    minuteHand = QPolygon([
        QPoint(2, -2),
        QPoint(-2, -2),
        QPoint(-2, -80),
        QPoint(2, -80)
    ])

    secondHand = QPolygon([
        QPoint(1, -1),
        QPoint(-1, -1),
        QPoint(-1, -85),
        QPoint(1, -85)
    ])

    hourColor = QColor(255,250,250)
    minuteColor = QColor(245, 245, 245)
    secondColor = QColor(255, 0, 0)

    def __init__(self, parent=None):
        super(AnalogClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.setWindowTitle("Analog Clock")
        self.resize(200, 200)

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Hour hand
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.hourColor)

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(AnalogClock.hourHand)
        painter.restore()

        painter.setPen(AnalogClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        # Minute hand
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.minuteColor)

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(AnalogClock.minuteHand)
        painter.restore()

        painter.setPen(AnalogClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

        # Second hand
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.secondColor)

        painter.save()
        painter.rotate(6.0 * time.second())
        painter.drawConvexPolygon(AnalogClock.secondHand)
        painter.restore()

app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
