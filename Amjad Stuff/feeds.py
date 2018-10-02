import sys
import time
# import cv2
# from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
import urllib.parse, urllib.request, json
from PyQt5.QtWidgets import *#QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import *#QFont, QPalette, QColor, QPainter, QPolygon, QImage, QPixmap
from PyQt5.QtCore import *

class Feeds(QWidget):
    def __init__ (self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # font = QFont('Helvetica', 18)
        # font.setWeight(1)

        # geolocator = Nominatim(user_agent="MirageSmartMirror")
        # location = geolocator.geocode("250 Sheetz Street West Lafayette Indiana")
        # print((location.latitude, location.longitude))

        # baseurl = "https://query.yahooapis.com/v1/public/yql?"
        # yql_query = "select * from weather.forecast where woeid in (SELECT woeid FROM geo.places WHERE text=\"(%f,%f)\")" %(location.latitude, location.longitude)
        # yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
        # result = urllib.request.urlopen(yql_url).read()
        # self.data = json.loads(result)
        # print(self.data['query']['results'])

        # datetime = QDateTime.currentDateTime()


        # Set background black
        # self.darkPalette = QPalette()
        # self.darkPalette.setColor(QPalette.Background, Qt.black)
        # self.qt.setPalette(self.darkPalette)


        self.feedVBox = QVBoxLayout()
        self.feedVBox.setAlignment(Qt.AlignCenter)

        self.titleBox = QHBoxLayout()
        self.titleBox.setAlignment(Qt.AlignCenter)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.titleBox.addWidget(self.title)

        # Feed box in the center (for news, calendar...)
        self.feedForm = QFormLayout()
        self.feedForm.setVerticalSpacing(20)
        self.feedForm.setAlignment(Qt.AlignCenter)

        self.feedVBox.addLayout(self.titleBox)
        self.feedVBox.addSpacing(10)
        self.feedVBox.addLayout(self.feedForm)


        self.setLayout(self.feedVBox)





        # self.location = QLabel()
        # self.location.setAlignment(Qt.AlignLeft)
        # self.location.setFont(font)
        # self.location.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['title'] + "</font")
        #
        # self.condition = QLabel()
        # self.condition.setAlignment(Qt.AlignLeft)
        # self.condition.setFont(font)
        # self.condition.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['text'] + "</font")
        #
        # self.temp = QLabel()
        # self.temp.setAlignment(Qt.AlignLeft)
        # self.temp.setFont(font)
        # self.temp.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['temp'] + "u'\N{DEGREE SIGN}'" + "</font")
        #
        # self.icon = QLabel()
        # self.icon.setAlignment(Qt.AlignLeft)
        # self.icon.setPixmap(QPixmap.fromImage(image))
        #
        #
        #
        # self.weatherBox.addWidget(self.location)
        # self.weatherBox.addWidget(self.condition)
        # self.weatherBox.addWidget(self.icon)
        # self.weatherBox.addWidget(self.temp)
        #
        # self.weatherBox.setAlignment(Qt.AlignLeft)
        #
        # self.setLayout(self.weatherBox)

        # self.timeWeatherBox.addLayout(self.weatherBox)

        # self.weatherBox.setFixedHeight(300)

        # oldLayout.addLayout(self.timeWeatherBox)






        # self.qt.setLayout(oldLayout)
        # self.qt.setWindowTitle('Main screen')

        # self.qt.digitaltime.setAlignment(Qt.AlignCenter)

        # self.qt.b.clicked.connect(self.btn_click)

        # self.init_timer()


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


    # def init_timer(self):
    #     self.timer = QTimer()
    #     self.timer.timeout.connect(self.update_time)
    #     self.timer.start(1000)
    #
    # def update_time(self):
    #     datetime = QDateTime.currentDateTime()
    #     if self.weatherBox != None:
    #         self.location.setText("<font color='white'>" + self.data['query']['results']['channel']['location']['city'] + "</font")
    #         self.condition.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['text'] + "</font")
    #         self.temp.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['temp'] + u'\N{DEGREE SIGN}' + "</font")
    #
    # def clearLayout(self, layout):
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget() is not None:
    #             child.widget().deleteLater()
    #         elif child.layout() is not None:
    #             self.clearLayout(child.layout())
    # def clearLayout(self, layout):
        # for i in reversed(range(layout.count())):
        #     widget = layout.itemAt(i).widget()
        #     if widget != None:
        #         widget.deleteLater()
