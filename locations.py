# encoding:utf-8
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
def file_reader(path_to_file, year):
    """
    Parse path to the file and then read it, making a dict.
    """
    ukrlang = "абвгґдеєжзиіїйклмнопрстуфхцчшщбюя"
    films_info_dct = {}
    film_linelst = []
    with open (path_to_file, 'r',  encoding="utf8", errors='ignore') as file:
        for line in file:
            if year in line:
                if "{" or "(" in line:
                    line = line[:line.index("{")] + line[line.index("}") + 1:]
                    while "(" in line:
                        line = line[:line.index("(")] + line[line.index(")") + 1:]
                line = line.replace("#", "")
                line = line.replace("\n", "")
                if line[0] in ukrlang:
                    line = line[1:]
                linelst = line.split('\t')
                for element in linelst:
                    if element == '' or element == "" :
                        linelst.remove(element)
                if linelst[0] in films_info_dct.keys():
                    films_info_dct[linelst[0]].append(linelst[-1])
                else:
                    films_info_dct[linelst[0]] = [linelst[-1]]


def making_map(latitude, longtitude):
    map = folium.Map(tiles="Stamen Terrain",location=[latitude, longtitude])
    map.save('Map_1.html')

def film_coordinates(film_linelst):
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
