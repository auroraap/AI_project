import json
import random
import time
from graph_utils import city_distance_estimate

def gradient_descent(doctor_location, patient_list, graph):
    """ Solves the TSP with a gradient descent-like approach.
    
    Parameters:
        graph: graph containing nodes with lists of neighbors and distances.
        patient_list: list of the locations of each patient.
        doctor_location: the location of the doctor.
    
    Returns:
        A list containing all the steps that the doctor made.
    """
    solution = []
    past_steps = ["", "", ""]
    
    while patient_list != []:
        # Loop while there are unvisited patients
        neighbor_dists = []
        neighbor_list = graph[doctor_location]["neighbors"].copy()

        for neighbor in neighbor_list:
            if neighbor in patient_list:
                # Choose neighboring patient if there is one
                neighbor_list = [neighbor]
                neighbor_dists = [0]
                break
            else:
                # Calculate total distance between unvisited neighbors and all unvisited patients
                next_distance = total_distance(doctor_location=neighbor, patient_list=patient_list)
                neighbor_dists.append(next_distance)
        
        # Choos the best neighbor for next step
        indices = list(range(len(neighbor_dists)))
        neighbor_dists, indices = zip(*sorted(zip(neighbor_dists, indices)))

        best_neighbor = None
        for i, _ in enumerate(neighbor_dists):
            # Choose neighbor with minimum total distance if it has not recently been visited
            neighbor_index = indices[i]
            neighbor = neighbor_list[neighbor_index]

            if not neighbor in past_steps:
                best_neighbor = neighbor
                break

        if not best_neighbor:
            # If all neighbors have been recently visited, choose next step at random
            best_neighbor = random.choice(graph[doctor_location]["neighbors"])
            neighbor_index = graph[doctor_location]["neighbors"].index(best_neighbor)

        best_neighbor_steplength = graph[doctor_location]["distances"][neighbor_index]
        
        if best_neighbor in patient_list:
            # Remove visited patient from patient list
            patient_list.remove(best_neighbor)

        # Update recently visited cities, remove the least recent one.
        past_steps.append(doctor_location)
        past_steps.pop(0)

        # Make doctor step
        doctor_step = {"location": best_neighbor, "step length": best_neighbor_steplength}
        solution.append(doctor_step)
        doctor_location = best_neighbor

    return solution

def total_distance(doctor_location, patient_list):
    """ Computes the distance between one location and all locations in a list.
    
    Parameters:
        patient_list: list of the locations of each patient.
        doctor_location: the location of the doctor.
    
    Returns:
        The sum of the distances.
    """
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