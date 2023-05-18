from graph_utils import city_distance_estimate
import json
import random

def nearest_neighbor_search(doctor_location, patient_list, graph):
    with open('turkey_coordinates.json', 'r') as f:
        coordinates = json.load(f)

    solution = []
    doctor_step = {"location": doctor_location, "step length": 0}
    solution.append(doctor_step)
    past_steps = ["", "", "", ""]
    if doctor_location in patient_list:
        patient_list.remove(doctor_location)
        
    while patient_list != []:
        neighborFound = False
        reoccurrence = False
        for location in past_steps:
            if (past_steps.count(location) >= 2) and (location != ""):
                reoccurrence = True

        for neighbor_index, neighbor in enumerate(graph[doctor_location]["neighbors"]):
            # if a neighboring city is a patient, go there
            if neighbor in patient_list:
                best_neighbor = neighbor
                best_neighbor_dist = graph[doctor_location]["distances"][neighbor_index]
                neighborFound = True
                break
        if not neighborFound:
            allowed_neigbors = graph[doctor_location]["neighbors"].copy()
            if reoccurrence and ( len(allowed_neigbors) > 1 ):
                allowed_neigbors.remove(past_steps[-1])
            goal_patient = get_nearest_patient(coordinates=coordinates, doctor_location=doctor_location, patient_list=patient_list)
            best_neighbor = get_nearest_patient(coordinates=coordinates, doctor_location=goal_patient, patient_list=allowed_neigbors)
            neighbor_index = graph[doctor_location]["neighbors"].index(best_neighbor)
            best_neighbor_dist = graph[doctor_location]["distances"][neighbor_index]
        
        if best_neighbor in patient_list:
            patient_list.remove(best_neighbor)

        # store step in solution
        doctor_step = {"location": best_neighbor, "step length": best_neighbor_dist}
        solution.append(doctor_step)
        past_steps.append(doctor_location)
        past_steps.pop(0)
        doctor_location = best_neighbor
        
    return solution

def get_nearest_patient(coordinates, doctor_location, patient_list):
    doctor_lon = coordinates[doctor_location]["longitude"]
    doctor_lat = coordinates[doctor_location]["latitude"]

    shortest_dist = float('inf')

    for patient in patient_list:
        patient_lon = coordinates[patient]["longitude"]
        patient_lat = coordinates[patient]["latitude"]

        patient_dist = city_distance_estimate(doctor_lon, doctor_lat, patient_lon, patient_lat)
        if patient_dist < shortest_dist:
            shortest_dist = patient_dist
            nearest_patient = patient
    
    return nearest_patient

