# encoding:utf-8
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
def file_reader(path_to_file, year):
    """
    Parse path to the file and then read it, making a dict.
    """
    films_info_dct = {}
    temporarylst = []
    with open (path_to_file, 'r',  encoding="utf8", errors='ignore') as file:
        for line in file:
            if year in line:
                if "{" in line:
                    line = line[:line.index("{")] + line[line.index("}"):]
                line = line.replace("#", "")
                if 
                line = line.split('\t')
def making_map(latitude, longtitude):
    map = folium.Map(tiles="Stamen Terrain",location=[latitude, longtitude])
    map.save('Map_1.html')

def film_coordinates(filmnameslst):
    """
    Parse the coordinates to the film's palces 
    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode("Старі Кути")
def distance(location1, location2):
    """
    Calculates the distance between two locs.
    """
file_reader('/Users/mskoropad/OPlabs/OPlabs2/Laboratory1/locationslist.txt', '2015')