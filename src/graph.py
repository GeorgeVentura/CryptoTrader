import math


class Graph:

    def __init__(self):
        self.graph = dict()

    def add_edge(self, v1, v2, w):
        if v1 not in self.graph:
            self.graph[v1] = {}
        self.graph[v1][v2] = -math.log(w)
        if v2 not in self.graph:
            self.graph[v2] = {}
        self.graph[v2][v1] = math.log(w)

    def set_weight(self, u, v, w):
        print("updating: " + u + " -> " + v + " = " + str(w))
        self.graph[u][v] = -math.log(w)
        self.graph[v][u] = math.log(w)

    def get_vertices(self):
        vertices = []
        for k in self.graph.keys():
            vertices.append(k)
        return vertices

    def get_edges(self, vertex):
        return self.graph[vertex]

    def get_edge_weight(self, u, v):
        return self.graph[u][v]

    def retrace_loop(self, p, start):
        arbitrageLoop = [start]
        prev_node = start
        while True:
            prev_node = p[prev_node]
            if prev_node not in arbitrageLoop:
                arbitrageLoop.append(prev_node)
            else:
                arbitrageLoop.append(prev_node)
                arbitrageLoop = arbitrageLoop[arbitrageLoop.index(prev_node):]
                #self.export_DOT_path(list(reversed(arbitrageLoop)))
                return list(reversed(arbitrageLoop))

    def bellman_ford(self, src):

        dist = dict()
        pred = dict()
        vertices = self.get_vertices()

        # Initialize distances from src to infinity.
        for vertex in vertices:
            dist[vertex] = float("Inf")
            pred[vertex] = None
        dist[src] = 0

        # Relax all edges |V| - 1 times.
        for i in range(len(self.graph) - 1):
            for u in self.graph:
                for v in self.graph[u]:
                    self.relax(u, v, dist, pred)

        # negative cycles
        for u in self.graph:
            for v in self.graph[u]:
                if dist[v] < dist[u] + self.graph[u][v]:
                    return self.retrace_loop(pred, v)
        return None

    def relax(self, node, neighbour, d, p):
        dist = self.graph[node][neighbour]
        if d[neighbour] > d[node] + dist:
            d[neighbour] = d[node] + dist
            p[neighbour] = node

    # DOT language
    # https://en.wikipedia.org/wiki/DOT_(graph_description_language)
    def export_DOT(self):
        print("digraph {")
        for u in self.graph:
            print(u)
        print("\n")
        for u in self.graph:
            for v in self.graph[u]:
                print(u + " -> " + v + " [label=" + str(self.graph[u][v]) + "]")
        print("}")

    def export_DOT_path(self, path):
        print("digraph {")
        for i in range(len(path)-1):
            print(path[i] + " -> " + path[i+1] + "[label=" + str(self.graph[path[i]][path[i+1]]) + "]")

        print("}")

