import csv
import json
import math
import matplotlib.pyplot as plt
import networkx as nx
import random
from geopy.geocoders import Nominatim

def build_graph(filename):
    """Build a graph with weighted edges.

    Parameters:
        filename: name of the csv file with the dataset.
    
    Returns:
        Graph in dictionary format. The key is city name, and the values are naighboring cities and distances.
    """
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

def evaluate(solution, n_doctors):
    """ Evaluates TSP solution.

    Parameters:
        solution: list of steps made by the doctors.
        n_doctors: number of doctors in problem.
    
    Returns:
        total distance travelled and gini index indicating distribution of steps between the doctors.
    """
    total_distance = 0
    doctor_distance = [0] * n_doctors
    for doctor_index, doctor_solution in enumerate(solution):
        for step in doctor_solution:
            total_distance += int(step['step length'])
            doctor_distance[doctor_index] += int(step['step length'])
    
    gini = 1
    for distance in doctor_distance:
        gini -= (distance / total_distance) ** 2
    
    return [total_distance, gini]

def get_coordinates(graph):
    """Find longitude and latitude of each city in the graph.
    
    Parameters:
        graph: Dictionary with cities as keys.
    """
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

def city_distance_estimate(lon1, lat1, lon2, lat2):
    """ Uses Haversine formula to estimate distance between two cities.

    Parameters:
        lon1
        lat1
        lon2
        lat2

    Returns:
        Distance bewteen the two cities in km.
    """
    earth_radius = 6371*(10**3)

    phi1 = lat1 * math.pi/180
    phi2 = lat2 * math.pi/180
    dphi = (lat2-lat1) * math.pi/180
    dlambda = (lon2-lon1) * math.pi/180

    a = math.sin(dphi/2) * math.sin(dphi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2) * math.sin(dlambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance_estimate = earth_radius * c / 1000

    return distance_estimate

def kmeans(json_filename, patient_locations, k):
    """ Clusters patient locations.

    Parameters:
        json_filename: json file containing the coordinates of each city.
        patient_locations: list of locations for each patient.
        k: number of clusters to be made
    
    Returns:
        List of k patient location lists.
    """
    # Read json
    with open(json_filename, 'r') as f:
        coordinates = json.load(f)

    # Initialize k centroids
    centroids = random.sample(list(coordinates), k)
    centroid_long, centroid_lat = [], []
    for centroid in centroids:
        centroid_long.append( coordinates[centroid]['longitude'] )
        centroid_lat.append( coordinates[centroid]['latitude'] )
    
    stop = False
    n_iter = 0
    
    while not stop:
        clusters = [[] for i in range(k) ]
        clusters_long = [[] for i in range(k) ]
        clusters_lat = [[] for i in range(k) ]
        new_centroid_long, new_centroid_lat = [0]*k, [0]*k

        # Loop over cities
        for location in patient_locations:
            # Loop over centroids
            patient_long = coordinates[location]['longitude']
            patient_lat = coordinates[location]['latitude']
            dists = []
            for i in range(k):
                dist = city_distance_estimate( patient_long, patient_lat, centroid_long[i], centroid_lat[i] )
                dists.append( dist )
            # Assign city to nearest centroid
            min_distance = min(dists)
            assigned_cluster = dists.index(min_distance)
            clusters[assigned_cluster].append(location)
            # Store coordinates of the patient location to ease centroid calculation
            clusters_long[assigned_cluster].append(patient_long)
            clusters_lat[assigned_cluster].append(patient_lat)
         # Calculate new centroids
        for i in range(k):
            new_centroid_long[i] = sum(clusters_long[i]) / len(clusters_long[i])
            new_centroid_lat[i] = sum(clusters_lat[i]) / len(clusters_lat[i])
        
        # Check stopping criteria
        if (( new_centroid_long == centroid_long ) and ( new_centroid_lat == centroid_lat )) or ( n_iter == 20 ):
            stop = True
        # Update centroids
        else:
            centroid_long = new_centroid_long
            centroid_lat = new_centroid_lat

        n_iter += 1
       

    return clusters
        
def visualize(turkey_map, clusters, doctors, solutions = []):
    """ Builds a networkx graph and visualizes it.

    Parameters:
        turkey_map: graph in dictionary structure.
        clusters: 2d list containing the clustered patient list.
        doctors: the location of the doctors.
    """
    G = nx.Graph()
    G.add_nodes_from(turkey_map.keys())
    pos = nx.spring_layout(G)
    colors = ['#cc99ff', '#0099ff', '#ffcc00', '#ff0000', '#d9d9d9']
    edge_colors = []

    color_map = []
    for node in G:
        color_assigned = colors[-1]
        for idx, cluster in enumerate(clusters):
            if node in cluster:
                color_assigned = colors[idx]
            if node in doctors:
                color_assigned = colors[-2]
        color_map.append(color_assigned)

    for location in turkey_map:
        for index, neighbor in enumerate(turkey_map[location]['neighbors']):
            # if not G.has_edge(location, neighbor):
            edge_color = '#C0C0C0'
            for s, solution in enumerate(solutions):
                for step in range(len(solution)-1):
                    #print("{a}, {b}, {c}, {d}".format(a=location, b=neighbor, c=solution[step]["location"], d=solution[step+1]["location"]))
                    if ((solution[step]["location"] == location) or (solution[step]["location"] == neighbor)) and  ((solution[step+1]["location"] == location) or (solution[step+1]["location"] == neighbor)):
                        edge_color = colors[s]
            G.add_edge(location, neighbor, weight=turkey_map[location]['distances'][index])
            edge_colors.append(edge_color)
    
    nx.draw(G, node_color=color_map, with_labels=True, node_size=50, node_shape="s", alpha=0.6, linewidths=10, font_size=6, edge_color=edge_colors)
    plt.show()
    

def clean_solution(solution, patient_list):
    n_steps = len(solution)
    new_sol = []
    new_sol.append(solution[0])
    new_sol.append(solution[1])
    for step_num, step in enumerate(solution):
        if (step_num < n_steps - 2):
            new_sol.append(solution[step_num+2])
        if (step_num < n_steps - 2) and (solution[step_num]['location'] == solution[step_num+2]['location']) and (solution[step_num+1]['location'] not in patient_list):
            # Remove steps that are repeated IF the middle step does not contain a patient
            new_sol.pop(-2)
            new_sol.pop(-1)

        if solution[step_num]['location'] in patient_list:
            # Keep track of visited patients
            while solution[step_num]['location'] in patient_list:
                patient_list.remove(solution[step_num]['location'])
        if patient_list == []:
            break
    return new_sol