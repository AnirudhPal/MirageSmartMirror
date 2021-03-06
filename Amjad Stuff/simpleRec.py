import face_recognition
from imutils.video import VideoStream
import imutils
import cv2
import pickle
import time

vs = VideoStream(usePiCamera=True).start()

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
def recognize(rgb_small_frame):

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
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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

        return name

    # Release handle to the webcam


# def numberOfFaces():
# # Get a reference to webcam #0 (the default one)
#     video_capture = cv2.VideoCapture(0)
#     time.sleep(0.5)
#
#     # import ipdb; ipdb.set_trace() # BREAKPOINT
#     process_this_frame = True
#
#
#     # Grab a single frame of video
#     ret, frame = video_capture.read()
#
#     # Resize frame of video to 1/4 size for faster face recognition processing
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#
#     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#     rgb_small_frame = small_frame[:, :, ::-1]
#
#
#     # Find all the faces and face encodings in the current frame of video
#     numberOfFaces = len(face_recognition.face_locations(rgb_small_frame))
#     # cv2.imshow('Video', frame)
#     video_capture.release()
#     cv2.destroyAllWindows()
#
#
#     return numberOfFaces,rgb_small_frame
def numberOfFaces():
	#vs =  VideoStream(usePiCamera=True).start()

# construct the argument parser and parse the arguments
	# load the known faces and embeddings along with OpenCV's Haar
	# cascade for face detection
	detector = cv2.CascadeClassifier("/home/pi/MirageSmartMirror/src/haar_face_cascade.xml")
	# initialize the video stream and allow the camera sensor to warm up
	#print("[INFO] starting video stream...")
	#vs = VideoStream(src=0).start()
	#vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# start the FPS counter

	# loop over frames from the video file stream
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
	frame = vs.read()
	#print(frame)
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
	#vs.stop()
	return len(rects),rgb
#print(numberOfFaces())
