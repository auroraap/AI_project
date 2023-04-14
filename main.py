import random
import sys

from graph_utils import build_graph, get_coordinates, kmeans, visualize
from brute_force import brute_force_search
from evaluate_solution import evaluate
from matching import cluster_matching, cluster_preferences

def main() -> int:
    # Build map from dataset
    turkey_map = build_graph("distances.csv")

    ans = input("Run coordinate collection (y/n)? ")
    if ans == 'y':
        get_coordinates(turkey_map)

    # Problem definition
    num_cities = len(turkey_map)
    num_patients = 40
    num_doctors = 3
    patient_locations = random.choices(list(turkey_map.keys()), k=num_patients)
    doctor_locations = random.choices(list(turkey_map.keys()), k=num_doctors)

    print("######## MEDICAL AID ALLOCATION OPTIMIZATION PROBLEM ########")
    print("Number of cities: {num_cities}".format(num_cities=num_cities))
    print("Number of doctors: {num_doctors}".format(num_doctors=num_doctors))
    print("Doctor locations (repetition allowed): {doctor_locations}".format(doctor_locations=doctor_locations))
    print("Number of patients: {num_patients}".format(num_patients=num_patients))
    print("Patient locations (repetition allowed): {patient_locations}\n\n".format(patient_locations=patient_locations))

    print("######## Brute force result ########")
    brute_force_solution = brute_force_search(graph=turkey_map, patient_locations=patient_locations, doctor_locations=doctor_locations)
    brute_force_performance = evaluate(brute_force_solution, num_doctors)
    print("Total distance travelled: {total_dist}".format(total_dist = brute_force_performance[0]))
    print("Travel distance distribution index: {total_dist}\n\n".format(total_dist = brute_force_performance[1]))


    print("######## Brute force with clustering of patients and doctor matching ########")
    cluster_ok = False
    i = 0
    while not cluster_ok:
        # Redo clustering step until clusters are more or less evenly sized
        try:
            i += 1
            clusters = kmeans(json_filename='turkey_coordinates.json', patient_locations=patient_locations, k=num_doctors)
            for cluster in clusters:
                if len(cluster) < (num_patients / 6):
                    raise(ValueError)
            cluster_ok = True
        except:
            # print("One or more clusters have too fiew elements. Retrying. Iteration: {i}".format(i=i))
            continue
    preferences = cluster_preferences(doctor_locations=doctor_locations, patient_clusters=clusters)
    matching = cluster_matching(preferences=preferences, num_doctors=num_doctors)
    dist = 0
    for i, doctor in enumerate(doctor_locations):
        cluster = matching[i]
        brute_force_cluster = brute_force_search(graph=turkey_map, patient_locations=clusters[cluster], doctor_locations=[doctor_locations[i]] )
        brute_force_performance = evaluate(brute_force_cluster, 1)
        dist += brute_force_performance[0]
    print("Total distance travelled: {total_dist}".format(total_dist = dist))
    visualize(turkey_map=turkey_map, clusters=clusters)

    # Informed search: we have x and y coordinates of each city. Use clustering to create a collection of patients for each doctor.
    # Distribute clusters between doctors.
    # Create a minimal spanning tree for each doctor (Prim/Kruskal)
    # Let each doctor traverse the MST to visit their patients

    return 0

if __name__ == '__main__':
    sys.exit(main())