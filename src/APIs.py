import sys
import datetime
import time
import json
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
import urllib.parse, urllib.request, json, requests

    def get_map():
        user_destinations = ["305 Swindon Way, West Lafayette, Indiana", "222 West Wood St, West Lafayette, Indiana", "West Madison Street, Chicago, Illinois"]
        address = "250 Sheetz Street, West Lafayette, Indiana"

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
            destination_i = geolocator.geocode(dest)
            maps_destination = "&destination=%f,%f" %(destination_i.latitude, destination_i.longitude)
            maps_request = maps_url + maps_origin + maps_destination + maps_key
            maps_get = requests.get(maps_request)
            maps_json = maps_get.json()
            route_info_time = "Time to %s: %s" %(maps_json['routes'][0]['legs'][0]['end_address'], maps_json['routes'][0]['legs'][0]['duration']['text'])
            route_info_dist = "%s away - Take %s" %(maps_json['routes'][0]['legs'][0]['distance']['text'], maps_json['routes'][0]['summary'])
            route_info = [route_info_time, route_info_dist]
            routes.append(route_info)
        return routes


if __name__== "__main__":
    for i in range(5):
        # print(datetime.datetime.now().time())
        # calendar_info = googleCalendar.Calendar() # fix to take in user id and get user's token
        # weather_info = weather.Weather("250 Sheetz Street, West Lafayette, Indiana")
        # date_time_info = DateTime.DateTime()
        # feed_info = feeds.Feeds()

        dict = {"id": i}
        with open('test.json', 'w') as outfile:
            json.dump(dict, outfile)
        time.sleep(30)
