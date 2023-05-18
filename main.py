import random
import sys

from graph_utils import build_graph, get_coordinates, kmeans, visualize, evaluate
from search_algorithms.brute_force import brute_force_search
from matching import cluster_matching, cluster_preferences
from search_algorithms.gradient_descent import gradient_descent
from search_algorithms.nearest_neighbor import nearest_neighbor_search

NUM_RUNS = 1
PRINT = False

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

    # Initialize performance numbers
    brute_force_distance, brute_force_gini = 0, 0
    gradient_distance, gradient_gini = 0, 0
    nn_distance, nn_gini = 0, 0

    for i in range (NUM_RUNS):
        print("Run number {n}.".format(n=i+1))
        patient_locations = random.choices(list(turkey_map.keys()), k=num_patients)
        doctor_locations = random.choices(list(turkey_map.keys()), k=num_doctors)

        if PRINT:
            print("######## MEDICAL AID ALLOCATION OPTIMIZATION PROBLEM ########")
            print("Number of cities: {num_cities}".format(num_cities=num_cities))
            print("Number of doctors: {num_doctors}".format(num_doctors=num_doctors))
            print("Doctor locations (repetition allowed): {doctor_locations}".format(doctor_locations=doctor_locations))
            print("Number of patients: {num_patients}".format(num_patients=num_patients))
            print("Patient locations (repetition allowed): {patient_locations}\n\n".format(patient_locations=patient_locations))

        # ~~~~~~~~~~~~~~~ RUN BRUTE FORCE ~~~~~~~~~~~~~~~
        brute_force_solution = brute_force_search(graph=turkey_map, patient_locations=patient_locations.copy(), doctor_locations=doctor_locations)
        brute_force_performance = evaluate(brute_force_solution, num_doctors)
        brute_force_distance += brute_force_performance[0]
        brute_force_gini += brute_force_performance[1]

        # ~~~~~~~~~~~~~~~ RUN PATIENT CLUSTERING ~~~~~~~~~~~~~~~
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
                
            except:
                continue
        preferences = cluster_preferences(doctor_locations=doctor_locations, patient_clusters=clusters)
        matching = cluster_matching(preferences=preferences, num_doctors=num_doctors)

        # ~~~~~~~~~~~~~~~ RUN GRADIENT ~~~~~~~~~~~~~~~
        gradient_solution = []
        for i, doctor in enumerate(doctor_locations):
            cluster = matching[i]
            assigned_patients = clusters[cluster].copy()
            solution = gradient_descent(doctor_location=doctor, patient_list=assigned_patients, graph=turkey_map)
            gradient_solution.append(solution)

        gradient_performance = evaluate(solution=gradient_solution, n_doctors=num_doctors)
        gradient_distance += gradient_performance[0]
        gradient_gini += gradient_performance[1]

        # ~~~~~~~~~~~~~~~ RUN NEAREST NEIGHBOR ~~~~~~~~~~~~~~~
        nn_solution = []
        for i, doctor in enumerate(doctor_locations):
            cluster = matching[i]
            assigned_patients = clusters[cluster].copy()
            solution = nearest_neighbor_search(doctor_location=doctor, patient_list=assigned_patients, graph=turkey_map)
            nn_solution.append(solution)

        nn_performance = evaluate(solution=nn_solution, n_doctors=num_doctors)
        nn_distance += nn_performance[0]
        nn_gini += nn_performance[1]
        
    print("\n######## RESULTS after {n} runs ########\n".format(n = NUM_RUNS))

    print("~~~~~~ Brute force result ~~~~~~")
    print("Avg. Total distance travelled: {total_dist}".format(total_dist = brute_force_distance / NUM_RUNS))
    print("Avg. Travel distance distribution index: {total_dist}\n".format(total_dist = brute_force_gini / NUM_RUNS))

    print("~~~~~~ Gradient method result ~~~~~~")
    print("Avg. Total distance travelled: {total_dist}".format(total_dist = gradient_distance / NUM_RUNS))
    print("Avg. Travel distance distribution index: {total_dist}\n".format(total_dist = gradient_gini / NUM_RUNS))

    print("~~~~~~ Nearest neighbor result ~~~~~~")
    print("Avg. Total distance travelled: {total_dist}".format(total_dist = nn_distance / NUM_RUNS))
    print("Avg. Travel distance distribution index: {total_dist}\n".format(total_dist = nn_gini / NUM_RUNS))

    visualize(turkey_map=turkey_map, clusters=clusters, doctors=doctor_locations, solutions=nn_solution)

    return 0

if __name__ == '__main__':
    sys.exit(main())