import random
import sys

from build_map import build_graph
from brute_force import brute_force_search
from evaluate_solution import evaluate

def main() -> int:
    # Build map from dataset
    turkey_map = build_graph("distances.csv")

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
    print("Patient locations (repetition allowed): {patient_locations}".format(patient_locations=patient_locations))

    # Run the different algorithms to get solutions for the paths of the 3 doctors
    brute_force_solution = brute_force_search(graph=turkey_map, patient_locations=patient_locations, doctor_locations=doctor_locations)
    brute_force_performance = evaluate(brute_force_solution, num_doctors)
    print("######## Brute force result ########")
    print("Total distance travelled: {total_dist}".format(total_dist = brute_force_performance[0]))
    print("Travel distance distribution index: {total_dist}".format(total_dist = brute_force_performance[1]))
    # Evaluate the solutions with respect to distance travelled in total

    return 0

if __name__ == '__main__':
    sys.exit(main())