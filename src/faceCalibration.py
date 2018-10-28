from time import sleep
from picamera import PiCamera

def faceCalibration:
    camera = PiCamera()
    camera.start_preview()
    for i in range(5):
        sleep(5)
        camera.capture('./Users/%/image%s.jpg' % (name , i))
    camera.stop_preview()
    
faceCalibration("Andrew0")
