import pprint
import requests
import json
import folium
from geopy.exc import GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

mapp = folium.Map()
geolocator = Nominatim(user_agent="sotiy_try.")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def twitter_data(access_token, screen_name):
    base_url = "https://api.twitter.com/"

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    search_params = {
        'screen_name': screen_name
    }

    search_url = '{}1.1/friends/list.json'.format(base_url)
    response = requests.get(
        search_url, headers=search_headers, params=search_params)
    return response.json()


def find_locations(read_file):
    locations = list()
    for i in read_file['users']:
        if i["location"] != "":
            locations.append([i["screen_name"], i["location"]])
        if len(locations) == 100:
            break
    return locations


def find_coordinates(loactions_lst: list):
    counter = 0
    while True:
        try:
            location = geolocator.geocode(loactions_lst[counter][-1])
            loactions_lst[counter].append(
                (location.latitude, location.longitude))
            counter += 1
        except (GeocoderUnavailable, AttributeError):
            del loactions_lst[counter]
            continue
        if counter == len(loactions_lst):
            break
    return loactions_lst


def adding_points_to_map(locations_with_coordinates: list):
    for coordinates in locations_with_coordinates:
        folium.Marker(
            location=coordinates[-1], popup=coordinates[0],
            icon=folium.Icon(color='red')).add_to(mapp)


def main_function(access_token, screen_name):
    read_file = twitter_data(access_token, screen_name)
    print(read_file)
    loactions_lst = find_locations(read_file)
    locations_with_coordinates = find_coordinates(loactions_lst)
    adding_points_to_map(locations_with_coordinates)
    mapp.save("lol.html")


print(main_function("AAAAAAAAAAAAAAAAAAAAAO2SMwEAAAAAFIOTZh1di1leanfjtvYE%2FJzmwqg%3D3wqNmOgxKmTbYMeUVsA4Sgxklat8IcI7HYW886jdhhLXH1eaow", "@OlehPalka"))
