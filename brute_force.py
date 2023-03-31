import random
import time

def brute_force_search(graph, patient_locations, doctor_locations):
    """
    Brute force approach to solving the multi doctor graph traversal.
    """
    start_timespamp = time.time_ns()

    solution = [[], [], []]

    # Check if the doctors start at a patient location
    for doctor_index, doctor_location in enumerate(doctor_locations):
        if doctor_location in patient_locations:
            patient_locations = list(filter((doctor_location).__ne__, patient_locations))
        # Add initial positions to solution
        solution[doctor_index].append({doctor_location, 0})

    while patient_locations:
        print(len(patient_locations))
        for doctor_index, doctor_location in enumerate(doctor_locations):
            # Initialize empty step
            doctor_step = {}
            for neighbor_index, neighbor in enumerate(graph[doctor_location]["neighbors"]):
                # Iterate through neighbors of the current selected doctor
                if neighbor in patient_locations:
                    # Remove location from patient list
                    patient_locations = list(filter((neighbor).__ne__, patient_locations))
                    doctor_step_length = graph[doctor_location]["distances"][neighbor_index]
                    # Go to patient location if it is a neighbor
                    doctor_locations[doctor_index] = neighbor
                    doctor_step = {"location": doctor_location, "step length": doctor_step_length}

                    
                    break
            if not doctor_step:
                # If no neighbor was a patient location, choose next location at random
                neighbor_index = random.randrange(start=0,stop=len(graph[doctor_location]["neighbors"])-1)
                doctor_step_length = graph[doctor_location]["distances"][neighbor_index]
                doctor_locations[doctor_index] = graph[doctor_location]["neighbors"][neighbor_index]

                doctor_step = {"location": doctor_location, "step length": doctor_step_length}
                
            # add location to solution
            solution[doctor_index].append(doctor_step)

    end_timespamp = time.time_ns()
    print("Runtime in ns: {runtime}".format(runtime=end_timespamp-start_timespamp))

    return solution
