# Shortest Path Visualizer (Dijkstra's Algorithm)

This Python program computes and visualizes the shortest path between stations in a weighted graph using **Dijkstra's Algorithm**.

---

## Features
1. **Graph Representation**: Uses an adjacency list for stations and routes.
2. **User Input**: Input stations, routes, and distances interactively.
3. **Shortest Path**: Computes the shortest path using Dijkstra's Algorithm.
4. **Path Visualization**: Displays the shortest path and distances.

---

## Code Overview

### Graph Class
- **add_edge(u, v, weight)**: Adds an edge between stations.
- **dijkstra(start, end)**: Computes the shortest path using Dijkstra's algorithm.

### Path Visualization
Displays the shortest path, e.g.:
A → (4) → B → (1) → C

---

## Dijkstra's Algorithm
1. **Initialization**: Set distances to infinity, with the start node as 0.
2. **Relaxation**: Update distances for neighbors.
3. **Path Reconstruction**: Backtrack using a `previous` dictionary.

### Complexity:
- **Time**: O(E + V log V)
- **Space**: O(V + E)

---

## Example

### Input:
Stations: A, B, C Routes from A: B (4), C (7) Routes from B: C (1) Start: A, End: C

### Output:
Shortest Path: A → (4) → B → (1) → C Total Distance: 5

---

## Extensions
- **Directed Graph**: Modify edge direction.
- **Multiple Algorithms**: Add Bellman-Ford or Floyd-Warshall.
