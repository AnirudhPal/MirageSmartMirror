import sys
import time
# import cv2
# from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
import urllib.parse, urllib.request, json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPolygon, QImage, QPixmap
from PyQt5.QtCore import *

class Weather(QWidget):
    def __init__ (self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # self.qt.showFullScreen()

        # self.qt.resize(800, 800)
        # send_url = 'http://freegeoip.net/json'
        # r = requests.get(send_url)
        # j = json.loads(r.text)
        # lat = j['latitude']
        # lon = j['longitude']

        # g = Geocoder.google('Mountain View, CA')
        # print(g.latlng)
        # latitude = 40.423874100000006
        # longitude = -86.9094914
        geolocator = Nominatim(user_agent="MirageSmartMirror")
        location = geolocator.geocode("250 Sheetz Street West Lafayette Indiana")
        # print((location.latitude, location.longitude))

        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid in (SELECT woeid FROM geo.places WHERE text=\"(%f,%f)\")" %(location.latitude, location.longitude)
        yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
        result = urllib.request.urlopen(yql_url).read()
        self.data = json.loads(result)
        # print(self.data['query']['results'])

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

        # self.weatherBox = QVBoxLayout()
        self.weatherBox = QVBoxLayout()
        # self.timeWeatherBox = QHBoxLayout()
        # self.weatherBox.setAlignment(Qt.AlignRight)
        # image = cv2.imread("cloudy.png")
        # image = cv2.resize(image, (50, 50), interpolation=cv2.INTER_CUBIC)
        # image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)

        self.location = QLabel()
        self.location.setAlignment(Qt.AlignLeft)
        self.location.setFont(font)
        self.location.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['title'] + "</font")

        self.condition = QLabel()
        self.condition.setAlignment(Qt.AlignLeft)
        self.condition.setFont(font)
        self.condition.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['text'] + "</font")

        self.temp = QLabel()
        self.temp.setAlignment(Qt.AlignLeft)
        self.temp.setFont(font)
        self.temp.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['temp'] + "u'\N{DEGREE SIGN}'" + "</font")

        # self.icon = QLabel()
        # self.icon.setAlignment(Qt.AlignLeft)
        # self.icon.setPixmap(QPixmap.fromImage(image))



        self.weatherBox.addWidget(self.location)
        self.weatherBox.addWidget(self.condition)
        # self.weatherBox.addWidget(self.icon)
        self.weatherBox.addWidget(self.temp)

        self.weatherBox.setAlignment(Qt.AlignLeft)

        self.setLayout(self.weatherBox)

        # self.timeWeatherBox.addLayout(self.weatherBox)

        # self.weatherBox.setFixedHeight(300)

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
        if self.weatherBox != None:
            self.location.setText("<font color='white'>" + self.data['query']['results']['channel']['location']['city'] + "</font")
            self.condition.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['text'] + "</font")
            self.temp.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['temp'] + u'\N{DEGREE SIGN}' + "</font")

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
