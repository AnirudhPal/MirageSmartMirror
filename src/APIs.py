#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import datetime
import time
import json
import ssl
import os
import geopy.geocoders
from geopy.geocoders import Nominatim
import urllib.parse
import urllib.request
import json
import requests
from newsapi import NewsApiClient
import subprocess

# Amjad

CLIENT_ID = \
    '238441387160-vg5u4bb2td0vugjb7i39umeat5s6dtm0.apps.googleusercontent.com'
CLIENT_SEC = '6xgHHdJrMfISGFtU3KKkryid'

# Andrew
# CLIENT_ID = "130335195609-r8e5aguvg3sr2a1d0e2oap6bjrn3aoml.apps.googleusercontent.com"
# CLIENT_SEC = "kK5MrgIPk5GLluvDZS4E7HYM"

REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

auth_code = ''
access_token = ''
refresh_token = ''


def get_wifi_status() :
        # Check WiFi connectivity
        f = os.popen('iwgetid')
        now = f.read()
        if not now == '':
            #print("INTERNET IN API")
            return 1
        else:
            #print("NO INTERNET IN API")
            return 0

def get_map(address, user_destinations):
    if get_wifi_status() is 0:
        return None
    # user_destinations = ["305 Swindon Way, West Lafayette, Indiana", "222 West Wood St, West Lafayette, Indiana", "West Madison Street, Chicago, Illinois"]
    # address = "250 Sheetz Street, West Lafayette, Indiana"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(scheme='https',
                           user_agent='MirageSmartMirror')
    maps_key = '&key=AIzaSyDKTb75-vuAvnWxO2Wfm_1DWlyr4BadgJc'
    maps_url = 'https://maps.googleapis.com/maps/api/directions/json?'
    routes = []
    print(address)
    origin = geolocator.geocode(address, timeout=3)
    maps_origin = 'origin=%f,%f' % (origin.latitude, origin.longitude)

    for dest in user_destinations:
        # destination_i = geolocator.geocode(dest['address'], timeout=3)
        # maps_destination = '&destination=%f,%f' \
            # % (destination_i.latitude, destination_i.longitude)
        maps_destination = '&destination=%f,%f' %(dest['latitude'], dest['longitude'])
        maps_request = maps_url + maps_origin + maps_destination \
            + maps_key
        maps_get = requests.get(maps_request)
        maps_json = maps_get.json()
        route_info_time = 'Time to %s: %s' % (maps_json['routes'
                ][0]['legs'][0]['end_address'], maps_json['routes'
                ][0]['legs'][0]['duration']['text'])
        route_info_dist = '%s away - Take %s' % (maps_json['routes'
                ][0]['legs'][0]['distance']['text'], maps_json['routes'
                ][0]['summary'])
        route_info = [route_info_time, route_info_dist]
        routes.append(route_info)
    return routes


def get_weather(address):
    if get_wifi_status() is 0:
        return
    geolocator = Nominatim(user_agent='MirageSmartMirror')
    origin = geolocator.geocode(address, timeout=3)

    weather_key = '50f9b96898249aa1a036886103f78788'
    weather_url = 'https://api.darksky.net/forecast/' + weather_key

    # 0123456789abcdef9876543210fedcba/42.3601,-71.0589

    weather_request = weather_url + '/%f,%f' % (origin.latitude,
            origin.longitude)
    weather_get = requests.get(weather_request)
    weather_json = weather_get.json()

    daily_summary = weather_json['daily']['data'][0]['summary']
    current_summary = weather_json['currently']['summary']
    current_temp = weather_json['currently']['temperature']
    current_icon = weather_json['currently']['icon']
    weather_dict = {'daily': daily_summary, 'current': current_summary,
                    'temp': current_temp, 'icon': current_icon}
    return weather_dict


def get_news(preferences):
    newsapi = NewsApiClient(api_key='33ff7834a7ee40928e7bb90746c8b6e5')

    # top_headlines = newsapi.get_top_headlines(category=user_dict["newsCategories"][0]
    #                                         language='en',
    #                                           country='us')

    news_sources = newsapi.get_sources()
    if len(preferences) == 0:
        news_url = 'https://newsapi.org/v2/top-headlines?&country=us&apiKey=33ff7834a7ee40928e7bb90746c8b6e5'
    else:
        news_url = \
        'https://newsapi.org/v2/top-headlines?category=%s&country=us&apiKey=33ff7834a7ee40928e7bb90746c8b6e5' \
        % preferences[0]

    # print(news_url)

    news_response = requests.get(news_url)
    news_data = news_response.json()
    return news_data


def get_calendar_list():
    global access_token

    authorization_header = {'Authorization': 'Bearer %s' % access_token}
    result = \
        requests.get('https://www.googleapis.com/calendar/v3/users/me/calendarList'
                     , headers=authorization_header)

    # print(result.text)

    return result.text


def refresh_access_token(user_path):
    global access_token

    print('Refreshing Access Token')

    with open(user_path, 'r') as outfile:
        try:
            data = json.load(outfile)
        except:
            print("Could not load user's auth file")
            return

    print('Old access token: %s' % data['access_token'])

    access_token_req = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SEC,
        'refresh_token': data['refresh_token'],
        'grant_type': 'refresh_token',
        }

# ....content_len = len(urlencode(access_token_req))

    result = requests.post('https://www.googleapis.com/oauth2/v4/token'
                           , data=access_token_req)
    print(result.text)
    new_data = json.loads(result.text)
    if 'access_token' in new_data:
        data['access_token'] = new_data['access_token']
        data['expires_in'] = new_data['expires_in']
        access_token = data['access_token']

        print('New access token: %s' % access_token)

        with open(user_path, 'w') as jsonFile:
            json.dump(data, jsonFile)
    else:
        print('Unable to refresh token: error: %s, description: %s'
            % (new_data['error'], new_data['error_description']))
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
        return (start, end)
    except:

        return (event['etag'], event['status'])

def fix_event_time(str):
    sub1 = str[0:10]
    sub2 = str[11:16]
    return sub1 + ' ' + sub2


def get_events_list(user_path):
    if user_path == "Empty":
        return None
    global access_token

    with open(user_path, 'r') as outfile:
        try:
            auth_data = json.load(outfile)
        except:
            return 'Unable to read user authentication file'

    curr_time = time.time()
    if curr_time - os.path.getmtime(user_path) >= auth_data['expires_in'
            ]:
        refresh_access_token(user_path)
    else:
        access_token = auth_data['access_token']

    data = json.loads(get_calendar_list())
    if 'error' in data:
        print('Error loading calendars')
        return
    for calendar in data['items']:
        if calendar['accessRole'] == 'reader':
            break

        calendar_id = calendar['id']

        authorization_header = {'Authorization': 'Bearer %s' \
                                % access_token}
        url = \
            'https://www.googleapis.com/calendar/v3/calendars/%s/events' \
            % urllib.parse.quote_plus(calendar_id)
        result = requests.get(url, headers=authorization_header)

        events = json.loads(result.text)
        events_list = []
        for event in events['items']:

            # print(event)

            summary = event.get('summary', '(Event title not set)')
            if event['status'] != 'cancelled':
                key1 = list(event['start'].keys())[0]
                start = fix_event_time(event['start'][key1])
                end = fix_event_time(event['end'][key1])
                dict = {'summary':summary, 'start':start, 'end':end}
                events_list.append(dict)
                # print(dict)
    return events_list

# Call this after writing the user0.json file... Example: pullApi("user0")
# Might need to put semaphores here...
# TODO: Check if google calendar information is available
def pullApi(userName):
    if get_wifi_status() is 0:
        return
    file_path = '/home/pi/MirageSmartMirror/src/Users/%s/%s.json' % (userName, userName)
    with open(file_path) as f:
        data = json.load(f)

    user_dict = json.loads(data)
    #print(user_dict['address'])
    #print(user_dict["address"])
    # print(user_dict['freqDests'])
    calendar_path = "Empty"
    if user_dict['googleConnected'] == "True":
        calendar_path = '/home/pi/MirageSmartMirror/src/Users/%s/%s_auth.json' % (userName, userName)

    dict = {'name': user_dict['name'],
            'map': get_map(user_dict['address'],
            user_dict['freqDests']),
            'weather': get_weather(user_dict['address']),
            'news': get_news(user_dict['newsCategories']),
            'events': get_events_list(calendar_path)}
    file_path = '/home/pi/MirageSmartMirror/src/Users/%s/%sAPI.json' % (userName, userName)
    with open(file_path, 'w') as outfile:
        json.dump(dict, outfile)
        print('JSON Dumped!')

if __name__ == '__main__':
    #subprocess.call("python3 /home/pi/MirageSmartMirror/src/window.py &", shell=True)
    while True:
        if get_wifi_status() is 0:
            continue
        num_of_users = len(os.listdir('/home/pi/MirageSmartMirror/src/Users'))

        # print(num_of_users)

        stime = time.asctime(time.localtime(time.time()))
        print('Start time: ', stime)

        for i in range(num_of_users):
            j = num_of_users - i - 1
            name = "user%d" %j
            pullApi(name)
            # file_path = '/home/pi/MirageSmartMirror/src/Users/user%d/user%d.json' % (j, j)
            # calendar_path = '/home/pi/MirageSmartMirror/src/Users/user%d/user%d_auth.json' % (j, j)
            # with open(file_path) as f:
            #     data = json.load(f)
            # #    print(data[103])
            # #print(user_dict)
            # user_dict = json.loads(data)
            #
            # # print(user_dict['freqDests'])
            # #print(user_dict["address"])
            # #print(user_dict['address'])
            # dict = {'map': get_map(user_dict['address'],
            #         user_dict['freqDests']),
            #         'weather': get_weather(user_dict['address']),
            #         'news': get_news(user_dict['newsCategories']),
            #         'events': get_events_list(calendar_path)}
            # file_path = '/home/pi/MirageSmartMirror/src/Users/user%d/user%dAPI.json' % (j, j)
            # with open(file_path, 'w') as outfile:
            #     json.dump(dict, outfile)
            #     print('JSON Dumped!')
        etime = time.asctime(time.localtime(time.time()))
        print('End time: ', etime)
        time.sleep(60)
