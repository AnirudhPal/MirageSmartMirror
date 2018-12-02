import face_recognition
from imutils.video import VideoStream
import imutils
import cv2
import pickle
import time
import os
import subprocess

# for LED
import setLed

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
def detectFace():
	# Turn on LED
	setLed.ledON()


	#vs =  VideoStream(usePiCamera=True).start()
	vs = VideoStream(usePiCamera=True)
	vs.start()

	#wite to file to signal that Camera is on
	data['status'] = [{
		'username':None,
		'error':'no face detected',
		'cameraOn':'True'
	}]
	with open('faceDetectStatus.json', 'w') as outfile:
		json.dump(data, outfile)
# construct the argument parser and parse the arguments
	# load the known faces and embeddings along with OpenCV's Haar
	# cascade for face detection
	detector = cv2.CascadeClassifier("/home/pi/MirageSmartMirror/src/haar_face_cascade.xml")
	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	#vs = VideoStream(src=0).start()
	#vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# start the FPS counter

	# loop over frames from the video file stream
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
	frame = vs.read()
	frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180) # Tried to rotate image - Amjad
	# print(frame)
	#cv2.imshow('video', frame)
	frame = imutils.resize(frame, width=500)

	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1,
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)
	vs.stop()
	# Turn off LED
	setLed.ledOFF()
	if (len(rects)== 0):
		data['status'] = [{
			'username':None,
			'error':'no face detected',
			'cameraOn':'False'
		}]
		with open('faceDetectStatus.json', 'w') as outfile:
			json.dump(data, outfile)
		return
	elif (len(rects) > 1):
		data['status'] = [{
			'username':None,
			'error':'To many faces',
			'cameraOn':'False'
		}]
		with open('faceDetectStatus.json', 'w') as outfile:
			json.dump(data, outfile)
		return

	data = pickle.loads(open("/home/pi/MirageSmartMirror/src/faceRecognitionEncodings/encodings", "rb").read())

	# Create arrays of known face encodings and their names
	known_face_encodings = data['encodings']

	known_face_names = data['names']

	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	# Find all the faces and face encodings in the current frame of video
	face_locations = face_recognition.face_locations(rgb)
	face_encodings = face_recognition.face_encodings(rgb, face_locations)

	face_names = []
	for face_encoding in face_encodings:
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		name = "Unknown"

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
			data['status'] = [{
				'username':None,
				'error':'Face unknown',
				'cameraOn':'False'
			}]
			with open('faceDetectStatus.json', 'w') as outfile:
				json.dump(data, outfile)
			return

		data['status'] = [{
			'username':name,
			'error':'Found',
			'cameraOn':'False'
		}]
		with open('faceDetectStatus.json', 'w') as outfile:
			json.dump(data, outfile)
		return

def faceCalibration(name):
	#Turn on LED
	setLed.ledON()
	vs = VideoStream(usePiCamera=True)

	# camera.start_preview()
	#path = "./Users/%s/" % name
	# camera = PiCamera()
	#simpleRec.vs.start()
	vs.start()
	time.sleep(2)
	path = "/home/pi/MirageSmartMirror/src/Users/%s/" % name
	try:
		os.mkdir(path)
	except OSError:
		print ("Creation of the directory %s failed" % path)
	else:
		print ("Successfully created the directory %s " % path)

	for i in range(5):
		if not (calibrationCancel):
			time.sleep(2)
			# camera.capture('/home/pi/MirageSmartMirror/src/Faces/%s/image%s.jpg' % (name , i))
			frame = vs.read()
			frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180) # Tried to rotate image - Amjad
			pathImage = '/home/pi/MirageSmartMirror/src/Users/%s/image%s.jpg' % (name , i)
			cv2.imwrite( pathImage,frame );
	# camera.stop_preview()
		else:
			break
	vs.stop()
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
	detectFace()
	nothing = 0
