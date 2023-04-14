import random
import time

def brute_force_search(graph, patient_locations, doctor_locations):
    """ Solves the TSP with a brute force approach.
    
    Parameters:
        graph: graph containing nodes with lists of neighbors and distances.
        patient_locations: list of the locations of each patient.
        doctor_locations: list of the locations of each doctor.
    
    Returns:
        A list containing all the steps that each doctor made.
    """
    start_timespamp = time.time_ns()

    solution = [[] for i in range(len(doctor_locations)) ]

    # Check if the doctors start at a patient location
    for doctor_index, doctor_location in enumerate(doctor_locations):
        if doctor_location in patient_locations:
            patient_locations = list(filter((doctor_location).__ne__, patient_locations))
        # Add initial positions to solution
        solution[doctor_index].append({"location": doctor_location, "step length": 0})

    while patient_locations:
        for doctor_index, doctor_location in enumerate(doctor_locations):
            # Initialize empty step
            doctor_step = {}
            for neighbor_index, neighbor in enumerate(graph[doctor_location]["neighbors"]):
                # Iterate through neighbors of the current selected doctor
                if neighbor in patient_locations:
                    # Go to patient location if it is a neighbor
                    # Remove location from patient list
                    patient_locations = list(filter((neighbor).__ne__, patient_locations))
                    # Store the step
                    doctor_step_length = graph[doctor_location]["distances"][neighbor_index]
                    doctor_locations[doctor_index] = neighbor
                    doctor_step = {"location": doctor_location, "step length": doctor_step_length}

                    break
            if not doctor_step:
                # If no neighbor is a patient location, choose next location at random
                neighbor_index = random.randint(0,len(graph[doctor_location]["neighbors"])-1)
                # Store the step
                doctor_step_length = graph[doctor_location]["distances"][neighbor_index]
                doctor_locations[doctor_index] = graph[doctor_location]["neighbors"][neighbor_index]
                doctor_step = {"location": doctor_location, "step length": doctor_step_length}
                
            # add location to solution
            solution[doctor_index].append(doctor_step)

    end_timespamp = time.time_ns()
    print("Runtime in ns: {runtime}".format(runtime=end_timespamp-start_timespamp))

    return solution
