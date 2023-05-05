import random
import sys

from graph_utils import build_graph, get_coordinates, kmeans, visualize, evaluate
from search_algorithms.brute_force import brute_force_search
from matching import cluster_matching, cluster_preferences
from search_algorithms.gradient_descent import gradient_descent

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

    cluster_ok = False
    i = 0
    while not cluster_ok:
        # Redo clustering step until clusters are more or less evenly sized
        try:
            i += 1
            clusters = kmeans(json_filename='turkey_coordinates.json', patient_locations=patient_locations, k=num_doctors)
            for cluster in clusters:
                if len(cluster) < (num_patients / 6):
                    # Ensure quite even patient distribution
                    raise(ValueError)
            cluster_ok = True
            # visualize(turkey_map=turkey_map, clusters=clusters, doctors=doctor_locations)
        except:
            continue
    preferences = cluster_preferences(doctor_locations=doctor_locations, patient_clusters=clusters)
    matching = cluster_matching(preferences=preferences, num_doctors=num_doctors)

    print("######## Gradient method result ########")
    gradient_solution = []
    for i, doctor in enumerate(doctor_locations):
        cluster = matching[i]
        assigned_patients = clusters[cluster]
        solution = gradient_descent(doctor_location=doctor, patient_list=assigned_patients, graph=turkey_map)
        gradient_solution.append(solution)

    gradient_performance = evaluate(solution=gradient_solution, n_doctors=num_doctors)
    print("Total distance travelled: {total_dist}".format(total_dist = gradient_performance[0]))
    print("Travel distance distribution index: {total_dist}\n\n".format(total_dist = gradient_performance[1]))

    return 0

if __name__ == '__main__':
    sys.exit(main())