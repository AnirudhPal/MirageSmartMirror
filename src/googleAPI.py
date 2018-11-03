import sys
import requests
import json
import time
#import urllib.request as urllib
#from urllib import urlencode
import urllib.request
import os

#CLIENT_ID = "238441387160-vg5u4bb2td0vugjb7i39umeat5s6dtm0.apps.googleusercontent.com"
#CLIENT_SEC = "6xgHHdJrMfISGFtU3KKkryid"
CLIENT_ID = "130335195609-r8e5aguvg3sr2a1d0e2oap6bjrn3aoml.apps.googleusercontent.com"
CLIENT_SEC = "kK5MrgIPk5GLluvDZS4E7HYM"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"


auth_code = ""
access_token = ""
refresh_token = ""

def get_calendar_list():
	global access_token

	authorization_header = {"Authorization" : "Bearer %s" % access_token}
	result = requests.get("https://www.googleapis.com/calendar/v3/users/me/calendarList", headers=authorization_header)
	#print(result.text)
	return result.text

def refresh_access_token(user_path):
	global access_token

	print("Refreshing Access Token")

	with open(user_path, 'r') as outfile:
		try:
			data = json.load(outfile)
		except:
			print("Could not load user's auth file")
			return

	print("Old access token: %s" % data['access_token'])

	access_token_req = {
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SEC,
		"refresh_token": data['refresh_token'],
		"grant_type":"refresh_token"
	}
#	content_len = len(urlencode(access_token_req))
	result = requests.post("https://www.googleapis.com/oauth2/v4/token", data=access_token_req)
	print(result.text)
	new_data = json.loads(result.text)
	if 'access_token' in new_data:
		data['access_token'] = new_data['access_token']
		data['expires_in'] = new_data['expires_in']
		access_token = data['access_token']

		print("New access token: %s" % access_token)

		with open(user_path, 'w') as jsonFile:
			json.dump(data, jsonFile)
	else:
		print("Unable to refresh token: error: %s, description: %s" %(new_data['error'], new_data['error_description']))
		return


def get_start_end_time(event):
	try:
		if event['start'].has_key('date'):
			start = event['start']['date']
		elif event['start'].has_key('dateTime'):
			start = event['start']['dateTime']
		else:
			start = 'N/A'

		if event['end'].has_key('date'):
			end = event['end']['date']
		elif event['end'].has_key('dateTime'):
			end = event['end']['dateTime']
		else:
			end = 'N/A'
		return start, end

	except:
		return event['etag'], event['status']


def get_events_list(user_path):
	global access_token

	with open(user_path, 'r') as outfile:
		try:
			auth_data = json.load(outfile)
		except:
			return "Unable to read user authentication file"

	curr_time = time.time()
	if (curr_time - os.path.getmtime(user_path) >= auth_data['expires_in']):
		refresh_access_token(user_path)
	else:
		access_token = auth_data['access_token']

	data = json.loads(get_calendar_list())
	if "error" in data:
		print("Error loading calendars")
		return
	for calendar in data['items']:
		if (calendar['accessRole'] == "reader"):
			break

		calendar_id = calendar['id']

		authorization_header = {"Authorization" : "Bearer %s" % access_token}
		url = ("https://www.googleapis.com/calendar/v3/calendars/%s/events" %(urllib.parse.quote_plus(calendar_id)))
		result = requests.get(url, headers=authorization_header)

		events = json.loads(result.text)
		for event in events['items']:
			print(event.get('summary', '(Event title not set)'))
			if event['status'] != 'cancelled':
				start, end = get_start_end_time(event)
				print("   start : ", start, "  end : ", end)


def main():
#	get_events_list("~/MirageSmartMirror/src/Users/user0/user0_auth.json")
	get_events_list(sys.argv[1])

if __name__=='__main__':
	main()
