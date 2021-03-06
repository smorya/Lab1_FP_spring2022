"""Module that analyzes the database of films"""
# encoding:utf-8
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from haversine import haversine
import argparse
def file_reader(year, path_to_file):
    """
    Parse path to the file and then read it, making a dict.
    """
    ukrlang = "абвгґдеєжзиіїйклмнопрстуфхцчшщбюя"
    films_info_dct = {}
    film_linelst = []
    with open (path_to_file, 'r',  encoding="utf-8", errors='ignore') as file:
        for line in file:
            if year in line:
                if "{" in line:
                    line = line[:line.index("{")] + line[line.index("}") + 1:]
                if "(" in line:
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
    return films_info_dct

def film_coordinates(films_info_dct):
    """
    Parse the coordinates to the film's places and make tuple of it.
    >>> film_coordinates({'"15SecondScare"  ': ['Coventry, West Midlands, England, UK']})
    {'"15SecondScare"  ': [(52.4081812, -1.510477)]}
    """
    films_locs_dct = {}
    geolocator = Nominatim(user_agent="main.py")
    for tple in films_info_dct.items():
        for loc in tple[1]:
            location = geolocator.geocode(loc, timeout = None)
            if location is None:
                def splitter(loc):
                    try:
                        loc = loc[loc.index(",") + 1:]
                        location = geolocator.geocode(loc, timeout = None)
                        if location is None:
                            splitter(loc)
                        else:
                            return location
                    except Exception:
                        return None
                location = splitter(loc)
            if location is not None:
                if tple[0] in films_locs_dct.keys():
                    films_locs_dct[tple[0]].append((location.latitude, location.longitude))
                else:
                    films_locs_dct[tple[0]] = [(location.latitude, location.longitude)]
    return films_locs_dct

def distance(latitude1, longitude2, films_locs_dct):
    """
    Calculates the distance between two locs.
    >>> distance(49.83826, 24.02324, {'"15SecondScare"  ': [(52.4081812, -1.510477)]})
    [('"15SecondScare"  ', 1795.09010826153, (52.4081812, -1.510477))]
    """
    usersloc = (float(latitude1), float(longitude2))
    lstofdistance = []
    for item in films_locs_dct.items():
        for locati in item[1]:
            distance = haversine(usersloc, locati)
            lstofdistance.append((item[0], distance, locati))
    lstofdistance = sorted(lstofdistance, key = lambda x: x[1])
    lstofdistance = lstofdistance[:10]
    return lstofdistance

def making_map(latitude1, longitude2,lstofdistance):
    """
    Makes a map out od data, stated in previous functions.
    """
    map = folium.Map(zoom_start=4, tiles="Stamen Terrain",location = [latitude1, longitude2], control_scale=True)
    film_markers = folium.FeatureGroup(name = "Films")
    users_location = folium.FeatureGroup(name = "your location")
    map.add_child(users_location)
    map.add_child(film_markers)
    users_location.add_child(folium.Marker(location = (latitude1, longitude2), popup="your location"))
    for element in lstofdistance:
        film_markers.add_child(folium.Marker(location = element[2], popup = element[0]))
    map.add_child(folium.LayerControl())
    map.save('Map_films.html')

def main():
    """
    Brings up all functions together to make the module work.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('year', help = 'year of a film', type = str)
    parser.add_argument('latitude', help = 'latitude of users loc')
    parser.add_argument('longitude', help = 'longitude of users loc')
    parser.add_argument('path_to_dataset', help = 'path to dataset', type = str)
    args = parser.parse_args()
    latitude1 = args.latitude
    longitude1 = args.longitude
    path_to_file = args.path_to_dataset
    year = args.year
    films_info_dct = file_reader(args.year, args.path_to_dataset)
    films_locs_dct = film_coordinates(films_info_dct)
    making_map(latitude1, longitude1, distance(latitude1, longitude1, films_locs_dct))

if __name__ == "__main__":
    main()
