import face_recognition
import imutils
from imutils.video import VideoStream
import cv2
import pickle
import time
import os
import subprocess
import json
import threading
import coProcessor
import time
import picamera
import numpy as np



# for LED
# import setLed

calibrationCancel = False

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
# def recognize(rgb_small_frame):

	# data = pickle.loads(open("/home/pi/MirageSmartMirror/src/faceRecognitionEncodings/encodings", "rb").read())
	#
	# # Create arrays of known face encodings and their names
	# known_face_encodings = data['encodings']
	#
	# known_face_names = data['names']
	#
	# # Initialize some variables
	# face_locations = []
	# face_encodings = []
	# face_names = []
	# process_this_frame = True
	#
	# # Find all the faces and face encodings in the current frame of video
	# face_locations = face_recognition.face_locations(rgb_small_frame)
	# face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
	#
	# face_names = []
	# for face_encoding in face_encodings:
	#	 # See if the face is a match for the known face(s)
	#	 matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
	#	 name = "Unknown"
	#
	#	 # If a match was found in known_face_encodings, just use the first one.
	#	 if True in matches:
	#		 # find the indexes of all matched faces then initialize a
	#		 # dictionary to count the total number of times each face
	#		 # was matched
	#		 matchedIdxs = [i for (i, b) in enumerate(matches) if b]
	#		 counts = {}
	#
	#		 # loop over the matched indexes and maintain a count for
	#		 # each recognized face face
	#		 for i in matchedIdxs:
	#		 	name = data["names"][i]
	#		 	counts[name] = counts.get(name, 0) + 1
	#
	#		 # determine the recognized face with the largest number of
	#		 # votes (note: in the event of an unlikely tie Python will
	#		 # select first entry in the dictionary)
	#		 name = max(counts, key=counts.get)
	#	 if name is None:
	#		 name = "Unknown"
	#	 print("In recognize:")
	#	 print(name)
	#	 return name

	# Release handle to the webcam


# def numberOfFaces():
# # Get a reference to webcam #0 (the default one)
#	 video_capture = cv2.VideoCapture(0)
#	 time.sleep(0.5)
#
#	 # import ipdb; ipdb.set_trace() # BREAKPOINT
#	 process_this_frame = True
#
#
#	 # Grab a single frame of video
#	 ret, frame = video_capture.read()
#
#	 # Resize frame of video to 1/4 size for faster face recognition processing
#	 small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#
#	 # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#	 rgb_small_frame = small_frame[:, :, ::-1]
#
#
#	 # Find all the faces and face encodings in the current frame of video
#	 numberOfFaces = len(face_recognition.face_locations(rgb_small_frame))
#	 # cv2.imshow('Video', frame)
#	 video_capture.release()
#	 cv2.destroyAllWindows()
#
#
#	 return numberOfFaces,rgb_small_frame

sema = threading.Semaphore()

def detectFace():
	global sema
	# Turn on LED
	#setLed.ledON()
	jsonData = {}

	with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'r') as testData:
		jsonData = json.load(testData)
		if jsonData['username'] is not None:
			return

	#vs =  VideoStream(usePiCamera=True).start()
	jsonData = {
		'username':None,
		'error':None,
		'cameraOn':True,
		'detectCalled':True
	}
	sema.acquire(blocking=True)
	with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
		json.dump(jsonData, outfile)
		sema.release()

	# Set Green LED on
	coProcessor.setLedGreenFadeIn()
	vs = VideoStream(usePiCamera=True)
	vs.start()
	time.sleep(1)
	# with picamera.PiCamera() as camera:
	# 	camera.resolution = (320, 240)
	# 	camera.framerate = 24
	# 	time.sleep(2)
	# 	camera.start_preview()
	# 	frame = np.empty((240, 320, 3), dtype=np.uint8)
	# 	camera.capture(frame, 'rgb')
	# 	# Turn off LED
	# 	camera.stop_preview()

	#wite to file to signal that Camera is on

		#print(jsonData)
	# construct the argument parser and parse the arguments
	# load the known faces and embeddings along with OpenCV's Haar
	# cascade for face detection
	detector = cv2.CascadeClassifier("/home/pi/MirageSmartMirror/src/haar_face_cascade.xml")
	# initialize the video stream and allow the camera sensor to warm up
	#vs = VideoStream(src=0).start()
	#vs = VideoStream(usePiCamera=True).start()

	# start the FPS counter

	# loop over frames from the video file stream
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
	frame = vs.read()
	#rgb = cv2.rotate(frame, rotateCode=cv2.ROTATE_180) # Tried to rotate image - Amjad
	# print(frame)
	#cv2.imshow('video', frame)
	frame = imutils.resize(frame, width=500)

	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	# detect faces in the grayscale frame
	print("Detecting faces in greyscale frame: " + str(time.asctime(time.localtime(time.time()))))

	rects = detector.detectMultiScale(gray, scaleFactor=1.1,
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
	vs.stop()
	# Set green LED off
	coProcessor.setLedGreenFadeOut()

	jsonData = {
		'username':None,
		'error':None,
		'cameraOn':False,
		'detectCalled':True
	}
	sema.acquire(blocking=True)
	with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
		json.dump(jsonData, outfile)
		sema.release()

	if (len(rects)== 0):
		jsonData = {
			'username':None,
			'error':'No face detected',
			'cameraOn':False,
			'detectCalled':False
		}
		sema.acquire(blocking=True)
		with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
			json.dump(jsonData, outfile)
			print(jsonData)
			sema.release()
			return
	elif (len(rects) > 1):
		jsonData = {
			'username':None,
			'error':'Too many faces',
			'cameraOn':False,
			'detectCalled':False
		}
		sema.acquire(blocking=True)
		with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
			json.dump(jsonData, outfile)
			print(jsonData)
			sema.release()
			return

	print("faceDetected")
	print("Face detected at: " + str(time.asctime(time.localtime(time.time()))))

	data = pickle.loads(open("/home/pi/MirageSmartMirror/src/faceRecognitionEncodings/encodings", "rb").read())

	# Create arrays of known face encodings and their names
	known_face_encodings = data['encodings']
#	print("Number of Known Face Encodings: " + str(len(known_face_encodings)))
	known_face_names = data['names']
#	print("Number of Known Encoded Names: " + str(len(known_face_names)) + ": " + str(known_face_names))

	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	# Find all the faces and face encodings in the current frame of video
	print("Getting face_locations: " + str(time.asctime(time.localtime(time.time()))))
	#face_locations = face_recognition.face_locations(rgb)
#	print("Face Locations: " + str(face_locations))
	print("Getting face encodings: " + str(time.asctime(time.localtime(time.time()))))

	face_encodings = face_recognition.face_encodings(rgb, boxes)

	face_names = []
#	print("Number of Face Encodings: " + str(len(face_encodings)))
	print("Going into face recognition loop: " + str(time.asctime(time.localtime(time.time()))))
	for face_encoding in face_encodings:
		print("Found an encoding")
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		name = None

		# If a match was found in known_face_encodings, just use the first one.
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number of
			# votes (note: in the event of an unlikely tie Python will
			# select first entry in the dictionary)
			name = max(counts, key=counts.get)
		if name is None:
			jsonData = {
				'username':None,
				'error':'Face unknown',
				'cameraOn':False,
				'detectCalled':False
			}

			sema.acquire(blocking=True)
			with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
				json.dump(jsonData, outfile)
				print(jsonData)
				sema.release()
				return

		jsonData = {
			'username':name,
			'error':'Found',
			'cameraOn':False,
			'detectCalled':False
		}
		sema.acquire(blocking=True)
		with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
			json.dump(jsonData, outfile)
			print("User Found: " + str(jsonData) + " at time " + time.asctime(time.localtime(time.time())))
			print(str(threading.get_ident()))
			sema.release()
			return
	jsonData = {
		'username':None,
		'error':None,
		'cameraOn':False,
		'detectCalled':False
	}
	sema.acquire(blocking=True)
	with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
		json.dump(jsonData, outfile)
		sema.release()

def faceCalibration(name):


	coProcessor.initProximity() # If not running thru window.py
	# camera.start_preview()
	#path = "./Users/%s/" % name
	# camera = PiCamera()
	#simpleRec.vs.start()
	path = "/home/pi/MirageSmartMirror/src/Users/%s/" % name
	try:
		os.mkdir(path)
	except OSError:
		print ("Creation of the directory %s failed" % path)
	else:
		print ("Successfully created the directory %s " % path)

	#Turn on LED
	#setLed.ledON()
	coProcessor.setLedGreenFadeIn()
	with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json') as json_file:
		jsonData = json.load(json_file)
		jsonData['error'] = "Face calibration"
		jsonData['cameraOn'] = True
	with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
		json.dump(jsonData, outfile)
	with picamera.PiCamera() as camera:
		camera.resolution = (320, 240)
		camera.framerate = 24
		time.sleep(2)
		frame = np.empty((240, 320, 3), dtype=np.uint8)
		for i in range(5):
			if not (calibrationCancel):
				time.sleep(2)
				# camera.capture('/home/pi/MirageSmartMirror/src/Faces/%s/image%s.jpg' % (name , i))
				camera.capture(frame, 'rgb')
				coProcessor.setLedGreenFadeIn()
				#frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180) # Tried to rotate image - Amjad
				pathImage = '/home/pi/MirageSmartMirror/src/Users/%s/image%s.jpg' % (name , i)
				cv2.imwrite( pathImage,frame );
		# camera.stop_preview()
			else:
				break
		# Turn off LED
		#setLed.ledOFF()
		coProcessor.setLedGreenFadeOut()
		jsonData['cameraOn'] = False
		jsonData['error'] = None
		with open('/home/pi/MirageSmartMirror/src/faceDetectStatus.json', 'w') as outfile:
			json.dump(jsonData, outfile)


	#subprocess.call("python3 /home/pi/MirageSmartMirror/src/faceEncoding.py &", shell=True)
	return
	# if res.returncode == 0:
	#	 print("Encoding done!")
	# else:
	#	 print("Encoding failed!")
	# #Turn off LED
	# setLed.ledOFF()
#faceCalibration("Andrew0")
def cancelCalibration():
	calibrationCancel = True


if __name__ == "__main__":
	#while(True):
	#	detectFace()
	#	time.sleep(3)
	coProcessor.initProximity()
	faceCalibration("user2")

	nothing = 0
	#detectFace()
