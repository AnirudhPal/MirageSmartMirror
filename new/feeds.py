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

        self.feedVBox = QVBoxLayout()
        self.feedVBox.setAlignment(Qt.AlignCenter)

        self.titleBox = QHBoxLayout()
        self.titleBox.setAlignment(Qt.AlignCenter)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.titleBox.addWidget(self.title)

        # Feed box in the center (for news, calendar...)
        self.feedForm = QFormLayout()
        self.feedForm.setVerticalSpacing(10)
        self.feedForm.setAlignment(Qt.AlignCenter)
        self.feedForm.setRowWrapPolicy(QFormLayout.WrapAllRows)

        self.feedVBox.addLayout(self.titleBox)
        self.feedVBox.addSpacing(10)
        self.feedVBox.addLayout(self.feedForm)


        self.setLayout(self.feedVBox)
