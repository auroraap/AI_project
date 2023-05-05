import json
import random
import time
from graph_utils import city_distance_estimate

def gradient_descent(doctor_location, patient_list, graph):
    start_timespamp = time.time_ns()
    print("[DEBUG] Staring gradient descent.")
    solution = []
    visited_nodes = []
    
    while patient_list != []:
        neighbor_dists = []
        neighbor_list = graph[doctor_location]["neighbors"].copy()

        for neighbor in neighbor_list:
            if neighbor in patient_list:
                neighbor_list = [neighbor]
                neighbor_dists = [0]
                break

            elif neighbor in visited_nodes:
                neighbor_list.remove(neighbor)
            else:
                # calculate total distance between unvisited neighbors and all unvisited patients
                next_distance = total_distance(doctor_location=neighbor, patient_list=patient_list)
                neighbor_dists.append(next_distance)
        
        if neighbor_dists == []:
            print("[DEBUG] No allowed neighbors. Choosing at random.")
            best_neighbor = random.choice(graph[doctor_location]["neighbors"])
            neighbor_index = graph[doctor_location]["neighbors"].index(best_neighbor)
        else:
            min_distance = min(neighbor_dists)
            neighbor_index = neighbor_dists.index(min_distance)
            best_neighbor = neighbor_list[neighbor_index]
        best_neighbor_steplength = graph[doctor_location]["distances"][neighbor_index]
        
        if best_neighbor in patient_list:
            patient_list.remove(best_neighbor)
            visited_nodes = []
        else:
            visited_nodes.append(doctor_location)

        doctor_step = {"location": best_neighbor, "step length": best_neighbor_steplength}
        solution.append(doctor_step)
        doctor_location = best_neighbor

        ts = time.time_ns()
        if ts - start_timespamp > 2500000:
            return None

    return solution

def total_distance(doctor_location, patient_list):
    with open('turkey_coordinates.json', 'r') as f:
        coordinates = json.load(f)
    
    doctor_lon = coordinates[doctor_location]["longitude"]
    doctor_lat = coordinates[doctor_location]["latitude"]

    sum = 0

    for patient_location in patient_list:
        patient_lon = coordinates[patient_location]["longitude"]
        patient_lat = coordinates[patient_location]["latitude"]

        distance = city_distance_estimate(lon1=doctor_lon, lat1=doctor_lat, lon2=patient_lon, lat2=patient_lat)
        sum += distance
    
    return sum