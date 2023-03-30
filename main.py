import sys
from build_map import build_city_graph

def main() -> int:

    turkey_map = build_city_graph("distances.csv")
    num_cities = len(turkey_map)

    print("Number of cities: {num_cities}".format(num_cities=num_cities))

    return 0

if __name__ == '__main__':
    sys.exit(main())