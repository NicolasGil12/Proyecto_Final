from queue import PriorityQueue

class Graph:
    def __init__(self, vertex_number):
        self.v = vertex_number
        self.edges = [[-1 for i in range(vertex_number)] for j in range(vertex_number)]
        self.visited = []

    def add_edges(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight

    def dijkstra(graph, vertex):
        D = {v:float('inf') for v in range(graph.v)}
        D[vertex] = 0

        pq = PriorityQueue()
        pq.put((0, vertex))

        while not pq.empty():
            (dist, vertex) = pq.get()
            graph.visited.append(vertex)

            for neighbour in range(graph.v):
                if graph.edges[vertex][neighbour] != -1:
                    distance = graph.edges[vertex][neighbour]
                    if neighbour not in graph.visited:
                        old_cost = D[neighbour]
                        new_cost = D[vertex] + distance
                        if new_cost < old_cost:
                            pq.put((new_cost, neighbour))
                            D[neighbour] = new_cost
        return D