import csv
import json
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
