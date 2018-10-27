import sys
import time
import cv2
# from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
import urllib.parse, urllib.request, json, requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPolygon, QImage, QPixmap
from PyQt5.QtCore import *

icons = {
'cloudy':'icons/cloudy.png',
'partly-cloudy-day':'icons/cloudy.png',
'partly-cloudy-night':'icons/cloudy.png',
'fog':'icons/fog.png',
'wind':'icons/wind.png',
'sleet':'icons/sleet.png',
'snow':'icons/snow.png',
'rain':'icons/raining.png',
'clear-day':'icons/sun.png',
'clear-night':'icons/moon.png',
'thunderstorm':'icons/storm.png',
'hail':'icons/hail.png',
'tornado':'icons/tornado.png'
}


class Weather(QWidget):
    def __init__ (self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        geolocator = Nominatim(user_agent="MirageSmartMirror")
        origin = geolocator.geocode("250 Sheetz Street, West Lafayette, Indiana")
        destination = geolocator.geocode("305 Swindon Way, West Lafayette, Indiana")

        # print((origin.latitude, origin.longitude))




        # maps_key = "&key=AIzaSyDKTb75-vuAvnWxO2Wfm_1DWlyr4BadgJc"
        weather_key = "50f9b96898249aa1a036886103f78788"

        # maps_url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
        # maps_origin1 = "&origins=%f,%f" %(origin.latitude, origin.longitude)
        # maps_destination1 = "&destinations=%f,%f" %(destination.latitude, destination.longitude)
        # maps_request = maps_url1 + maps_origin1 + maps_destination1 + maps_key
        # https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.424399,-86.925882&destinations=40.422035,-86.901596&key=AIzaSyDKTb75-vuAvnWxO2Wfm_1DWlyr4BadgJc

        # maps_get1 = requests.get(maps_request)
        # maps_json1 = maps_get1.json()

        weather_url = "https://api.darksky.net/forecast/" + weather_key
        # 0123456789abcdef9876543210fedcba/42.3601,-71.0589
        weather_request = weather_url + "/%f,%f" %(origin.latitude, origin.longitude)
        # weather_request = weather_request +
        # print(weather_request)

        weather_get = requests.get(weather_request)
        weather_json = weather_get.json()
        # print(weather_json['timezone'])



        datetime = QDateTime.currentDateTime()

        font = QFont('Helvetica', 18)
        font.setWeight(1)


        self.weatherBox = QVBoxLayout()
        # self.timeWeatherBox = QHBoxLayout()
        # self.weatherBox.setAlignment(Qt.AlignRight)
        icon = icons[weather_json['currently']['icon']]
        image = cv2.imread(icon)
        image = cv2.resize(image, (50, 50), interpolation=cv2.INTER_CUBIC)
        image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)

        self.dailySummary = QLabel()
        self.dailySummary.setAlignment(Qt.AlignLeft)
        self.dailySummary.setFont(font)
        self.daily = weather_json['daily']['data'][0]['summary']
        self.dailySummary.setText("<font color='white'>" + self.daily + "</font")

        self.currently = QLabel()
        self.currently.setAlignment(Qt.AlignLeft)
        self.currently.setFont(font)
        self.curr = "Currently " + weather_json['currently']['summary']
        self.currently.setText("<font color='white'>" + self.curr + "</font")

        self.temp = QLabel()
        self.temp.setAlignment(Qt.AlignLeft)
        self.temp.setFont(font)
        self.fahrenheit = weather_json['currently']['temperature']
        self.temp.setText("<font color='white'> %d" %self.fahrenheit + u'\N{DEGREE SIGN}' + "</font")
        # self.dailySummary.setText("<font color='white'>" + "West Lafayette" + "</font")
        # self.currently.setText("<font color='white'>" + "Cloudy" + "</font")
        # self.temp.setText("<font color='white'>" + "72" + u'\N{DEGREE SIGN}' + "</font")

        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignLeft)
        self.icon.setPixmap(QPixmap.fromImage(image))



        self.weatherBox.addWidget(self.dailySummary)
        self.weatherBox.addWidget(self.currently)
        self.weatherBox.addWidget(self.icon)
        self.weatherBox.addWidget(self.temp)

        self.weatherBox.setAlignment(Qt.AlignLeft)

        self.setLayout(self.weatherBox)


        self.init_timer()



    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        datetime = QDateTime.currentDateTime()
        if self.weatherBox != None:
            # self.dailySummary.setText("<font color='white'>" + "West Lafayette" + "</font")
            # self.currently.setText("<font color='white'>" + "Cloudy" + "</font")
            # self.temp.setText("<font color='white'>" + "72" + u'\N{DEGREE SIGN}' + "</font")
            self.dailySummary.setText("<font color='white'>" + self.daily + "</font")
            self.currently.setText("<font color='white'>" + self.curr + "</font")
            self.temp.setText("<font color='white'> %d" %self.fahrenheit + u'\N{DEGREE SIGN}' + "</font")


    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())