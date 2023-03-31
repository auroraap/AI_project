import collections

def evaluate(solution, n_doctors):
    total_distance = 0
    doctor_distance = [0] * n_doctors
    for doctor_index, doctor_solution in enumerate(solution):
        for step in doctor_solution:
            total_distance += int(step['step length'])
            doctor_distance[doctor_index] += int(step['step length'])
    
    gini = 1
    for distance in doctor_distance:
        gini -= (distance / total_distance) ** 2
    
    return [total_distance, gini]
        