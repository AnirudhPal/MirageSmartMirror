from time import sleep
from picamera import PiCamera
import os

def faceCalibration(name):
    camera = PiCamera()
    # camera.start_preview()
    path = "./Users/%s/" % name
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    for i in range(5):
        sleep(5)
        camera.capture('./Users/%s/image%s.jpg' % (name , i))
    # camera.stop_preview()

faceCalibration("Andrew0")
