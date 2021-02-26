"""
This is module with my first flask project
"""
import requests
import folium
from geopy.exc import GeocoderUnavailable
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request


mapp = folium.Map()
geolocator = Nominatim(user_agent="sotiy_try.")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
app = Flask(__name__)


def twitter_data(access_token, screen_name):
    """
    This function gets information about user from Twitter.
    """
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
    """
    This function finds location of each person, you follow.
    """
    locations = list()
    for i in read_file['users']:
        if i["location"] != "":
            locations.append([i["screen_name"], i["location"]])
        if len(locations) == 100:
            break
    return locations


def find_coordinates(loactions_lst: list):
    """
    This function finds coordinates according to the
    location of people you folow.
    """
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
    """
    This function adds points of your friends location to the map.
    """
    for coordinates in locations_with_coordinates:
        folium.Marker(
            location=coordinates[-1], popup=coordinates[0],
            icon=folium.Icon(color='red')).add_to(mapp)


def main_function(access_token, screen_name):
    """
    This id the main function, which returns ready map.
    """
    read_file = twitter_data(access_token, screen_name)
    loactions_lst = find_locations(read_file)
    locations_with_coordinates = find_coordinates(loactions_lst)
    adding_points_to_map(locations_with_coordinates)
    return mapp


@app.route("/")
def index():
    """
    This function generates site.
    """
    return render_template("index.html")


@app.route("/followers", methods=["POST"])
def adding_map():
    """
    This function add map to the site.
    """
    user_name = str(request.form.get("user_name"))
    api_key = str(request.form.get("API_key"))
    map_html = main_function(api_key, user_name)
    return map_html.get_root().render()


if __name__ == "__main__":
    app.run(debug=True)
