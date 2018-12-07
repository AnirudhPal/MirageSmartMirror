import sys
import os
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
import subprocess
# for news
from newsapi import NewsApiClient
import requests
import json
import coProcessor
#
from PyQt5.QtWidgets import *#QApplication, QWidget, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QSpacerItem, QGridLayout, QFormLayout
from PyQt5.QtGui import *#QFont, QPalette, QColor, QPainter, QPolygon
from PyQt5.QtCore import *
from simpleRec import *
from pynput.keyboard import Key, Listener
# for sensor
#import testSensor

'''
<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
'''



font = QFont('Helvetica', 24)
news_source_font = QFont('Helvetica', 11, italic = True)
news_headline_font = QFont('Helvetica', 13)
news_space_font = QFont('Helvetica', 4)
font.setWeight(1)

effect = QGraphicsDropShadowEffect()
effect2 = QGraphicsDropShadowEffect()
effect.setOffset(1, 1)
effect2.setOffset(1, 1)
effect.setBlurRadius(30)
effect.setColor(QColor(255,255,255))
effect2.setBlurRadius(20)
effect2.setColor(QColor(255,255,255))

icons = {
'cloudy':'/home/pi/MirageSmartMirror/src/icons/cloudy.png',
'partly-cloudy-day':'/home/pi/MirageSmartMirror/src/icons/cloudy.png',
'partly-cloudy-night':'/home/pi/MirageSmartMirror/src/icons/cloudy.png',
'fog':'/home/pi/MirageSmartMirror/src/icons/fog.png',
'wind':'/home/pi/MirageSmartMirror/src/icons/wind.png',
'sleet':'/home/pi/MirageSmartMirror/src/icons/sleet.png',
'snow':'/home/pi/MirageSmartMirror/src/icons/snow.png',
'rain':'/home/pi/MirageSmartMirror/src/icons/raining.png',
'clear-day':'/home/pi/MirageSmartMirror/src/icons/sun.png',
'clear-night':'/home/pi/MirageSmartMirror/src/icons/moon.png',
'thunderstorm':'/home/pi/MirageSmartMirror/src/icons/storm.png',
'hail':'/home/pi/MirageSmartMirror/src/icons/hail.png',
'maps':'/home/pi/MirageSmartMirror/src/icons/maps.png',
'news':'/home/pi/MirageSmartMirror/src/icons/news.png',
'main':'/home/pi/MirageSmartMirror/src/icons/main.png',
'groom':'/home/pi/MirageSmartMirror/src/icons/groom.png',
'calendar':'/home/pi/MirageSmartMirror/src/icons/calendar.png'
}

def get_wifi_status():
        # Check WiFi connectivity
        f = os.popen('iwgetid')
        now = f.read()
        if not now == '':
                return 1
        else:
                return 0


class Window(QWidget):
    def __init__ (self):
        super().__init__()
        self.qt = QWidget()
        self.init_ui()
        # print(str(threading.get_ident()))
        # self.currentWidget = None

    def init_ui(self):

        self.qt.resize(800, 800)

        font = QFont('Helvetica', 18)
        font.setWeight(1)

        # Set background black
        self.darkPalette = QPalette()
        self.darkPalette.setColor(QPalette.Background, Qt.black)
        self.qt.setPalette(self.darkPalette)


        self.loggedIn = False
        self.errorMessage = None
        self.userName = None
        # self.ExpirationTimerCount = 0
        # self.numberOfDetectedFaces = 0
        # self.faceFrame = 0
        self.proximity = 100
        self.isDetectingFace = False
        # self.prompt_asked = False
        # self.launch_face_detection = False
        self.new_user_prompt = False
        # self.googleCodeTimeout = 0
        self.curr_screen = 0    # 0: lock screen, 1: main screen, 2: groom mode, 3: prompt screen
        self.curr_app = 0
        # self.curr_user = 0
        # self.face_detection_countdown = 0
        self.google_code = None
        self.googleCodeTimeout = 0
        self.promptTimeout = 0
        self.walkAwayTimeout = -1
        self.curr_user_name = "John Doe"

# Creating new blank face detection status JSON file..
        statDict = {'username': None, 'error': None, 'cameraOn': False, 'detectCalled':False}
        with open("/home/pi/MirageSmartMirror/src/faceDetectStatus.json", 'w') as statFile:
            json.dump(statDict, statFile)

        coProcessor.initProximity()
        self.set_lockscreen_layout()
        self.init_timer()
        self.init_controller()


        self.qt.showFullScreen()

    def msd(self):
        if self.curr_screen == 0:
            self.timer.stop()
        self.loggedIn = True
        self.curr_screen = 1
        self.curr_app = 0
        self.clearLayout(self.qt.v_box)
        self.load_user_info(self.userName)
        # self.timer.stop()

        # user_destinations = ["305 Swindon Way, West Lafayette, Indiana", "222 West Wood St, West Lafayette, Indiana", "West Madison Street, Chicago, Illinois"]
        # self.rt = maps.Maps("250 Sheetz Street, West Lafayette, Indiana", user_destinations)
        # self.calendarEvents = googleCalendar.Calendar() # fix to take in user id and get user's token

        # self.qt.msb = QPushButton('Main screen')
        # self.qt.gmb = QPushButton('Groom mode')
        # self.qt.lsb = QPushButton('Lock screen')
        # self.qt.l = QLabel()

        # Main screen layout
        self.TimeWeatherBox = QHBoxLayout()
        self.welcomeBox = QHBoxLayout()
        self.appListBox = QHBoxLayout()
        self.appBox = QHBoxLayout()

        ###
        font = QFont('Helvetica', 18)
        font.setWeight(1)
        self.weather = QWidget()
        self.weather.weatherBox = QVBoxLayout()

        self.weather.dailySummary = QLabel()
        self.weather.dailySummary.setAlignment(Qt.AlignLeft)
        self.weather.dailySummary.setFont(font)

        self.weather.currently = QLabel()
        self.weather.currently.setAlignment(Qt.AlignLeft)
        self.weather.currently.setFont(font)

        self.weather.temp = QLabel()
        self.weather.temp.setAlignment(Qt.AlignLeft)
        self.weather.temp.setFont(font)

        self.weather.icon = QLabel()
        self.weather.icon.setAlignment(Qt.AlignLeft)

        self.weather.weatherBox.addWidget(self.weather.dailySummary)
        self.weather.weatherBox.addWidget(self.weather.currently)
        self.weather.weatherBox.addWidget(self.weather.icon)
        self.weather.weatherBox.addWidget(self.weather.temp)
        self.weather.weatherBox.setAlignment(Qt.AlignLeft)

        self.weather.setLayout(self.weather.weatherBox)


        self.weather.setFixedHeight(200)
        self.TimeWeatherBox.addWidget(self.weather)
        self.weather_info()

        self.datetime = DateTime.DateTime()
        self.datetime.setFixedHeight(150)
        self.TimeWeatherBox.addWidget(self.datetime)

        ###
        self.welcomeLabel = QLabel("<font color='white'>" + "Welcome, " + self.curr_user_name + "!" + "</font>")
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setFixedHeight(100)
        self.welcomeBox.addWidget(self.welcomeLabel)

        ###
        # self.feed = feeds.Feeds()
        self.feed.setFixedWidth(800)
        self.appBox.addWidget(self.feed)

        ###
        self.appList = []
        # self.news = QPushButton('News')
        # self.calendar = QPushButton('Calendar')
        # self.routes = QPushButton('Routes')
        self.news = QLabel()
        news_effect = QGraphicsDropShadowEffect()
        news_effect.setOffset(1, 1)
        news_effect.setBlurRadius(30)
        news_effect.setColor(QColor(255,255,255))
        news_icon = icons['news']
        news_image = cv2.imread(news_icon)
        news_image = cv2.resize(news_image, (60, 60), interpolation=cv2.INTER_CUBIC)
        news_image = QImage(news_image, news_image.shape[1], news_image.shape[0], news_image.strides[0], QImage.Format_RGB888)
        self.news.setFixedWidth(75)
        self.news.setFixedHeight(75)
        self.news.setAlignment(Qt.AlignCenter)
        self.news.setPixmap(QPixmap.fromImage(news_image))
        self.news.setFrameShape(QFrame.Box)
        self.news.setFrameShadow(QFrame.Raised)
        self.news.setLineWidth(1)
        self.news.setMidLineWidth(2)
        self.news.setGraphicsEffect(news_effect)
        self.news.graphicsEffect().setEnabled(False)

        self.calendar = QLabel()
        calendar_effect = QGraphicsDropShadowEffect()
        calendar_effect.setOffset(1, 1)
        calendar_effect.setBlurRadius(30)
        calendar_effect.setColor(QColor(255,255,255))
        calendar_icon = icons['calendar']
        calendar_image = cv2.imread(calendar_icon)
        calendar_image = cv2.resize(calendar_image, (60, 60), interpolation=cv2.INTER_CUBIC)
        calendar_image = QImage(calendar_image, calendar_image.shape[1], calendar_image.shape[0], calendar_image.strides[0], QImage.Format_RGB888)
        self.calendar.setFixedWidth(75)
        self.calendar.setFixedHeight(75)
        self.calendar.setAlignment(Qt.AlignCenter)
        self.calendar.setPixmap(QPixmap.fromImage(calendar_image))
        self.calendar.setFrameShape(QFrame.Box)
        self.calendar.setFrameShadow(QFrame.Raised)
        self.calendar.setLineWidth(1)
        self.calendar.setMidLineWidth(2)
        self.calendar.setGraphicsEffect(calendar_effect)
        self.calendar.graphicsEffect().setEnabled(False)

        self.maps = QLabel()
        maps_effect = QGraphicsDropShadowEffect()
        maps_effect.setOffset(1, 1)
        maps_effect.setBlurRadius(30)
        maps_effect.setColor(QColor(255,255,255))
        maps_icon = icons['maps']
        maps_image = cv2.imread(maps_icon)
        maps_image = cv2.resize(maps_image, (60, 60), interpolation=cv2.INTER_CUBIC)
        maps_image = QImage(maps_image, maps_image.shape[1], maps_image.shape[0], maps_image.strides[0], QImage.Format_RGB888)
        self.maps.setFixedWidth(75)
        self.maps.setFixedHeight(75)
        self.maps.setAlignment(Qt.AlignCenter)
        self.maps.setPixmap(QPixmap.fromImage(maps_image))
        self.maps.setFrameShape(QFrame.Box)
        self.maps.setFrameShadow(QFrame.Raised)
        self.maps.setLineWidth(1)
        self.maps.setMidLineWidth(2)
        self.maps.setGraphicsEffect(maps_effect)
        self.maps.graphicsEffect().setEnabled(False)

        self.groom = QLabel()
        groom_effect = QGraphicsDropShadowEffect()
        groom_effect.setOffset(1, 1)
        groom_effect.setBlurRadius(30)
        groom_effect.setColor(QColor(255,255,255))
        groom_icon = icons['groom']
        groom_image = cv2.imread(groom_icon)
        groom_image = cv2.resize(groom_image, (60, 60), interpolation=cv2.INTER_CUBIC)
        groom_image = QImage(groom_image, groom_image.shape[1], groom_image.shape[0], groom_image.strides[0], QImage.Format_RGB888)
        self.groom.setFixedWidth(75)
        self.groom.setFixedHeight(75)
        self.groom.setAlignment(Qt.AlignCenter)
        self.groom.setPixmap(QPixmap.fromImage(groom_image))
        self.groom.setFrameShape(QFrame.Box)
        self.groom.setFrameShadow(QFrame.Raised)
        self.groom.setLineWidth(1)
        self.groom.setMidLineWidth(2)
        self.groom.setGraphicsEffect(groom_effect)
        self.groom.graphicsEffect().setEnabled(False)

        self.main = QLabel()
        main_effect = QGraphicsDropShadowEffect()
        main_effect.setOffset(1, 1)
        main_effect.setBlurRadius(30)
        main_effect.setColor(QColor(255,255,255))
        main_icon = icons['main']
        main_image = cv2.imread(main_icon)
        main_image = cv2.resize(main_image, (60, 60), interpolation=cv2.INTER_CUBIC)
        main_image = QImage(main_image, main_image.shape[1], main_image.shape[0], main_image.strides[0], QImage.Format_RGB888)
        self.main.setFixedWidth(75)
        self.main.setFixedHeight(75)
        self.main.setAlignment(Qt.AlignCenter)
        self.main.setPixmap(QPixmap.fromImage(main_image))
        self.main.setFrameShape(QFrame.Box)
        self.main.setFrameShadow(QFrame.Raised)
        self.main.setLineWidth(1)
        self.main.setMidLineWidth(2)
        self.main.setGraphicsEffect(main_effect)
        self.main.graphicsEffect().setEnabled(True)



        self.appList.append(self.main)
        self.appList.append(self.calendar)
        self.appList.append(self.maps)
        self.appList.append(self.news)
        self.appList.append(self.groom)
        # self.appList.append(self.qt.gmb)


        for app in self.appList:
            self.appListBox.addWidget(app)

        # self.qt.msb.clicked.connect(self.msd)
        # self.qt.gmb.clicked.connect(self.gmd)
        # self.qt.lsb.clicked.connect(self.set_lockscreen_layout)
        # self.news.clicked.connect(self.news_headlines)
        # self.calendar.clicked.connect(self.calendar_events)
        # self.routes.clicked.connect(self.routes_info)

        # self.clearLayout(self.qt.v_box)

        self.qt.setWindowTitle('Main screen')
        # self.qt.lsb = QPushButton('Lock screen')
        # self.qt.lsb.clicked.connect(self.set_lockscreen_layout)
        #self.qt.v_box.addWidget(self.qt.lsb)
        self.qt.v_box.addLayout(self.TimeWeatherBox)

        self.qt.v_box.addLayout(self.appBox)
        self.qt.v_box.addLayout(self.welcomeBox)
        self.qt.v_box.addSpacing(50)
        self.qt.v_box.addLayout(self.appListBox)
        self.qt.v_box.addSpacing(150)

        # temp = DateTime.DateTime()
        # self.qt.v_box = temp

    def gmd(self):
        # self.curr_screen = 2
        self.curr_app = 4
        # self.timer.stop()
        # self.clearLayout(self.qt.v_box)
        self.feed.title.setText("<font color='black'>" + "Blank" + "</font>")
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        # Turn on LED
        coProcessor.setLedWhiteFadeIn()
        #self.qt.v_box.addWidget(self.qt.lsb)
        # self.qt.v_box.addWidget(groom.Groom().frame)
        # self.qt.v_box.setContentsMargins(0,0,0,0)

    def set_buffering_screen(self):
        self.clearLayout(self.qt.v_box)
        self.timer.stop()
        self.curr_screen = 3
        prompt_box = QHBoxLayout()
        self.prompt = QLabel("<font color='white'>" + "Please stand still while we detect your face and load your profile." + "</font>")
        self.prompt.setAlignment(Qt.AlignCenter)
        prompt_box.addWidget(self.prompt)
        self.qt.layout().addLayout(prompt_box)
        # self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()

    def set_new_user_screen(self):
        self.clearLayout(self.qt.v_box)
        # self.timer.stop()
        self.curr_screen = 3
        prompt_box = QHBoxLayout()
        self.prompt = QLabel("<font color='white'>" + "Face not recognized! Please download our MirageCompanion iPhone App to set up a new profile." + "</font>")
        self.prompt.setAlignment(Qt.AlignCenter)
        prompt_box.addWidget(self.prompt)
        self.qt.layout().addLayout(prompt_box)

    def show_auth_code(self):
        font = QFont('Helvetica', 28)
        font.setWeight(1)
        self.prompt.setText("<font color='white'>" + message + "</font>")
        self.prompt.setFont(font)
        self.googleCodeTimeout = 10
        return

    def load_user_info(self, user_name):
        # os.system('nohup python3 APIs.py &')
        # user_destinations = ["305 Swindon Way, West Lafayette, Indiana", "222 West Wood St, West Lafayette, Indiana", "West Madison Street, Chicago, Illinois"]
        file_path = "/home/pi/MirageSmartMirror/src/Users/%s/%sAPI.json" %(user_name, user_name)
        with open(file_path) as f:
            user_dict = json.load(f)

        self.rt = user_dict['map']
        self.calendarEvents = user_dict['events']
        self.weather_dict = user_dict['weather']
        self.datetime = DateTime.DateTime()
        self.feed = feeds.Feeds()
        self.news_data = user_dict['news']
        self.curr_user_name = user_dict['name']

    def changePrompt(self, message):
        font = QFont('Helvetica', 28)
        font.setWeight(1)
        self.prompt.setText("<font color='white'>" + message + "</font>")
        self.prompt.setFont(font)
        self.promptTimeout = 5
        return



    def set_lockscreen_layout(self):
        # self.init_timer()
        self.loggedIn = False
        self.walkAwayTimeout = -1
        self.numberOfDetectedFaces = 0
        if self.curr_app == 4:
            coProcessor.setLedWhiteFadeOut()
        self.curr_screen = 0
        # self.prompt_asked = False
        font = QFont('Helvetica', 18)
        font.setWeight(1)
        effect = QGraphicsDropShadowEffect()
        effect2 = QGraphicsDropShadowEffect()
        effect3 = QGraphicsDropShadowEffect()
        effect.setOffset(1, 1)
        effect2.setOffset(1, 1)
        effect3.setOffset(1, 1)
        effect.setBlurRadius(30)
        effect2.setBlurRadius(20)
        effect3.setBlurRadius(50)
        effect.setColor(QColor(255,255,255))
        effect2.setColor(QColor(255,255,255))
        effect3.setColor(QColor(255,255,255))

        datetime = QDateTime.currentDateTime()
        self.qt.time = QLabel("<font color='white'>" + datetime.toString("MMM d, yyyy hh:mm:ss AP") + "</font>")
        self.qt.time.setFont(font)
        self.qt.time.setGraphicsEffect(effect2)

        self.analog = analog.AnalogClock()
        self.analog.setGraphicsEffect(effect)

        self.qt.digitaltime = QHBoxLayout()
        self.qt.analogclock = QHBoxLayout()
        self.qt.digitaltime.addWidget(self.qt.time)
        self.qt.analogclock.addWidget(self.analog)
        self.qt.digitaltime.setAlignment(Qt.AlignCenter)

        self.qt.h_box = QHBoxLayout()
        self.qt.msb = QPushButton('Main screen')
        self.qt.msb.clicked.connect(self.msd)
        #self.qt.h_box.addWidget(self.qt.msb)

        prompt_box = QHBoxLayout()
        self.prompt = QLabel()
        self.prompt.setFixedHeight(50)
        self.prompt.setAlignment(Qt.AlignCenter)
        # self.prompt.setGraphicsEffect(effect2)
        self.prompt.setText("<font color='black'>" + "Blank" + "</font>")
        prompt_box.addWidget(self.prompt)


        if self.qt.layout() != None:
            self.clearLayout(self.qt.v_box)
            self.qt.layout().addLayout(self.qt.h_box)
            self.qt.layout().addSpacing(150)
            self.qt.layout().addLayout(self.qt.analogclock)
            self.qt.layout().addLayout(self.qt.digitaltime)
            self.qt.layout().addLayout(prompt_box)
            self.qt.layout().addSpacing(150)
            self.init_timer()
        else:
            self.qt.v_box = QVBoxLayout()
            self.qt.v_box.addLayout(self.qt.h_box)
            self.qt.v_box.addSpacing(150)
            self.qt.v_box.addLayout(self.qt.analogclock)
            self.qt.v_box.addLayout(self.qt.digitaltime)
            self.qt.v_box.addLayout(prompt_box)
            self.qt.v_box.addSpacing(150)
            self.qt.setLayout(self.qt.v_box)
            self.init_timer()

        self.qt.setWindowTitle('Lock screen')



    def news_headlines(self):
        self.curr_app = 3
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        # self.calendar.setEnabled(True)
        # self.news.setEnabled(False)
        # self.routes.setEnabled(True)
        if get_wifi_status() is 0:
            self.feed.title.setFont(font)
            self.feed.title.setText("<font color='white'>" + "No internet connection" + "</font>")
            # print("NO INTERNET IN NEWS")
            return
        self.feed.title.setFont(font)
        if self.news_data is None:
            self.feed.title.setText("<font color='white'>" + "No news preferences selected!" + "</font>")
            return
        self.feed.title.setText("<font color='white'>" + "News Headlines" + "</font>")

        for i in range(6):
            temp1 = QLabel("<font color='white'>" + self.news_data['articles'][i]['title'] + "." + "</font>")
            temp1.setFont(news_headline_font)
             # + self.news_data['articles'][i]['source']['name']
            temp2 = QLabel("<font color='white'>" + self.news_data['articles'][i]['source']['name'] + "</font>")
            temp2.setFont(news_source_font)
            temp3 = QLabel()
            temp3.setFont(news_space_font)
            # self.news_data['articles'][i]['source']['name']
            temp1.setAlignment(Qt.AlignLeft)
            self.feed.feedForm.addRow(temp2, temp1)
            self.feed.feedForm.addRow(temp3)

    def routes_info(self):
        self.curr_app = 2
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        # self.routes.setEnabled(False)
        # self.calendar.setEnabled(True)
        # self.news.setEnabled(True)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "Routes Info" + "</font>")
        if len(self.rt) == 0:
            self.feed.title.setText("<font color='white'>" + "No favorite destinations found!" + "</font>")

        counter = 0

        for route in self.rt:
            temp1 = QLabel("<font color='white'>" + route[1] + "</font>")
            temp1.setFont(news_source_font)
             # + self.news_data['articles'][i]['source']['name']
            temp2 = QLabel("<font color='white'>" + route[0] + "</font>")
            temp2.setFont(news_headline_font)
            temp3 = QLabel()
            temp3.setFont(news_space_font)
            # self.news_data['articles'][i]['source']['name']
            temp1.setAlignment(Qt.AlignLeft)
            self.feed.feedForm.addRow(temp2, temp1)
            self.feed.feedForm.addRow(temp3)

            counter = counter + 1
            if counter > 5:
                return

    def calendar_events(self):
        self.curr_app = 1
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        # self.calendar.setEnabled(False)
        # self.news.setEnabled(True)
        # self.routes.setEnabled(True)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "Calendar Events" + "</font>")

        if self.calendarEvents == None:
            self.feed.title.setText("<font color='white'>" + "No upcoming events!" + "</font>")
        else:
            num_of_events = len(self.calendarEvents)
            if num_of_events > 6:
                num_of_events = 6
            for i in range(num_of_events):
                event = self.calendarEvents[i]
                temp1 = QLabel("<font color='white'>" + event['summary'] + "</font>")
                temp1.setFont(news_headline_font)
                 # + self.news_data['articles'][i]['source']['name']
                temp2 = QLabel("<font color='white'>" + event['start'] + "</font>")
                temp2.setFont(news_source_font)
                temp3 = QLabel()
                temp3.setFont(news_space_font)
                # self.news_data['articles'][i]['source']['name']
                temp1.setAlignment(Qt.AlignLeft)
                self.feed.feedForm.addRow(temp2, temp1)
                self.feed.feedForm.addRow(temp3)


    def weather_info(self):
        effect = QGraphicsDropShadowEffect()
        effect.setOffset(1, 1)
        effect.setBlurRadius(30)
        effect.setColor(QColor(255,255,255))

        icon = icons[self.weather_dict['icon']]
        image = cv2.imread(icon)
        image = cv2.resize(image, (75, 75), interpolation=cv2.INTER_CUBIC)
        image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)

        # self.weather.daily = self.weather_dict['daily']['data'][0]['summary']
        self.weather.dailySummary.setText("<font color='white'>" + parseApiText(self.weather_dict['daily']) + "</font>")
        # print(self.weather_dict['daily'])

        # self.weather.curr = "Currently " + self.weather_dict['currently']['summary']
        self.weather.currently.setText("<font color='white'>" + parseApiText(self.weather_dict['current']) + "</font>")

        # self.weather.fahrenheit = self.weather_dict['currently']['temperature']
        self.weather.temp.setText("<font color='white'> %d" %self.weather_dict['temp'] + u'\N{DEGREE SIGN}' + "</font>")

        self.weather.icon.setFixedWidth(75)
        self.weather.icon.setFixedHeight(75)
        self.weather.icon.setAlignment(Qt.AlignCenter)
        self.weather.icon.setPixmap(QPixmap.fromImage(image))
#        self.weather.icon.frame = QFrame() # Not needed
#        self.weather.icon.setFrameShape(QFrame.Box)
#        self.weather.icon.setFrameShadow(QFrame.Raised)
#        self.weather.icon.setLineWidth(1)
#        self.weather.icon.setMidLineWidth(2)
#        self.weather.icon.setGraphicsEffect(effect)

    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def init_controller(self):
        self.cTimer = QTimer()
        self.cTimer.timeout.connect(self.controller)
        self.cTimer.start(1000)

    def update_time(self):
        datetime = QDateTime.currentDateTime()
        if self.qt.digitaltime != None:
            if self.qt.time != None:
                self.qt.time.setText("<font color='white'>" + datetime.toString("MMM d, yyyy hh:mm:ss AP") + "</font>")

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

    def check_google_code(self):
        with open('/home/pi/MirageSmartMirror/src/userCode.json') as f:
            data = json.load(f)
        dict = json.loads(data)
        return dict['hasCode']

    # Return False if timer still running, return True if timed out
    def googleCodeController(self):
        if self.googleCodeTimeout > 0:
            self.googleCodeTimeout = self.googleCodeTimeout - 1
            return False

        if self.check_google_code() == "True":
            with open('/home/pi/MirageSmartMirror/src/device_authorization.json') as f:
                dict = json.loads(f)
            #     data = json.load(f)
            # dict = json.loads(data)
            self.google_code = dict['userCode']
            self.show_auth_code()
            self.googleCodeTimeout = 10
            return False
       # elif self.google_prompt is True:
        #    self.google_code = None
         #   self.set_lockscreen_layout()
        return True

    # Function that takes a message and displays it on lockscreen. Keep for 5? seconds..
    def promptController(self):
        if self.loggedIn is False and self.promptTimeout == 0 and self.googleCodeTimeout == 0:
            self.prompt.setText("<font color='black'>" + "Blank" + "</font>")
        elif self.promptTimeout > 0:
            self.promptTimeout = self.promptTimeout - 1
        return

    def checkInternet(self):
        if get_wifi_status() is 0:
            self.changePrompt("No Internet connection! Use Mirage App to connect.")
            return 0
        else:
            return 1


    def controller(self):

        # Check internet connection
        if self.checkInternet() == 0:
            return

        # Check prompt message timeout
        self.promptController()
        # Step 1: Check google code controller. Displays lock screen if done!
        if self.googleCodeController() is False:
            return  # Displaying google code, so wait for timer to finish

        # Step 2: Read face detection status file
        #acquired = sema.acquire(blocking=True, timeout=1)
        #if acquired is True:
        with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json') as f:
            try:
                detectionStatusDictionary = json.load(f)
            except ValueError:
                return
         #       sema.release()
#        detectionStatusDictionary = data
        #else:
         #   return
        # Parse status dictionary
        if detectionStatusDictionary['username'] is None:
            self.loggedIn = False   # No face detected(reason unknown)
        else:
            self.loggedIn = True
            print("Now logged in at: " + str(time.asctime(time.localtime(time.time()))))

        self.userName = detectionStatusDictionary['username']

        self.isDetectingFace = detectionStatusDictionary['cameraOn']

        self.errorMessage = detectionStatusDictionary['error']

        self.detectCalled = detectionStatusDictionary['detectCalled']

        if self.errorMessage == "Face calibration":
            #TODO: Display calibration prompt, control LED?
            print("\"Face calibration is running now\" will be displayed")
            self.set_lockscreen_layout()
            self.changePrompt("Face calibration in progress!")
            return


        # Step 3: Check proximity value

        self.proximity = coProcessor.getProximity()
        print(self.proximity)
        print(detectionStatusDictionary)
        # Manual logout (proximity <= 10)
        if self.proximity <= 10:
            detectionStatusDictionary['username'] = None
            detectionStatusDictionary['error'] = None
            detectionStatusDictionary['cameraOn'] = False
            detectionStatusDictionary['detectCalled'] = False
            sema.acquire(blocking=True)
            with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as jsonFile:
                json.dump(detectionStatusDictionary, jsonFile)
            sema.release()
            self.set_lockscreen_layout()

        # User steps away (proximity >= 80)
        elif self.proximity >= 78:
            if self.loggedIn is True:
                # Start timer when user walks away for 10 seconds?
                if self.walkAwayTimeout == 0:
                    # Log the user out and reset timer
                    detectionStatusDictionary['username'] = None
                    detectionStatusDictionary['error'] = None
                    detectionStatusDictionary['cameraOn'] = False
                    detectionStatusDictionary['detectCalled'] = False
                    sema.acquire(blocking=True)
                    with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as jsonFile:
                        json.dump(detectionStatusDictionary, jsonFile)
                    sema.release()
                    self.set_lockscreen_layout()
                elif self.walkAwayTimeout < 0:
                    self.walkAwayTimeout = 10
                elif self.walkAwayTimeout >= 0:
                    self.walkAwayTimeout = self.walkAwayTimeout - 1


        # User in proximity(10 < proximity < 80)
        else:
            # Reset walk away timer
            self.walkAwayTimeout = -1
            # If detection is finished and no user logged in..
            if self.isDetectingFace is False and self.loggedIn is False:
                # Check error message
                if self.errorMessage == "Too many faces!":
                    self.changePrompt(self.errorMessage)
                    print("\"Too many faces\" will be displayed")
                    nothing = 0
                elif self.errorMessage == "Face not recognized!":
                    self.changePrompt(self.errorMessage)
                    print("\"New user\" will be displayed")
                    nothing = 0
                elif self.errorMessage == "No face detected!":
                    self.changePrompt(self.errorMessage)
                    print("\"No face detected\" will be displayed")
                    nothing = 0


                # Call face detection again
                # with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json') as f:
                #     data = json.load(f)
                #     if data['detectCalled'] is False:
                if not self.detectCalled and not self.loggedIn:
                    t = threading.Thread(target=detectFace)
                    t.start()
                    print("Detecting face now")
#                elif not self.isDetectingFace and not self.userName and not self.loggedIn:
 #                   detectionStatusDictionary['detectCalled'] = False
  #                  sema.acquire(blocking=True)
   #                 with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as jsonFile:
    #                    json.dump(detectionStatusDictionary, jsonFile)
     #                   sema.release()
                #subprocess.Popen("python3 simpleRec.py &", shell=True) #This creates multiple processes and overloads the pi

            # If fetection is finished and user logged in
            elif self.isDetectingFace is False and self.loggedIn is True:
                #Display main screen
                if self.curr_screen != 1:
                    print("Going to main screen")
                    # print(self.isDetectingFace)
                    # print(self.loggedIn)
                    self.msd()
                return

            # Camera is in use
            # elif self.isDetectingFace is True:
                #TODO: Increment timer (give camera time to try again)



        # if self.googleCodeTimeout > 0:
        #     self.googleCodeTimeout = self.googleCodeTimeout - 1
        #     return
        # else:
        #     self.prompt_asked = False
        #
        # if self.check_google_code() == "True":
        #     with open('/home/pi/MirageSmartMirror/src/userCode.json') as f:
        #         data = json.load(f)
        #     dict = json.loads(data)
        #     self.google_code = dict['userCode']
        #     self.google_prompt = True
        #     self.show_auth_code()
        #     self.googleCodeTimeout = 10
        #     return
        # elif self.google_prompt is True:
        #     self.google_code = None
        #     self.google_prompt = False
        #     self.set_lockscreen_layout()
        #
        # # if self.loggedIn is False:
        # #     self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()
        # # sensor.self.proximity()
        # # self.proximity = 300
        # if self.new_user_prompt is True:
        #     time.sleep(3)
        #     self.set_lockscreen_layout()
        #     self.new_user_prompt = False
        #     self.launch_face_detection = False
        #     self.googleCodeTimeout = 3
        #     return
        #
        #
        # if self.launch_face_detection is True and self.face_detection_countdown > 0:
        #     self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()
        #     print(self.numberOfDetectedFaces)
        #     self.face_detection_countdown = self.face_detection_countdown - 1
        #     self.launch_face_detection = False
        #     return
        # #elif self.loggedIn is False:
        #     #self.curr_screen = 0
        #     #self.set_lockscreen_layout()
        #
        # self.proximity = 70 #testSensor.getProximity()
        # print("Proximity value: %d" %self.proximity)
        #
        # if self.proximity > 50:
        #     if self.loggedIn is False:
        #         if self.prompt_asked is False:
        #             self.prompt.setText("<font color='white'>" + "Please stand still and wait for your profile to load." + "</font")
        #             self.prompt_asked = True
        #             self.set_buffering_screen()
        #         # self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()
        #             self.launch_face_detection = True
        #             self.face_detection_countdown = 3
        #         # self.set_buffering_screen()
        #
        #
        # if self.numberOfDetectedFaces == 1 and not self.loggedIn:
        #     print("one face Detected")
        #     self.launch_face_detection = False
        #     self.face_detection_countdown = 0
        #     name = recognize(self.faceFrame)
        #     print(name) #login
        #     if(name == "Unknown" or name is None):
        #         self.set_new_user_screen()
        #         self.new_user_prompt = True
        #     else:
        #         with open('/home/pi/MirageSmartMirror/src/Users/%s/%s.json' %(name, name)) as f:
        #             data = json.load(f)
        #
        #         dict = json.loads(data)
        #         self.curr_user = (name, dict)
        #         # print(self.curr_user["id"])
        #         # self.load_user_info(self.curr_user[0])
        #         self.msd()
        #         self.loggedIn = True
        #
        # elif self.numberOfDetectedFaces == 1 and self.loggedIn:
        #     print("one face and you are logged in")
        #     #if another user, start timer (5 sec) and switch to new profile
        #
        # elif self.numberOfDetectedFaces > 1:
        #     print("one person only")
        # else:
        #     #self.launch_face_detection = True
        #     print(self.loggedIn)
        #     print("no one is here")
        #     self.ExpirationTimerCount=self.ExpirationTimerCount+1
        #
        # if self.proximity > 50 and self.loggedIn is True:
        #     if self.curr_screen == 2:
        #         # self.load_user_info(self.curr_user[0])
        #         self.msd()
        # if self.proximity > 250 and self.loggedIn is True:
        #     if self.curr_screen == 1:
        #         self.set_lockscreen_layout()
        #
        # if self.ExpirationTimerCount >= 10:
        #     print("Time expired")
        #     self.set_lockscreen_layout()
        #     self.new_user_prompt = False
        #     self.launch_face_detection = False
        #     self.ExpirationTimerCount = 0

    def signalHandler1(self):
        # We got signal!
        # self.welcomeLabel.setText("<font color='white'>" + "Welcome, leftie!" + "</font>")
        current_app = self.appList[self.curr_app]
        current_app.graphicsEffect().setEnabled(False)
        if self.curr_app == 4:
            coProcessor.setLedWhiteFadeOut()
        self.curr_app = (self.curr_app - 1) % 5
        current_app = self.appList[self.curr_app]
        current_app.graphicsEffect().setEnabled(True)
        if self.curr_app == 0:
            self.msd()
        elif self.curr_app == 1:
            self.calendar_events()
        elif self.curr_app == 2:
            self.routes_info()
        elif self.curr_app == 3:
            self.news_headlines()
        elif self.curr_app == 4:
            self.gmd()
        print('Go left!')

    def signalHandler2(self):
        # We got signal!
        # self.welcomeLabel.setText("<font color='white'>" + "Welcome, rightie!" + "</font>")
        current_app = self.appList[self.curr_app]
        current_app.graphicsEffect().setEnabled(False)
        if self.curr_app == 4:
            coProcessor.setLedWhiteFadeOut()
        self.curr_app = (self.curr_app + 1) % 5
        current_app = self.appList[self.curr_app]
        current_app.graphicsEffect().setEnabled(True)
        if self.curr_app == 0:
            self.msd()
        elif self.curr_app == 1:
            self.calendar_events()
        elif self.curr_app == 2:
            self.routes_info()
        elif self.curr_app == 3:
            self.news_headlines()
        elif self.curr_app == 4:
            self.gmd()
        print('Go right!')

class keyboardListner(QThread):
    trigger1 = pyqtSignal()
    trigger2 = pyqtSignal()
    def on_press(self,key):
        if key == Key.left:
            self.trigger1.emit()
        if key == Key.right:
            self.trigger2.emit()
        # print('{0} pressed'.format(
            # key))

    def on_release(self,key):
        # print('{0} release'.format(
        #     key))
        if key == Key.esc:
            # Stop listener
            return False

    # Collect events until released

    def __init__(self, display):
        QThread.__init__(self)
        self.disp = display

    def run(self):
        self.trigger1.connect(self.disp.signalHandler1)
        self.trigger2.connect(self.disp.signalHandler2)
        # print("connected")
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()
        # self.trigger.emit()

    # def signalHandler1(self):
    #     # We got signal!
    #     print('Go left!')
    #
    # def signalHandler2(self):
    #     # We got signal!
    #     print('Go right!')
def parseApiText(str):
    index = str.find('(')
    if index >= 0:
        return str[:index]
    else:
        return str

def get_wifi_status() :
        # Check WiFi connectivity
        f = os.popen('iwgetid')
        now = f.read()
        if not now == '':
            #print("INTERNET IN API")
            return 1
        else:
            #print("NO INTERNET IN API")
            return 0

if __name__ == "__main__":
    #while get_wifi_status() is 0:
        #nothing = 0
    window_app = QApplication(sys.argv)
    Display = Window()


    # Create new thread object.
    thread = keyboardListner(Display)

    # Connect signalHandler function with some_signal which
    # will be emited by d thread object.

    # Start new thread.
    thread.start()


    sys.exit(window_app.exec_())
