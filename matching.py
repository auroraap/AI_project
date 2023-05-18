import json
from graph_utils import city_distance_estimate

def cluster_preferences(doctor_locations, patient_clusters):
    """ Generates preferences of the doctors towards the patient clusters.
    
    Parameters:
        doctor locations: the location of each doctor.
        patient_clusters: list of the locations of each patient in every patient cluster.
    
    Returns:
        A list of preferences for every doctor.
    """
    with open('turkey_coordinates.json', 'r') as f:
        coordinates = json.load(f)

    num_doctors = len(doctor_locations)

    nearest_patient_dist = [[] for i in range(num_doctors) ]
    preferences = [[] for i in range(num_doctors) ]
    for doc_idx, doctor in enumerate(doctor_locations):
        # calculate distance from each doctor to the nearest patient in each cluster
        doctor_long = coordinates[doctor]['longitude']
        doctor_lat = coordinates[doctor]['latitude']

        for patient_cluster in patient_clusters:
            dists = []
            for patient in patient_cluster:
                patient_long = coordinates[patient]['longitude']
                patient_lat = coordinates[patient]['latitude']

                dist = city_distance_estimate(doctor_long, doctor_lat, patient_long, patient_lat)
                dists.append(dist)

            min_distance = min(dists)
            nearest_patient_dist[doc_idx].append(min_distance)
        
        preferences[doc_idx] = [i[0] for i in sorted(enumerate(nearest_patient_dist), key=lambda x:x[1])]
    
    return preferences

def cluster_matching(preferences, num_doctors):
    """ Implementation of Gale-Shapely to find a stable doctor/patient list matching.
    
    Parameters:
        num_doctors: the number of doctors.
        preferences: list containing the patient list preferences of each doctor.
    
    Returns:
        A matching of doctors and patient clusters.
    """
    assigned_clusters = [None for i in range(num_doctors)]

    while None in assigned_clusters:
        for index, cluster in enumerate(assigned_clusters):
            if cluster == None:
                for pref_index, preference in enumerate(preferences[index]):
                    assigned = False
                    if preference not in assigned_clusters:
                        assigned_clusters[index] = preference
                        assigned = True
                    else:
                        assignee = assigned_clusters.index(preference)
                        assignee_preference = preferences[assignee].index(preference)
                        if assignee_preference > pref_index:
                            assigned_clusters[index] = preference
                            assigned_clusters[assignee] = None
                            assigned = True
                    if assigned:
                        break
    
    return assigned_clusters
                    
