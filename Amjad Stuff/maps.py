import sys
import time
# import cv2
# from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
import urllib.parse, urllib.request, json, requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPolygon, QImage, QPixmap
from PyQt5.QtCore import *


class Maps(QWidget):
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
        origin = geolocator.geocode("250 Sheetz Street, West Lafayette, Indiana")
        destination1 = geolocator.geocode("305 Swindon Way, West Lafayette, Indiana")
        destination2 = geolocator.geocode("222 West Wood St, West Lafayette, Indiana")
        destination3 = geolocator.geocode("West Madison Street, Chicago, Illinois")
        # print((origin.latitude, origin.longitude))




        maps_key = "&key=AIzaSyDKTb75-vuAvnWxO2Wfm_1DWlyr4BadgJc"

        maps_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"

        maps_origin1 = "&origins=%f,%f" %(origin.latitude, origin.longitude)
        maps_destination1 = "&destinations=%f,%f" %(destination1.latitude, destination1.longitude)
        maps_request1 = maps_url + maps_origin1 + maps_destination1 + maps_key

        maps_origin2 = "&origins=%f,%f" %(origin.latitude, origin.longitude)
        maps_destination2 = "&destinations=%f,%f" %(destination2.latitude, destination2.longitude)
        maps_request2 = maps_url + maps_origin2 + maps_destination2 + maps_key

        maps_origin3 = "&origins=%f,%f" %(origin.latitude, origin.longitude)
        maps_destination3 = "&destinations=%f,%f" %(destination3.latitude, destination3.longitude)
        maps_request3 = maps_url + maps_origin3 + maps_destination3 + maps_key


        maps_get1 = requests.get(maps_request1)
        maps_json1 = maps_get1.json()

        maps_get2 = requests.get(maps_request2)
        maps_json2 = maps_get2.json()

        maps_get3 = requests.get(maps_request3)
        maps_json3 = maps_get3.json()

        route_info_time_1 = "Time to %s: %s" %(maps_json1['destination_addresses'][0], maps_json1['rows'][0]['elements'][0]['duration']['text'])
        route_info_dist_1 = "%s away" % maps_json1['rows'][0]['elements'][0]['distance']['text']

        route_info_time_2 = "Time to %s: %s" %(maps_json2['destination_addresses'][0], maps_json2['rows'][0]['elements'][0]['duration']['text'])
        route_info_dist_2 = "%s away" % maps_json2['rows'][0]['elements'][0]['distance']['text']

        route_info_time_3 = "Time to %s: %s" %(maps_json3['destination_addresses'][0], maps_json3['rows'][0]['elements'][0]['duration']['text'])
        route_info_dist_3 = "%s away" % maps_json3['rows'][0]['elements'][0]['distance']['text']


        self.routes = [[route_info_time_1, route_info_dist_1], [route_info_time_2, route_info_dist_2], [route_info_time_3, route_info_dist_3]]


        # print(maps_json1['rows'][0]['elements'][0]['distance']['text'])




        datetime = QDateTime.currentDateTime()

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

        # self.mapBox = QVBoxLayout()
        # self.mapBox = QVBoxLayout()
        # self.timemapBox = QHBoxLayout()
        # self.mapBox.setAlignment(Qt.AlignRight)
        # image = cv2.imread("cloudy.png")
        # image = cv2.resize(image, (50, 50), interpolation=cv2.INTER_CUBIC)
        # image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)

        # self.dest1 = QLabel()
        # self.dest1.setAlignment(Qt.AlignLeft)
        # self.dest1.setFont(font)
        # # self.dest1.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['title'] + "</font")
        #
        # self.dest2 = QLabel()
        # self.dest2.setAlignment(Qt.AlignLeft)
        # self.dest2.setFont(font)
        # # self.dest2.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['dest2']['text'] + "</font")
        #
        # self.dest3 = QLabel()
        # self.dest3.setAlignment(Qt.AlignLeft)
        # self.dest3.setFont(font)
        # # self.dest3.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['dest2']['dest3'] + "u'\N{DEGREE SIGN}'" + "</font")
        #
        # self.dest1.setText("<font color='white'>" + "West Lafayette" + "</font")
        # self.dest2.setText("<font color='white'>" + "Cloudy" + "</font")
        # self.dest3.setText("<font color='white'>" + "72" + u'\N{DEGREE SIGN}' + "</font")

        # self.icon = QLabel()
        # self.icon.setAlignment(Qt.AlignLeft)
        # self.icon.setPixmap(QPixmap.fromImage(image))



        # self.mapBox.addWidget(self.dest1)
        # self.mapBox.addWidget(self.dest2)
        # # self.mapBox.addWidget(self.icon)
        # self.mapBox.addWidget(self.dest3)
        #
        # self.mapBox.setAlignment(Qt.AlignLeft)
        #
        # self.setLayout(self.mapBox)

        # self.timemapBox.addLayout(self.mapBox)

        # self.mapBox.setFixedHeight(300)

        # oldLayout.addLayout(self.timemapBox)






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


    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        datetime = QDateTime.currentDateTime()
        if self.mapBox != None:
            self.dest1.setText("<font color='white'>" + "West Lafayette" + "</font")
            self.dest2.setText("<font color='white'>" + "Cloudy" + "</font")
            self.dest3.setText("<font color='white'>" + "72" + u'\N{DEGREE SIGN}' + "</font")
            # self.dest1.setText("<font color='white'>" + self.data['query']['results']['channel']['dest1']['city'] + "</font")
            # self.dest2.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['text'] + "</font")
            # self.dest3.setText("<font color='white'>" + self.data['query']['results']['channel']['item']['condition']['temp'] + u'\N{DEGREE SIGN}' + "</font")

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
