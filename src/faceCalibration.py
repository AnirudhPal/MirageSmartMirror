from time import sleep
from picamera import PiCamera
import simpleRec
import os

calibrationCancel = False


def faceCalibration(name):
    # camera.start_preview()
    #path = "./Users/%s/" % name
    # camera = PiCamera()
    # simpleRec.vs.start()
    sleep(2)
    path = "/home/pi/MirageSmartMirror/src/Faces/%s/" % name
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    for i in range(5):
        if not (calibrationCancel):
            sleep(2)
            # camera.capture('/home/pi/MirageSmartMirror/src/Faces/%s/image%s.jpg' % (name , i))
            frame = simpleRec.vs.read()
            pathImage = '/home/pi/MirageSmartMirror/src/Faces/%s/image%s.jpg' % (name , i)
            simpleRec.cv2.imwrite( pathImage,frame );
    # camera.stop_preview()
        else:
            break
    #simpleRec.vs.stop()
faceCalibration("ali12")
#faceCalibration("Andrew0")
def cancelCalibration():
    calibrationCancel = True
