import heapq
from .models import Node, Edge


def dijkstra(source_id, destination_id):
    nodes = Node.objects.all()
    edges = Edge.objects.all()

    graph = {node.id: [] for node in nodes}

    for edge in edges:
        graph[edge.source.id].append((edge.destination.id, edge.latency))

    pq = [(0, source_id, [])]  # (cost, node, path)
    visited = set()

    while pq:
        cost, current, path = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        path = path + [current]

        if current == destination_id:
            return cost, path

        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path))

    return None, []