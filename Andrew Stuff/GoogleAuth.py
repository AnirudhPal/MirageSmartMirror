# Imports
import json
import os
import subprocess
from threading import Timer
import requests

SCOPE='https://www.googleapis.com/auth/calendar.readonly'
CLIENT_ID='238441387160-vg5u4bb2td0vugjb7i39umeat5s6dtm0.apps.googleusercontent.com'
CLIENT_SECRET='6xgHHdJrMfISGFtU3KKkryid'
DEVICE_AUTH_PATH='/home/pi/Desktop/GoogleAuth/device_authorization.json'
USER_AUTH_PATH='/home/pi/Desktop/GoogleAuth/user_authorization.json'

userDidAuthorize = False
rt = None
uCode = ""
def getDeviceAuthorization():

	res = subprocess.run(["curl", "-s", "-d", "client_id=238441387160-vg5u4bb2td0vugjb7i39umeat5s6dtm0.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/calendar.readonly", "https://accounts.google.com/o/oauth2/device/code", "-o", DEVICE_AUTH_PATH])
	if res.returncode == 0:
		return True
	else:
		return False

def displayAuthorizationCode():

	fp = open(DEVICE_AUTH_PATH)
	jsonObj = json.load(fp)
	print("User Code:", jsonObj["user_code"])
	uCode = jsonObj["user_code"]

def getDeviceCode():
	fp = open(DEVICE_AUTH_PATH)
	jsonObj = json.load(fp)
	return jsonObj["device_code"]

def requestUserAuth():
	test = getDeviceCode()
    #r = requests.post("https://www.googleapis.com/oauth2/v4/token",  data={'client_id':CLIENT_ID, 'client_secret':CLIENT_SECRET, 'code':test, 'grant_type':'http://oauth.net/grant_type/device/1.0'})
    #print(r.json())
	res = subprocess.run(["curl",
				"-s",
				"-d",
				"client_id=" + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&code=" + test + "&grant_type=http://oauth.net/grant_type/device/1.0",
				"-H",
				"Content-Type: application/x-www-form-urlencoded",
				"https://www.googleapis.com/oauth2/v4/token",
				"-o",
				USER_AUTH_PATH])
                #print(res.args)
	if res.returncode == 0:
		fp = open(USER_AUTH_PATH)
		jsonObj = json.load(fp)
		for x in jsonObj:
			print(x + ": " + jsonObj[x])
			if x == "access_token":
				rt.stop()
				userDidAuthorize = True
                		print("User did authorize, access token: " + jsonObj[x])
				return

def getPollingInterval():
	fp = open(DEVICE_AUTH_PATH)
	jsonObj = json.load(fp)
	return int(jsonObj["interval"])

def getPollingExpiration():
	fp = open(DEVICE_AUTH_PATH)
	jsonObj = json.load(fp)
	return (int(jsonObj["expires_in"]))

def pollForUserAuth():
	interval = getPollingInterval()
	expiration = getPollingExpiration()
	rt = RepeatedTimer(interval+1, requestUserAuth)
	if userDidAuthorize:
		rt.stop()
		return True
	elif rt.elapsedTime > expiration:
		rt.stop()
		print("User did not authorize in time")
		return False

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.elapsedTime = 0
        self.start()

    def _run(self):
        self.elapsedTime += self.interval
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

if __name__== "__main__":
	res = getDeviceAuthorization()
	if res == True:
		print("Device Successfully requested Authorization")
		displayAuthorizationCode()
		res = pollForUserAuth()
		if res == True:
			print("User successfully authorized device")
	else:
		print("Device could not request Authorization")
