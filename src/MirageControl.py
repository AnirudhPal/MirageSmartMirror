from flask import Flask
from flask import request
import subprocess
import os
import json
import simpleRec
import GoogleAuth
import APIs

app = Flask(__name__)

M_USER_DIR = "/home/pi/MirageSmartMirror/src/Users/"

selected_user = 0
numUsers = 0

def get_num_users_plain():
	files = os.listdir("/home/pi/MirageSmartMirror/src/Users")
	return len(files)

# Get number of users
@app.route('/user/getnum')
def get_num_users():
	global numUsers
	files = os.listdir("/home/pi/MirageSmartMirror/src/Users")
	numUsers = len(files)
	return str(numUsers)


@app.route('/user/add', methods=['POST'])
def add_user():
	error = None
	#print(request.get_json())
	if request.method == "POST":
		next_user_num = get_num_users_plain()
		dirName = M_USER_DIR + "user" + str(next_user_num)
		filename = M_USER_DIR + "user" + str(request.json['user_info']['id']) + "/" + "user" + str(request.json['user_info']['id']) + ".json"
	else:
		print("Method is not post")
	with open(filename, 'w') as f:
		f.write("\"" + str(request.json['user_info']).replace('\'', '\\"') + '\"')

#	f = open(filename, "w")
#	f.write("\"" + str(request.json['user_info']).replace('\'', '\\"') + '\"')
	APIs.pullApi("user" + str(request.json['user_info']['id']))
	return "User successfully added"

# Get user by number
@app.route('/user/get/<user_number>')
def get_user(user_number):
	filename = M_USER_DIR + "user" + user_number + "/user" + user_number + ".json"
	with open(filename, 'r') as json_data:
		try:
			data = json.load(json_data)
			return data
		except:
			return "Unable to access user, might not exist"

# Update user by number
@app.route('/user/update', methods=['POST'])
def update_user():
	error = None
	#print(request.get_json())
	if request.method == "POST":
		next_user_num = get_num_users_plain()
		#dirName = M_USER_DIR + "user" + str(next_user_num)
		filename = M_USER_DIR + "user" + str(request.json['user_info']['id']) + "/" + "user" + str(request.json['user_info']['id']) + ".json"
	else:
		print("Method is not post")

	with open(filename, 'w') as f:
		f.write("\"" + str(request.json['user_info']).replace('\'', '\\"') + '\"')

#	f = open(filename, "w")
#	f.write("\"" + str(request.json['user_info']).replace('\'','\\"') + '\"')
	APIs.pullApi("user" + str(request.json['user_info']['id']))
	return "User successfully updated"

#	with open(filename, 'w') as outfile:
#		try:
#			json.dump(request.json['user_info'], outfile, ensure_ascii=False)
#			return "User successfully updated"
#		except:
#			return "User could not be updated"

# Delete user by number
@app.route('/user/delete/<user_number>')
def delete_user(user_number):
	file_to_delete = M_USER_DIR + "user" + user_number + "/user" + user_number + ".json"
	if (os.path.exists(file_to_delete)):
		os.remove(file_to_delete)
		print("User removed")
	else:
		return "User not found"

	new_num_users = get_num_users_plain()
	files = os.listdir("/home/pi/MirageSmartMirror/src/Users")
	for i in range(new_num_users):
		os.rename(M_USER_DIR + files[i], M_USER_DIR + files[i]+".temp")


	for j in range(new_num_users):
		os.rename(M_USER_DIR + files[j] + ".temp", M_USER_DIR + "user" + str(j) + ".json")


	return "User deleted and files updated"

# Setup user for face calibration
@app.route('/setup/newuser/<filename>')
def start_face_calibration(filename):
	simpleRec.faceCalibration(filename)
	print("Done")
	subprocess.call("python3 /home/pi/MirageSmartMirror/src/faceEncoding.py &", shell=True)
	return "Done"

# Cancel face calibration
@app.route('/setup/cancel')
def cancel_face_calibration():
	cancelCalibration()

# Start Google Calendar Authorization
@app.route('/user/authorize/google/<filename>')
def start_google_auth(filename):
	res = GoogleAuth.getDeviceAuthorization()
	if res == True:
		print("Device Successfully requested Authorization")
		GoogleAuth.displayAuthorizationCode()
		res = GoogleAuth.pollForUserAuth(filename)
		if res == True:
			print("User successfully authorized device")
			return "Success"
		else:
			return "Failure"
	else:
		print("Device could not request Authorization")
		return "Failure"
