import sys
import random
from build_map import build_graph

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
    # Evaluate the solutions with respect to distance travelled in total

    return 0

if __name__ == '__main__':
    sys.exit(main())