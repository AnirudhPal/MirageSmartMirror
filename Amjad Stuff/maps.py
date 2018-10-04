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




        # datetime = QDateTime.currentDateTime()


        # self.init_timer()


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
