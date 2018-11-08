import sys
import datetime
import time
import json
import ssl
import os
import geopy.geocoders
from geopy.geocoders import Nominatim
import urllib.parse, urllib.request, json, requests
from newsapi import NewsApiClient

def get_map(address, user_destinations):
    # user_destinations = ["305 Swindon Way, West Lafayette, Indiana", "222 West Wood St, West Lafayette, Indiana", "West Madison Street, Chicago, Illinois"]
    # address = "250 Sheetz Street, West Lafayette, Indiana"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim(scheme="https",user_agent="MirageSmartMirror")
    maps_key = "&key=AIzaSyDKTb75-vuAvnWxO2Wfm_1DWlyr4BadgJc"
    maps_url = "https://maps.googleapis.com/maps/api/directions/json?"
    routes = []


    origin = geolocator.geocode(address)
    maps_origin = "origin=%f,%f" %(origin.latitude, origin.longitude)

    for dest in user_destinations:
        destination_i = geolocator.geocode(dest['address'])
        maps_destination = "&destination=%f,%f" %(destination_i.latitude, destination_i.longitude)
        maps_request = maps_url + maps_origin + maps_destination + maps_key
        maps_get = requests.get(maps_request)
        maps_json = maps_get.json()
        route_info_time = "Time to %s: %s" %(maps_json['routes'][0]['legs'][0]['end_address'], maps_json['routes'][0]['legs'][0]['duration']['text'])
        route_info_dist = "%s away - Take %s" %(maps_json['routes'][0]['legs'][0]['distance']['text'], maps_json['routes'][0]['summary'])
        route_info = [route_info_time, route_info_dist]
        routes.append(route_info)
    return routes

def get_weather(address):
    geolocator = Nominatim(user_agent="MirageSmartMirror")
    origin = geolocator.geocode(address)

    weather_key = "50f9b96898249aa1a036886103f78788"
    weather_url = "https://api.darksky.net/forecast/" + weather_key
    # 0123456789abcdef9876543210fedcba/42.3601,-71.0589
    weather_request = weather_url + "/%f,%f" %(origin.latitude, origin.longitude)
    weather_get = requests.get(weather_request)
    weather_json = weather_get.json()

    daily_summary = weather_json['daily']['data'][0]['summary']
    current_summary = weather_json['currently']['summary']
    current_temp = weather_json['currently']['temperature']
    weather_dict = {"daily": daily_summary, "current": current_summary, "temp": current_temp}
    return weather_dict


def get_news(preferences):
    newsapi = NewsApiClient(api_key='33ff7834a7ee40928e7bb90746c8b6e5')
    # top_headlines = newsapi.get_top_headlines(category=user_dict["newsCategories"][0]
    #                                         language='en',
    #                                           country='us')
    news_sources = newsapi.get_sources()
    news_url = ('https://newsapi.org/v2/top-headlines?'
           'category=%s&'
           'country=us&'
           'apiKey=33ff7834a7ee40928e7bb90746c8b6e5' %(preferences[0]))
    # print(news_url)
    news_response = requests.get(news_url)
    news_data = news_response.json()
    return news_data




if __name__== "__main__":
    while(True):
        num_of_users = len(os.listdir("Users")) - 1
        # print(num_of_users)
        stime = time.asctime( time.localtime(time.time()) )
        print("Start time: ", stime)

        for i in range(num_of_users):
            file_path = 'Users/user%d/user%d.json' %(i, i)
            with open(file_path) as f:
                data = json.load(f)

            user_dict = json.loads(data)
            # print(user_dict['freqDests'])

            dict = {"map": get_map(user_dict["address"], user_dict['freqDests']), "weather": get_weather(user_dict["address"]), "news": get_news(user_dict["newsCategories"])}
            file_path = 'Users/user%d/user%dAPI.json' %(i, i)
            with open(file_path, 'w') as outfile:
                json.dump(dict, outfile)
                print("JSON Dumped!")
        etime = time.asctime( time.localtime(time.time()) )
        print("End time: ", etime)
        time.sleep(60)
