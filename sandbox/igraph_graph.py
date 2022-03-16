from igraph import *

# example graphs from Wang et al. 2013
dag = Graph(directed = True) # directed acyclic graph, no composite nodes
dag.add_vertices(10)
dag.add_edges([(0,1), (0,2), (0,3), (1,4), (2,5), (1,5), (3,2), (3,6), (4,7), (5,7), (5,9), (7,9), (6,8), (6,9), (8,9)])
dag.vs["name"] = ["I", "A", "B", "C", "D", "E", "F", "G", "H", "O"]

dcg = Graph(directed = True) # directed cyclic graph, no composite nodes
dcg.add_vertices(8)
dcg.add_edges([(0,1), (0,2), (0,3), (3,4), (4,2), (2,5), (1,5), (5,4), (4,6), (6,5), (5,7), (6,7)])
dcg.vs["name"] = ["I", "A", "B", "C", "D", "E", "F", "O"]
