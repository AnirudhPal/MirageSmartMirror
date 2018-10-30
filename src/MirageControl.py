from flask import Flask
import subprocess
import os
import json
import faceCalibration

app = Flask(__name__)

M_USER_DIR = "/home/pi/Desktop/MirageUsers/"

selected_user = 0
numUsers = 0

def get_num_users_plain():
	files = os.listdir("/home/pi/Desktop/MirageUsers")
	return len(files)

# Get number of users
@app.route('/user/getnum')
def get_num_users():
	global numUsers
	files = os.listdir("/home/pi/Desktop/MirageUsers")
	numUsers = len(files)
	return str(numUsers)

# Add a new user
@app.route('/user/add/<user_info>')
def add_user(user_info):
	next_user_num = get_num_users_plain()
	filename = M_USER_DIR + "user" + str(next_user_num) + ".json"
	with open(filename, 'w') as outfile:
		try:
			json.dump(user_info, outfile, ensure_ascii=False)
			return "User successfully added"
		except:
			return "Unable to add user, please try again"

# Get user by number
@app.route('/user/get/<user_number>')
def get_user(user_number):
	filename = M_USER_DIR + "user" + user_number + ".json"
	with open(filename, 'r') as json_data:
		try:
			data = json.load(json_data)
			return data
		except:
			return "Unable to access user, might not exist"

# Update user by number
@app.route('/user/update/<user_number>/<user_info>')
def update_user(user_number, user_info):
	filename = M_USER_DIR + "user" + user_number + ".json"
	with open(filename, 'w') as outfile:
		try:
			json.dump(user_info, outfile, ensure_ascii=False)
			return "User successfully updated"
		except:
			return "User could not be updated"

# Delete user by number
@app.route('/user/delete/<user_number>')
def delete_user(user_number):
	file_to_delete = M_USER_DIR + "user" + user_number + ".json"
	if (os.path.exists(file_to_delete)):
		os.remove(file_to_delete)
		print("User removed")
	else:
		return "User not found"

	new_num_users = get_num_users_plain()
	files = os.listdir("/home/pi/Desktop/MirageUsers")
	for i in range(new_num_users):
		os.rename(M_USER_DIR + files[i], M_USER_DIR + files[i]+".temp")

	for j in range(new_num_users):
		os.rename(M_USER_DIR + files[j] + ".temp", M_USER_DIR + "user" + str(j) + ".json")


	return "User deleted and files updated"

# Setup user for face calibration
@app.route('/setup/newuser/<filename>')
def start_face_calibration(filename):
	faceCalibration.faceCalibration(filename)

# Cancel face calibration
@app.route('/setup/cancel')
def cancel_face_calibration():
	faceCalibration.cancelCalibration()
