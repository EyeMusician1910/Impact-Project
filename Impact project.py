import heapq

def visualize_path(path, distances):
    """
    Visualizes the shortest path between stations.

    Args:
        path: A list of stations representing the shortest path.
        distances: A dictionary of distances from the start station to each station.

    Returns:
        A string representing the visualized path.
    """

    if len(path) == 1:
        return f"{path[0]}"  # Just return the station name if there's only one

    visualized_path = f"{path[0]}"
    for i in range(1, len(path)):
        prev_station = path[i - 1]
        current_station = path[i]
        # Fetch the distance between the previous and current station
        distance = distances[current_station] - distances[prev_station]
        visualized_path += f" → ({distance}) → {current_station}"

    return visualized_path

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))  # Assuming undirected graph

    def dijkstra(self, start, end):
        # Min-heap priority queue
        min_heap = [(0, start)]  # (distance, station)
        distances = {station: float('inf') for station in self.graph}
        distances[start] = 0
        previous = {station: None for station in self.graph}

        while min_heap:
            current_distance, current_station = heapq.heappop(min_heap)

            if current_station == end:
                break

            if current_distance > distances[current_station]:
                continue

            for neighbor, weight in self.graph[current_station]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_station
                    heapq.heappush(min_heap, (distance, neighbor))

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()
        return distances[end], path, distances

# Create the graph
graph = Graph()

# Input
num_stations = int(input("Enter the number of stations: "))
stations = []
print("Enter the names of the stations:")
for _ in range(num_stations):
    station_name = input(f"Station {_ + 1}: ")
    stations.append(station_name)

for station in stations:
    print(f"\nEnter the routes from '{station}':")
    num_routes = input("How many routes are available (or type 'none' if none): ").strip().lower()

    if num_routes == "none":
        continue
    else:
        num_routes = int(num_routes)

    for _ in range(num_routes):
        while True:
            try:
                destination = input("Enter destination station: ").strip()
                distance = int(input("Enter distance to the destination: ").strip())
                graph.add_edge(station, destination, distance)
                break
            except ValueError:
                print("Invalid input. Please ensure the distance is a number.")

# Input start and end stations
start_station = input("\nEnter the start station: ")
end_station = input("Enter the end station: ")

# Get the shortest route
distance, path, distances = graph.dijkstra(start_station, end_station)

# Visualize and print the shortest path
if distance == float('inf'):
    print(f"\nNo path exists between {start_station} and {end_station}.")
else:
    print(f"\nShortest Path: {visualize_path(path, distances)}")
    print(f"Total Distance: {distance}")
