import csv
import json
import math
from geopy.geocoders import Nominatim

def build_graph(filename):
    file = open(filename, "r")
    map_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    graph = {}

    for data in map_data:
        node = data["From"]

        if node not in graph.keys():
            graph[node] = {
                "neighbors": [],
                "distances": [],
            }
            
        neighbor = data["To"]
        distance = data["Distance"]

        graph[node]["neighbors"].append(neighbor)
        graph[node]["distances"].append(distance)

    return graph

def get_coordinates(graph):
    print("Collecting coordinates. This will take a minute...")
    geolocator = Nominatim(user_agent="Turkey")
    locations = {}

    for city in graph:
        location = geolocator.geocode(city)
        locations[city] = {
            "longitude": location.longitude,
            "latitude": location.latitude
        }
    
    with open('turkey_coordinates.json', 'w') as fp:
        json.dump(locations, fp)

def city_distance_estimate(city1, city2, cities_json):
    """ Uses Haversine formula to estimate distance between two cities.

    Parameters:
        city1: Name of city.
        city2: Name of city.
        cities_json: JSON containing cities, and their longitude and latitude

    Returns:
        Distance bewteen the two cities in km.
    """
    with open(cities_json) as json_file:
        cities_dict = json.load(json_file)

    earth_radius = 6371*(10**3)

    lon1 = cities_dict[city1]["longitude"]
    lon2 = cities_dict[city2]["longitude"]
    lat1 = cities_dict[city1]["latitude"]
    lat2 = cities_dict[city2]["latitude"]

    phi1 = lat1 * math.pi/180
    phi2 = lat2 * math.pi/180
    dphi = (lat2-lat1) * math.pi/180
    dlambda = (lon2-lon1) * math.pi/180

    a = math.sin(dphi/2) * math.sin(dphi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2) * math.sin(dlambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance_estimate = earth_radius * c / 1000

    return distance_estimate