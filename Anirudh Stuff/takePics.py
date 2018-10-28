from time import sleep
from picamera import PiCamera

def faceCalibration(name):
    camera = PiCamera()
    #camera.start_preview()
    sleep(2)
    for filename in camera.capture_continuous('./Users/%/img{counter:03d}.jpg' % name):
        print('Captured %s' % filename)
        sleep(2)
