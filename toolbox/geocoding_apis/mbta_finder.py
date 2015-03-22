"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
GMAPS_API_KEY = "&key=AIzaSyCBX_az1q0Qzk1-aBHhOX44LoucwwmZQxM"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """

    #Return the json of the url
    f = urllib2.urlopen(url)
    return f.read()


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """

    #Split the json into lines
    address = place_name.replace(' ', '+')
    jsonInfo = get_json(GMAPS_BASE_URL + "address=" + address + GMAPS_API_KEY)
    jsonInfo = jsonInfo.replace(' ', '')
    jsonInfo = jsonInfo.split('\n')

    #Find all lines that start with 'lat' or 'lng'
    lat_long = []
    for line in jsonInfo:
        if line[0:6] == '"lat":' or line[0:6] == '"lng":':
            lat_long.append(line)

    #Extract the actual latitude and longitude
    latitude = lat_long[0][6:-1]
    longitude = lat_long[1][6:]
    return (latitude, longitude)


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """

    #Parsing the MBTA data
    stops = get_json("http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key=wX9NwuHnZU2ToO7GmGR9uw&lat="+str(latitude)+"&lon="+str(longitude)+"&format=json")
    stops = stops.split('"stop_name":"')
    stops = stops[1]
    stops = stops.split(',')
    stop = [stops[0], stops[5]]
    stop[0] = stop[0].replace('"', '')
    stop[1] = stop[1].replace('"distance":"', '')
    stop[1] = stop[1].replace('"}', '')

    return (stop[0], float(stop[1]))

def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    """

    #Get lat and lng of the requested place
    lat_long = get_lat_long(place_name)

    #Return nearest station to the lat and lng
    return get_nearest_station(lat_long[0], lat_long[1])

print find_stop_near("Park Street Church Boston, MA")