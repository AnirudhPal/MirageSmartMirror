import sys
import time
import groom
import DateTime
import weather
import feeds
import analog
import maps
import googleCalendar
import time
import threading
# for news
from newsapi import NewsApiClient
import requests
import json
#
from PyQt5.QtWidgets import *#QApplication, QWidget, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QSpacerItem, QGridLayout, QFormLayout
from PyQt5.QtGui import *#QFont, QPalette, QColor, QPainter, QPolygon
from PyQt5.QtCore import *
from simpleRec import *



'''
<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
'''

# Init
newsapi = NewsApiClient(api_key='33ff7834a7ee40928e7bb90746c8b6e5')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
                                        language='en',
                                          country='us')

# /v2/everything
#all_articles = newsapi.get_everything(language='en',
                                      # sort_by='relevancy')

# /v2/sources
news_sources = newsapi.get_sources()
# print(all_articles)
# print(top_headlines)

news_url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=33ff7834a7ee40928e7bb90746c8b6e5')
news_response = requests.get(news_url)
news_data = news_response.json()
# for i in range(10):
#     print(news_data['articles'][i]['title'])


font = QFont('Helvetica', 24)
news_source_font = QFont('Helvetica', 11, italic = True)
news_headline_font = QFont('Helvetica', 13)
news_space_font = QFont('Helvetica', 4)
font.setWeight(1)

class Window(QWidget):
    def __init__ (self):
        super().__init__()
        self.qt = QWidget()
        self.init_ui()
        # self.currentWidget = None

    def init_ui(self):
        # self.qt.showFullScreen()
        self.analog = analog.AnalogClock()
        self.rt = maps.Maps()
        self.calendarEvents = googleCalendar.Calendar()

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
        self.feed.setFixedWidth(800)
        self.appBox.addWidget(self.feed)

        ###
        self.appList = []
        self.news = QPushButton('News')
        self.calendar = QPushButton('Calendar')
        self.routes = QPushButton('Routes')
        self.appList.append(self.news)
        self.appList.append(self.calendar)
        self.appList.append(self.routes)
        self.appList.append(self.qt.gmb)


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
        # self.qt.h_box.addWidget(self.qt.gmb)
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
        self.routes.clicked.connect(self.routes_info)

        self.init_timer()
        self.init_controller()
        self.loggedIn = False
        self.ExpirationTimerCount = 0
        self.numberOfDetectedFaces = 0
        self.faceFrame = 0
        self.proximity = 300


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
        self.qt.lsb = QPushButton('Lock screen')
        self.qt.lsb.clicked.connect(self.lsd)
        self.qt.v_box.addWidget(self.qt.lsb)
        self.qt.v_box.addLayout(self.TimeWeatherBox)
        # self.qt.v_box.addSpacing(400)
        self.qt.v_box.addLayout(self.appBox)
        self.qt.v_box.addLayout(self.welcomeBox)
        self.qt.v_box.addSpacing(200)
        self.qt.v_box.addLayout(self.appListBox)
        self.proximity = 300

    def gmd(self):
        self.timer.stop()
        self.clearLayout(self.qt.v_box)
        # self.qt.v_box.deleteLater()
        # self.gr = groom.Groom(self.qt)
        # self.qt.v_box.addLayout(self.TimeWeatherBox)
        self.qt.v_box.addWidget(self.qt.lsb)
        self.qt.v_box.addWidget(groom.Groom().frame)
        self.qt.v_box.setContentsMargins(0,0,0,0)
        self.proximity = 1000
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
        self.routes.setEnabled(True)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "News Headlines" + "</font")

        for i in range(6):
            temp1 = QLabel("<font color='white'>" + news_data['articles'][i]['title'] + "." + "</font")
            temp1.setFont(news_headline_font)
             # + news_data['articles'][i]['source']['name']
            temp2 = QLabel("<font color='white'>" + news_data['articles'][i]['source']['name'] + "</font")
            temp2.setFont(news_source_font)
            temp3 = QLabel()
            temp3.setFont(news_space_font)
            # news_data['articles'][i]['source']['name']
            temp1.setAlignment(Qt.AlignLeft)
            self.feed.feedForm.addRow(temp2, temp1)
            self.feed.feedForm.addRow(temp3)

    def routes_info(self):
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        self.routes.setEnabled(False)
        self.calendar.setEnabled(True)
        self.news.setEnabled(True)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "Routes Info" + "</font")

        for route in self.rt.routes:
            temp1 = QLabel("<font color='white'>" + route[1] + "</font")
            temp1.setFont(news_source_font)
             # + news_data['articles'][i]['source']['name']
            temp2 = QLabel("<font color='white'>" + route[0] + "</font")
            temp2.setFont(news_headline_font)
            temp3 = QLabel()
            temp3.setFont(news_space_font)
            # news_data['articles'][i]['source']['name']
            temp1.setAlignment(Qt.AlignLeft)
            self.feed.feedForm.addRow(temp2, temp1)
            self.feed.feedForm.addRow(temp3)

    def calendar_events(self):
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        self.calendar.setEnabled(False)
        self.news.setEnabled(True)
        self.routes.setEnabled(True)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "Calendar Events" + "</font")

        if self.calendarEvents.events == None:
            self.feed.title.setText("<font color='white'>" + "No upcoming events!" + "</font")
        else:
            for i in range(6):
                event = self.calendarEvents.events[i]
                temp1 = QLabel("<font color='white'>" + event['summary'] + "</font")
                temp1.setFont(news_headline_font)
                 # + news_data['articles'][i]['source']['name']
                temp2 = QLabel("<font color='white'>" + event['start'] + "</font")
                temp2.setFont(news_source_font)
                temp3 = QLabel()
                temp3.setFont(news_space_font)
                # news_data['articles'][i]['source']['name']
                temp1.setAlignment(Qt.AlignLeft)
                self.feed.feedForm.addRow(temp2, temp1)
                self.feed.feedForm.addRow(temp3)


    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def init_controller(self):
        self.cTimer = QTimer()
        self.cTimer.timeout.connect(self.controller)
        self.cTimer.start(5000)

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

    def controller(self):
        # import ipdb; ipdb.set_trace()

        if self.loggedIn is False:
            self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()
        # sensor.self.proximity()
        # self.proximity = 300
        if self.proximity > 200:

            if self.numberOfDetectedFaces == 1 and not self.loggedIn:
                print("one face Detected")
                print(recognize(self.faceFrame)) #login
                self.msd()
                self.loggedIn = True

                #if unknown ask if user wants to setup a new profile
                    #setup profile Protocal

                #if recognize retuned a name login
                    #loggedIn = True
                    #diSplAY
            elif self.numberOfDetectedFaces == 1 and self.loggedIn:
                print("one face and you are logged in")
                #if another user, start timer (5 sec) and switch to new profile

            elif self.numberOfDetectedFaces > 1:
                print("one person only")
            else :
                print("no one is here")
                self.ExpirationTimerCount=self.ExpirationTimerCount+1

                    #change ui to lock screen

                #please one person in front
        if self.proximity > 600:
            self.ExpirationTimerCount=self.ExpirationTimerCount+1
            self.msd()

        if self.ExpirationTimerCount >= 10:
            self.loggedIn = False


window_app = QApplication(sys.argv)
# a_window = Window()
Display = Window()
# t = threading.Thread(target = lambda: Display.controller())
# t.daemon = True
# t.start()
sys.exit(window_app.exec_())

#create proximity sensor

# while True:
#     time.sleep(3)
#     numberOfDetectedFaces,faceFrame = numberOfFaces()
#     # sensor.proximity()
#     proximity = 300
#     if proximity > 200:
#
#         if numberOfDetectedFaces == 1 and not loggedIn:
#             print("one face Detected")
#             print(recognize(faceFrame)) #login
#             # Display.msd()
#             # loggedIn = True
#
#             #if unknown ask if user wants to setup a new profile
#                 #setup profile Protocal
#
#             #if recognize retuned a name login
#                 #loggedIn = True
#                 #diSplAY
#         elif numberOfDetectedFaces == 1 and loggedIn:
#             print("one face and you are logged in")
#             #if another user, start timer (5 sec) and switch to new profile
#
#         elif numberOfDetectedFaces > 1:
#             print("one person only")
#         else :
#             print("no one is here")
#             ExpirationTimerCount=ExpirationTimerCount+1
#
#                 #change ui to lock screen
#
#             #please one person in front
#     elif proximity > 600:
#         ExpirationTimerCount=ExpirationTimerCount+1
#
#     if ExpirationTimerCount >= 10:
#         loggedIn = False
