#!/novo/users/zell/Python-3.9/bin/python3.9
import requests, heapq, csv, sys
start = sys.argv[2]
end = sys.argv[3]
if "9606.ENS" not in start: start = requests.post("https://string-db.org/api/json/get_string_ids", data = {"identifiers": start, "species": 9606, "limit": 999, "caller_identity": "Zelin Li"}).json()[0]['stringId']
if "9606.ENS" not in end: end = requests.post("https://string-db.org/api/json/get_string_ids", data = {"identifiers": end, "species": 9606, "limit": 999, "caller_identity": "Zelin Li"}).json()[0]['stringId']
try:
    graph = {}
    with open(sys.argv[1], 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ')
        next(csvreader)
        for row in csvreader:
            start_node, end_node, weight = row
            weight = float(weight)
            if start_node not in graph:
                graph[start_node] = {}
            graph[start_node][end_node] = 1/weight
            if end_node not in graph:
                graph[end_node] = {}
            graph[end_node][start_node] = 1/weight
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]
    previous_vertices = {vertex: None for vertex in graph}
    while heap:
        (current_distance, current_vertex) = heapq.heappop(heap)
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(heap, (distance, neighbor))
    sum_score = distances[end]
    path = []
    vertex = end
    while vertex != start:
        path.append(vertex)
        vertex = previous_vertices[vertex]
    path.append(start)
    path.reverse()
except:
    sum_score = 'No path found!'
    path = [start, end]
combined_paths = "\r".join(path)
parmas = {
    "identifiers": combined_paths,
    "species": 9606,
    "required_score": 1,
    "block_structure_pics_in_bubbles": 1,
    "network_type": "physical",
    "caller_identity": "Zelin Li"
    }
stringIdparmas = {
    "identifiers": combined_paths,
    "species": 9606,
    "limit": 999,
    "caller_identity": "Zelin Li"
    }
print('Sum of reversed scores:', sum_score)
print("Shortest path:", [i['preferredName'] for i in requests.post("https://string-db.org/api/json/get_string_ids", data = stringIdparmas).json()])
print("STRING's link:", requests.post("https://string-db.org/api/json/get_link", data = parmas).json()[0])
