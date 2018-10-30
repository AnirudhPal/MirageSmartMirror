import sys
import time
import groom
import DateTime
import weather
import feeds
import analog
import maps
import googleCalendar
import os
# for news
from newsapi import NewsApiClient
import requests
import json
#
from PyQt5.QtWidgets import *#QApplication, QWidget, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QSpacerItem, QGridLayout, QFormLayout
from PyQt5.QtGui import *#QFont, QPalette, QColor, QPainter, QPolygon
from PyQt5.QtCore import *

font = QFont('Helvetica', 24)
news_source_font = QFont('Helvetica', 11, italic = True)
news_headline_font = QFont('Helvetica', 13)
news_space_font = QFont('Helvetica', 4)
font.setWeight(1)

users = {}

class User:
    def __init__ (self, id, name, address, destinations, news):
        self.userId = id
        self.userName = name
        self.userAddress = address
        self.favDestinations = destinations
        self.newsPreferences = news

    def getNumberOfUsers(self):
        path, dirs, files = next(os.walk("/Users/azahraa/Desktop/MirageSmartMirror/Amjad Stuff/Users"))
        file_count = len(files)
        print(files)
        print("# of users: %d" %(file_count-1))
        return file_count-1

    def getUser(self, id):
        filename = "/Users/azahraa/Desktop/MirageSmartMirror/Amjad Stuff/Users/user%d" %id
        with open(filename + '.json') as data_file:
            data = json.load(data_file)
        # print(data)
        return data

    def addUser(self, id, userJSON):
        users[id] = userJSON
        # print(users)
        return
    def updateUser(self, id, userJSON):
        users[id] = userJSON
        return
    def deleteUser(self, id):
        filename = "/Users/azahraa/Desktop/MirageSmartMirror/Amjad Stuff/Users/user%d.json" %id
        del users[id]
        os.remove(filename)
        return

    def convertToJSON(self):
        return
    def convertToUser(self, userJSON):
        self.userId = userJSON['id']
        self.userName = userJSON['name']
        self.userAddress = userJSON['address']
        self.favDestinations = userJSON['destinations']
        self.newsPreferences = userJSON['news']
        return

if __name__== "__main__":
    user0 = User("Amjad", "250 Sheetz St.", "Home", "Sports")
    # user0.getNumberOfUsers()
    # user0.getUser(0)
    # user0.addUser(0, user0.getUser(0))
    # user0.addUser(1, user0.getUser(0))
    # user0.deleteUser(0)
    # print(users)
