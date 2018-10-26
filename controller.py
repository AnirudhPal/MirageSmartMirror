# import board
# import busio
# import adafruit_apds9960.apds9960
from simpleRec import *

# i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
#
# sensor.enable_proximity = True

# import ipdb; ipdb.set_trace()
loggedIn = False

#create proximity sensor

while True:
    numberOfDetectedFaces = int(numberOfFaces())
    # sensor.proximity()
    proximity = 300
    if proximity > 200:

        if numberOfDetectedFaces == 1 and not loggedIn:
            print("one face Detected")
            print(recognize()) #login
            #if unknown ask if user wants to setup a new profile
                #setup profile Protocal

            #if recognize retuned a name login
                #loggedIn = True
                #diSplAY
        elif numberOfDetectedFaces == 1 and loggedIn:
            print(1);
            #if another user, start timer (5 sec) and switch to new profile

        elif numberOfDetectedFaces > 1:
            print("one person only")
            #please one person in front
    if proximity > 600:
        loggedIn = False
        #log out z
