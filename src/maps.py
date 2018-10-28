import sys
import time
import ssl
import geopy.geocoders

# import cv2
# from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
import urllib.parse, urllib.request, json, requests


class Maps:
    def __init__ (self, address, destinations):
        self.address = address
        self.destinations = destinations
        self.init_ui()


    def init_ui(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        geopy.geocoders.options.default_ssl_context = ctx
        geolocator = Nominatim(scheme="https",user_agent="MirageSmartMirror")
        maps_key = "&key=AIzaSyDKTb75-vuAvnWxO2Wfm_1DWlyr4BadgJc"
        maps_url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
        self.routes = []


        origin = geolocator.geocode(self.address)
        maps_origin = "&origins=%f,%f" %(origin.latitude, origin.longitude)

        for dest in self.destinations:
            destination_i = geolocator.geocode(dest)
            maps_destination = "&destinations=%f,%f" %(destination_i.latitude, destination_i.longitude)
            maps_request = maps_url + maps_origin + maps_destination + maps_key
            maps_get = requests.get(maps_request)
            maps_json = maps_get.json()
            route_info_time = "Time to %s: %s" %(maps_json['destination_addresses'][0], maps_json['rows'][0]['elements'][0]['duration']['text'])
            route_info_dist = "%s away" % maps_json['rows'][0]['elements'][0]['distance']['text']
            route_info = [route_info_time, route_info_dist]
            self.routes.append(route_info)
