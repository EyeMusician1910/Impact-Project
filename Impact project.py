import heapq
import tkinter as tk
from tkinter import ttk
import time

def visualize_path(path, distances):
    """
    Visualizes the shortest path between stations.
    """
    if len(path) == 1:
        return f"{path[0]}"

    visualized_path = f"{path[0]}"
    for i in range(1, len(path)):
        prev_station = path[i - 1]
        current_station = path[i]
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
        self.graph[v].append((u, weight))

    def dijkstra(self, start, end):
        min_heap = [(0, start)]
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

# GUI Setup
window = tk.Tk()
window.title("Shortest Path Finder")
window.geometry("900x700")
window.configure(bg="#eaf2f8")

# Style configuration
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", background="#eaf2f8", font=("Arial", 12))

# Input Frame
input_frame = ttk.Frame(window, padding=20)
input_frame.pack(fill="x", padx=20, pady=10)

stations_label = ttk.Label(input_frame, text="Enter station names (comma-separated):", font=("Arial", 14))
stations_label.pack(anchor="w")
stations_entry = ttk.Entry(input_frame, font=("Arial", 12), width=60)  # Removed unsupported options
stations_entry.insert(0, "e.g., Station1, Station2, Station3")
stations_entry.pack(fill="x", pady=5)

routes_frame = ttk.Frame(window, padding=20)
routes_frame.pack(fill="x", padx=20, pady=10)

routes_label = ttk.Label(routes_frame, text="Enter routes (Station1, Station2, Distance):", font=("Arial", 14))
routes_label.pack(anchor="w")
routes_text = tk.Text(routes_frame, font=("Arial", 12), height=8, width=70, relief="solid", bg="#ffffff")
routes_text.insert("1.0", "e.g., Station1, Station2, 10\nStation2, Station3, 15")
routes_text.pack(fill="x", pady=5)

path_frame = ttk.Frame(window, padding=20)
path_frame.pack(fill="x", padx=20, pady=10)

start_label = ttk.Label(path_frame, text="Start Station:", font=("Arial", 12))
start_label.grid(row=0, column=0, sticky="e", padx=5)
start_entry = ttk.Entry(path_frame, font=("Arial", 12), width=20)  # Removed unsupported options
start_entry.grid(row=0, column=1, padx=5)

end_label = ttk.Label(path_frame, text="End Station:", font=("Arial", 12))
end_label.grid(row=0, column=2, sticky="e", padx=5)
end_entry = ttk.Entry(path_frame, font=("Arial", 12), width=20)  # Removed unsupported options
end_entry.grid(row=0, column=3, padx=5)

# Output Frame
output_frame = ttk.Frame(window, padding=20)
output_frame.pack(fill="x", padx=20, pady=10)

output_label = ttk.Label(output_frame, text="", font=("Arial", 14), wraplength=800, background="#d5f5e3")
output_label.pack(fill="x", pady=5)

loading_label = ttk.Label(output_frame, text="", font=("Arial", 14), foreground="#999", background="#eaf2f8")

def animate_loader():
    """
    Animates a loader with dots.
    """
    dots = ["", ".", "..", "..."]
    for i in range(len(dots)):
        loading_label.config(text=f"Calculating shortest path{dots[i]}")
        loading_label.update()
        time.sleep(0.4)

def animated_output(text):
    """
    Animates the display of the output text.
    """
    output_label.config(text="")
    for i in range(len(text)):
        output_label.config(text=text[:i + 1])
        output_label.update()
        time.sleep(0.03)

def find_path():
    """
    Finds the shortest path between the start and end stations.
    """
    # Parse stations
    stations = [s.strip() for s in stations_entry.get().split(",") if s.strip()]
    if not stations:
        output_label.config(text="Please enter station names.")
        return

    # Parse routes
    graph.graph.clear()
    routes = routes_text.get("1.0", "end").strip().split("\n")
    for route in routes:
        try:
            station1, station2, distance = route.split(",")
            station1 = station1.strip()
            station2 = station2.strip()
            distance = int(distance.strip())
            if station1 in stations and station2 in stations:
                graph.add_edge(station1, station2, distance)
            else:
                output_label.config(text=f"Invalid station in route: {route}")
                return
        except ValueError:
            output_label.config(text=f"Invalid route format: {route}")
            return

    # Parse start and end stations
    start_station = start_entry.get().strip()
    end_station = end_entry.get().strip()

    if start_station not in stations or end_station not in stations:
        output_label.config(text="Start or end station is invalid.")
        return

    # Show loading animation
    loading_label.pack()
    animate_loader()
    loading_label.pack_forget()

    # Calculate shortest path
    try:
        distance, path, distances = graph.dijkstra(start_station, end_station)
    except KeyError:
        output_label.config(text="Invalid start or end station.")
        return

    # Display result
    if distance == float('inf'):
        animated_output(f"No path exists between {start_station} and {end_station}.")
    else:
        animated_output(f"Shortest Path: {visualize_path(path, distances)}\nTotal Distance: {distance}")

find_path_button = ttk.Button(window, text="Find Shortest Path", command=find_path, style="TButton")
find_path_button.pack(pady=20)

window.mainloop()
