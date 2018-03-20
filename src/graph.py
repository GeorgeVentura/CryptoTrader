'''

'''

import math


class Graph:

    def __init__(self):
        self.graph = dict()

    def add_edge(self, v1, v2, w):
        print("updating: " + v1 + " -> " + v2 + " = " + str(w))
        if v1 not in self.graph:
            self.graph[v1] = {}
        self.graph[v1][v2] = -math.log(w)
        if v2 not in self.graph:
            self.graph[v2] = {}
        self.graph[v2][v1] = math.log(w)

    def get_edges(self, vertex):
        return self.graph[vertex]

    def get_edge_weight(self, u, v):
        return self.graph[u][v]

    @staticmethod
    def get_vertices(graph):
        vertices = []
        for k in graph.keys():
            vertices.append(k)
        return vertices

    @staticmethod
    def retrace_loop(p, start):
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

    @staticmethod
    def bellman_ford(src, graph):

        dist = dict()
        pred = dict()
        vertices = Graph.get_vertices(graph)

        # Initialize distances from src to infinity.
        for vertex in vertices:
            dist[vertex] = float("Inf")
            pred[vertex] = None
        dist[src] = 0

        # Relax all edges |V| - 1 times.
        for i in range(len(graph) - 1):
            for u in graph:
                for v in graph[u]:
                    Graph.relax(u, v, dist, pred, graph)

        # negative cycles
        for u in graph:
            for v in graph[u]:
                if dist[v] < dist[u] + graph[u][v]:
                    return Graph.retrace_loop(pred, v)
        return None

    @staticmethod
    def relax(node, neighbour, d, p, graph):
        dist = graph[node][neighbour]
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

