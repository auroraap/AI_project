import csv

def build_city_graph(filename):
    file = open(filename, "r")
    map_data = list(csv.DictReader(file, delimiter=","))
    file.close()

    graph = {}

    for data in map_data:
        node = data["From"]

        if node not in graph.keys():
            graph[node] = {
                "neighbors": [],
                "distances": [],
            }
            
        neighbor = data["To"]
        distance = data["Distance"]

        graph[node]["neighbors"].append(neighbor)
        graph[node]["distances"].append(distance)

    return graph
