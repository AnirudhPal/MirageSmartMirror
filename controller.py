# import board
# import busio
# import adafruit_apds9960.apds9960
from simpleRec import *
import time


# i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
#
# sensor.enable_proximity = True

# import ipdb; ipdb.set_trace()
loggedIn = False
ExpariationTimerCount = 0

#create proximity sensor

while True:
    time.sleep(3)
    numberOfDetectedFaces,faceFrame = numberOfFaces()
    # sensor.proximity()
    proximity = 300
    if proximity > 200:

        if numberOfDetectedFaces == 1 and not loggedIn:
            print("one face Detected")
            print(recognize(faceFrame)) #login
            #if unknown ask if user wants to setup a new profile
                #setup profile Protocal

            #if recognize retuned a name login
                #loggedIn = True
                #diSplAY
        elif numberOfDetectedFaces == 1 and loggedIn:
            print("one face and you are logged in")
            #if another user, start timer (5 sec) and switch to new profile

        elif numberOfDetectedFaces > 1:
            print("one person only")
        else :
            print("no one is here")
            ExpariationTimerCount++;

                #change ui to lock screen

            #please one person in front
    if proximity > 600:
        print("no one is here")
        ExpariationTimerCount++;

    if ExpariationTimerCount >= 10:
        loggedIn = False
