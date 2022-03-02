from igraph import Graph



line = Graph(directed=True)
line.add_vertices(3)
line.add_edges([(0, 1), (1, 2)])
print(line)


graph = Graph(directed = True)
graph.add_vertices(5)
graph.add_edges([(0,1), (0,2), (2,1), (1,3), (3,2), (1,4), (3,4)])
print(graph)