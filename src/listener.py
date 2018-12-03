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
# for news
from newsapi import NewsApiClient
import requests
import json
#
from PyQt5.QtWidgets import *#QApplication, QWidget, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsDropShadowEffect, QSpacerItem, QGridLayout, QFormLayout
from PyQt5.QtGui import *#QFont, QPalette, QColor, QPainter, QPolygon
from PyQt5.QtCore import *
from simpleRec import *
from pynput.keyboard import Key, Listener


'''
<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
'''

# for i in range(10):
#     print(self.news_data['articles'][i]['title'])


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


class Window(QWidget):
    def __init__ (self):
        super().__init__()
        self.qt = QWidget()
        self.init_ui()
        # self.currentWidget = None

    def init_ui(self):

        # self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        # self.shortcut.activated.connect(self.ctrlO)

        self.qt.resize(800, 800)
        font = QFont('Helvetica', 18)
        font.setWeight(1)

        # Set background black
        self.darkPalette = QPalette()
        self.darkPalette.setColor(QPalette.Background, Qt.black)
        self.qt.setPalette(self.darkPalette)

        self.loggedIn = False
        self.ExpirationTimerCount = 0
        self.numberOfDetectedFaces = 0
        self.faceFrame = 0
        self.proximity = 300
        self.prompt_asked = False
        self.launch_face_detection = False
        self.new_user_prompt = False
        self.leave_counter = 0
        self.curr_user = -1

        self.set_lockscreen_layout()
        self.init_timer()
        self.init_controller()


        # with open('Users/user0/user0.json') as f:
        #     data = json.load(f)
        #
        # print("user info:")
        # print(data)

        self.qt.showFullScreen()

    def msd(self):
        self.loggedIn = True
        self.launch_face_detection = False
        self.clearLayout(self.qt.v_box)
        self.timer.stop()
        self.load_user_info(self.curr_user[0])

        # user_destinations = ["305 Swindon Way, West Lafayette, Indiana", "222 West Wood St, West Lafayette, Indiana", "West Madison Street, Chicago, Illinois"]
        # self.rt = maps.Maps("250 Sheetz Street, West Lafayette, Indiana", user_destinations)
        # self.calendarEvents = googleCalendar.Calendar() # fix to take in user id and get user's token

        self.qt.msb = QPushButton('Main screen')
        self.qt.gmb = QPushButton('Groom mode')
        self.qt.lsb = QPushButton('Lock screen')
        self.qt.l = QLabel()

        # Main screen layout
        self.TimeWeatherBox = QHBoxLayout()
        self.welcomeBox = QHBoxLayout()
        self.appListBox = QHBoxLayout()
        self.appBox = QHBoxLayout()

        ###
        # self.weather = weather.Weather()
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


        self.weather.setFixedHeight(150)
        self.TimeWeatherBox.addWidget(self.weather)
        self.weather_info()

        self.datetime = DateTime.DateTime()
        self.datetime.setFixedHeight(150)
        self.TimeWeatherBox.addWidget(self.datetime)

        ###
        self.welcomeLabel = QLabel("<font color='white'>" + "Welcome, %s!"%(self.curr_user[1]['name']) + "</font")
        self.welcomeLabel.setAlignment(Qt.AlignCenter)
        self.welcomeLabel.setFixedHeight(100)
        self.welcomeBox.addWidget(self.welcomeLabel)

        ###
        # self.feed = feeds.Feeds()
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

        self.qt.msb.clicked.connect(self.msd)
        self.qt.gmb.clicked.connect(self.gmd)
        self.qt.lsb.clicked.connect(self.set_lockscreen_layout)
        self.news.clicked.connect(self.news_headlines)
        self.calendar.clicked.connect(self.calendar_events)
        self.routes.clicked.connect(self.routes_info)

        # self.clearLayout(self.qt.v_box)

        self.qt.setWindowTitle('Main screen')
        self.qt.lsb = QPushButton('Lock screen')
        self.qt.lsb.clicked.connect(self.set_lockscreen_layout)
        self.qt.v_box.addWidget(self.qt.lsb)
        self.qt.v_box.addLayout(self.TimeWeatherBox)

        self.qt.v_box.addLayout(self.appBox)
        self.qt.v_box.addLayout(self.welcomeBox)
        self.qt.v_box.addSpacing(200)
        self.qt.v_box.addLayout(self.appListBox)
        self.proximity = 300

        # temp = DateTime.DateTime()
        # self.qt.v_box = temp

    def gmd(self):
        self.timer.stop()
        self.clearLayout(self.qt.v_box)

        self.qt.v_box.addWidget(self.qt.lsb)
        self.qt.v_box.addWidget(groom.Groom().frame)
        self.qt.v_box.setContentsMargins(0,0,0,0)
        self.proximity = 1000

    def set_buffering_screen(self):
        self.clearLayout(self.qt.v_box)
        self.timer.stop()
        prompt_box = QHBoxLayout()
        self.prompt = QLabel("<font color='white'>" + "Please stand still while we detect your face and load your profile." + "</font")
        self.prompt.setAlignment(Qt.AlignCenter)
        prompt_box.addWidget(self.prompt)
        self.qt.layout().addLayout(prompt_box)
        # self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()

    def set_new_user_screen(self):
        self.clearLayout(self.qt.v_box)
        # self.timer.stop()
        prompt_box = QHBoxLayout()
        self.prompt = QLabel("<font color='white'>" + "Face not recognized! Please download our MirageCompanion iPhone App to set up a new profile." + "</font")
        self.prompt.setAlignment(Qt.AlignCenter)
        prompt_box.addWidget(self.prompt)
        self.qt.layout().addLayout(prompt_box)

    def load_user_info(self, user_name):
        # os.system('nohup python3 APIs.py &')
        # user_destinations = ["305 Swindon Way, West Lafayette, Indiana", "222 West Wood St, West Lafayette, Indiana", "West Madison Street, Chicago, Illinois"]
        file_path = "Users/%s/%sAPI.json" %(user_name, user_name)
        with open(file_path) as f:
            user_dict = json.load(f)

        self.rt = user_dict['map']
        self.calendarEvents = user_dict['events']
        self.weather_dict = user_dict['weather']
        self.datetime = DateTime.DateTime()
        self.feed = feeds.Feeds()
        self.news_data = user_dict['news']
        # Init
        # newsapi = NewsApiClient(api_key='33ff7834a7ee40928e7bb90746c8b6e5')
        # # top_headlines = newsapi.get_top_headlines(category=user_dict["newsCategories"][0]
        # #                                         language='en',
        # #                                           country='us')
        # news_sources = newsapi.get_sources()
        # news_url = ('https://newsapi.org/v2/top-headlines?'
        #        'category=%s&'
        #        'country=us&'
        #        'apiKey=33ff7834a7ee40928e7bb90746c8b6e5' %(user_dict["newsCategories"][0]))
        # # print(news_url)
        # news_response = requests.get(news_url)
        # self.news_data = news_response.json()
        # print(self.news_data)




    def set_lockscreen_layout(self):
        # self.init_timer()
        self.loggedIn = False
        self.numberOfDetectedFaces = 0
        # self.prompt_asked = False
        # self.launch_face_detection = False
        font = QFont('Helvetica', 18)
        font.setWeight(1)
        effect = QGraphicsDropShadowEffect()
        effect2 = QGraphicsDropShadowEffect()
        effect.setOffset(1, 1)
        effect2.setOffset(1, 1)
        effect.setBlurRadius(30)
        effect.setColor(QColor(255,255,255))
        effect2.setBlurRadius(20)
        effect2.setColor(QColor(255,255,255))

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
        self.qt.h_box.addWidget(self.qt.msb)

        prompt_box = QHBoxLayout()
        self.prompt = QLabel()
        self.prompt.setFixedHeight(30)
        self.prompt.setAlignment(Qt.AlignCenter)
        # self.prompt.setGraphicsEffect(effect2)
        prompt_box.addWidget(self.prompt)


        if self.qt.layout() != None:
            self.clearLayout(self.qt.v_box)
            self.qt.layout().addLayout(self.qt.h_box)
            self.qt.layout().addSpacing(150)
            self.qt.layout().addLayout(self.qt.analogclock)
            self.qt.layout().addLayout(self.qt.digitaltime)
            self.qt.layout().addLayout(prompt_box)
            self.init_timer()
        else:
            self.qt.v_box = QVBoxLayout()
            self.qt.v_box.addLayout(self.qt.h_box)
            self.qt.v_box.addSpacing(150)
            self.qt.v_box.addLayout(self.qt.analogclock)
            self.qt.v_box.addLayout(self.qt.digitaltime)
            self.qt.v_box.addLayout(prompt_box)
            self.qt.setLayout(self.qt.v_box)
            self.init_timer()

        self.qt.setWindowTitle('Lock screen')



    def news_headlines(self):
        self.clearLayout(self.feed.feedForm)
        self.clearLayout(self.welcomeBox)
        self.calendar.setEnabled(True)
        self.news.setEnabled(False)
        self.routes.setEnabled(True)

        self.feed.title.setFont(font)
        self.feed.title.setText("<font color='white'>" + "News Headlines" + "</font>")

        for i in range(6):
            temp1 = QLabel("<font color='white'>" + self.news_data['articles'][i]['title'] + "." + "</font")
            temp1.setFont(news_headline_font)
             # + self.news_data['articles'][i]['source']['name']
            temp2 = QLabel("<font color='white'>" + self.news_data['articles'][i]['source']['name'] + "</font")
            temp2.setFont(news_source_font)
            temp3 = QLabel()
            temp3.setFont(news_space_font)
            # self.news_data['articles'][i]['source']['name']
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

        for route in self.rt:
            temp1 = QLabel("<font color='white'>" + route[1] + "</font")
            temp1.setFont(news_source_font)
             # + self.news_data['articles'][i]['source']['name']
            temp2 = QLabel("<font color='white'>" + route[0] + "</font")
            temp2.setFont(news_headline_font)
            temp3 = QLabel()
            temp3.setFont(news_space_font)
            # self.news_data['articles'][i]['source']['name']
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

        if self.calendarEvents == None:
            self.feed.title.setText("<font color='white'>" + "No upcoming events!" + "</font")
        else:
            for i in range(6):
                event = self.calendarEvents[i]
                temp1 = QLabel("<font color='white'>" + event['summary'] + "</font")
                temp1.setFont(news_headline_font)
                 # + self.news_data['articles'][i]['source']['name']
                temp2 = QLabel("<font color='white'>" + event['start'] + "</font")
                temp2.setFont(news_source_font)
                temp3 = QLabel()
                temp3.setFont(news_space_font)
                # self.news_data['articles'][i]['source']['name']
                temp1.setAlignment(Qt.AlignLeft)
                self.feed.feedForm.addRow(temp2, temp1)
                self.feed.feedForm.addRow(temp3)

    def weather_info(self):
        icon = icons[self.weather_dict['icon']]
        image = cv2.imread(icon)
        image = cv2.resize(image, (50, 50), interpolation=cv2.INTER_CUBIC)
        image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)

        # self.weather.daily = self.weather_dict['daily']['data'][0]['summary']
        self.weather.dailySummary.setText("<font color='white'>" + self.weather_dict['daily'] + "</font")

        # self.weather.curr = "Currently " + self.weather_dict['currently']['summary']
        self.weather.currently.setText("<font color='white'>" + self.weather_dict['current'] + "</font")

        # self.weather.fahrenheit = self.weather_dict['currently']['temperature']
        self.weather.temp.setText("<font color='white'> %d" %self.weather_dict['temp'] + u'\N{DEGREE SIGN}' + "</font")

        self.weather.icon.setPixmap(QPixmap.fromImage(image))




    def init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def init_controller(self):
        self.cTimer = QTimer()
        self.cTimer.timeout.connect(self.controller)
        self.cTimer.start(3000)

    def update_time(self):
        datetime = QDateTime.currentDateTime()
        if self.qt.digitaltime != None:
            if self.qt.time != None:
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

        if self.leave_counter > 0:
            self.leave_counter = self.leave_counter - 1
            return
        else:
            self.prompt_asked = False

        # if self.loggedIn is False:
        #     self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()
        # sensor.self.proximity()
        # self.proximity = 300
        if self.new_user_prompt is True:
            time.sleep(5)
            self.set_lockscreen_layout()
            self.new_user_prompt = False
            self.launch_face_detection = False
            self.leave_counter = 3
            return

        # print(self.launch_face_detection)
        # print(self.prompt_asked)

        if self.launch_face_detection is True:
            self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()
            self.launch_face_detection = False

        if self.proximity > 200:
            if self.loggedIn is False:
                if self.prompt_asked is False:
                    self.prompt.setText("<font color='white'>" + "Please stand still and wait for your profile to load." + "</font")
                    self.prompt_asked = True
                    self.set_buffering_screen()
                # self.numberOfDetectedFaces,self.faceFrame = numberOfFaces()
                    self.launch_face_detection = True
                # self.set_buffering_screen()

            if self.numberOfDetectedFaces == 1 and not self.loggedIn:
                print("one face Detected")
                name = recognize(self.faceFrame)
                print(name) #login
                if(name == "Unknown"):
                    self.set_new_user_screen()
                    self.new_user_prompt = True
                    # self.launch_face_detection = True
                    # self.prompt_asked = False
                    # time.sleep(6)
                    # self.set_lockscreen_layout()
                else:
                    with open('Users/%s/%s.json' %(name, name)) as f:
                        data = json.load(f)
                    dict = json.loads(data)
                    # print(data)
                    # print("user info:")
                    self.curr_user = (name, dict)
                    print(self.curr_user)
                    # print(self.curr_user["id"])
                    self.load_user_info(self.curr_user[0])
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
                self.launch_face_detection = True
                print("no one is here")
                self.ExpirationTimerCount=self.ExpirationTimerCount+1

                    #change ui to lock screen

                #please one person in front
        if self.proximity > 600:
            self.ExpirationTimerCount=self.ExpirationTimerCount+1
            # self.load_user_info(0)
            # self.msd()

        if self.ExpirationTimerCount >= 3:
            print("Time expired")
            self.set_lockscreen_layout()
            self.new_user_prompt = False
            self.launch_face_detection = False
            self.ExpirationTimerCount = 0

    def signalHandler1(self):
        # We got signal!
        print('Go left!')

    def signalHandler2(self):
        # We got signal!
        print('Go right!')

class DoSomething(QThread):
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


if __name__ == "__main__":
    window_app = QApplication(sys.argv)
    Display = Window()


    # Create new thread object.
    d = DoSomething(Display)

    # Connect signalHandler function with some_signal which
    # will be emited by d thread object.

    # Start new thread.
    d.start()


    sys.exit(window_app.exec_())
