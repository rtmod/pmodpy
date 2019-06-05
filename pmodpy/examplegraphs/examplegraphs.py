#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 14:54:41 2017

@author: luissordovieira

`Kite`, `House`, and `Routers` graphs from:
    Albin, Sahneh, Goering, Poggi-Corradini (2014)
    "Modulus of families of walks on graphs"
    https://arxiv.org/abs/1401.7640
`Contacts` graph from:
    Albin, Brunner, Perez, Poggi-Corradini, Wiens (2015)
    "Modulus on graphs as a generalization of standard graph theoretic
    quantities"
    _Conformal Geometry and Dynamics_
    http://www.ams.org/journals/ecgd/2015-19-13/S1088-4173-2015-00287-8/
`Connecting_*` graphs from:
    Shakeri, Poggi-Corradini, Scoglio, Albin (2016)
    "Generalized network measures based on modulus of families of walks"
    _Journal of Computational and Applied Mathematics_
    https://www.sciencedirect.com/science/article/pii/S0377042716300061
`Paw`, `Diamond`, and `Broadcast` graphs from:
    Albin, Kottegoda, Poggy-Corradini (2019)
    "Spanning tree modulus for secure broadcast games"
    https://arxiv.org/abs/1904.03962

Notice that the indexing on vertices is shifted by -1.

"""

import igraph

def Kite():
    kite = igraph.Graph()
    kite.add_vertices(4)
    kite.add_edges([(0, 2), (0, 3), (1, 3), (2, 3)])
    return kite

def House():
    house = igraph.Graph()
    house.add_vertices(5)
    house.add_edges([(0, 1), (0, 4), (4, 1), (0, 3), (3, 2), (2, 1)])
    return house

def Routers():
    routers = igraph.Graph()
    routers.add_vertices(15)
    routers.add_edges([
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 7), (2, 8), (2, 5), (3, 6), (3, 7),
        (4, 8), (5, 9), (5, 13), (5, 10), (6, 10), (7, 10), (7, 11),
        (8, 12), (9, 12), (9, 13), (10, 13), (11, 13),
        (12, 14), (13, 14)
    ])
    return routers

def Paw():
    paw = igraph.Graph()
    paw.add_vertices(4)
    paw.add_edges([(0, 1), (1, 2), (1, 3), (2, 3)])
    return paw

def Diamond():
    diamond = igraph.Graph()
    diamond.add_vertices(4)
    diamond.add_edges([(0, 1), (1, 2), (2, 3), (0, 3), (1, 3)])
    return diamond

def Contacts():
    contacts = igraph.Graph()
    contacts.add_vertices(21)
    # u = 0, s = 1, t = 4, v = 20
    contacts.add_edges([
        (0, 1),
        (1, 2), (1, 3), (1, 4), (2, 4), (3, 4),
        (2, 5), (4, 5), (3, 7), (4, 7), (4, 6),
        (5, 8), (8, 11), (11, 14), (14, 17),
        (6, 9), (9, 12), (12, 15), (15, 18),
        (7, 10), (10, 13), (13, 16), (16, 19),
        (17, 20), (18, 20), (19, 20)
    ])
    return contacts

def Connecting_a():
    Connecting_a=igraph.Graph();
    Connecting_a=Connecting_a.as_directed()
    Connecting_a.add_vertices(9);
    Connecting_a.add_edges([
        (0,1),(1,2),(2,5),(3,1),(6,3),(8,6),(1,4),(4,7),(7,8),(5,8)
    ]);
    return Connecting_a

def Connecting_b():
    Connecting_b=igraph.Graph();
    Connecting_b=Connecting_b.as_directed()
    Connecting_b.add_vertices(9);
    Connecting_b.add_edges([
        (0,1),(1,2),(2,5),(1,3),(3,6),(6,8),(1,4),(4,7),(7,8),(5,8)
    ]);
    return Connecting_b

def Connecting_c():
    Connecting_c=igraph.Graph();
    Connecting_c=Connecting_c.as_directed()
    Connecting_c.add_vertices(9);
    Connecting_c.add_edges([
        (0,1),(1,2),(2,5),(1,3),(3,6),(3,6),(6,8),(1,4),(4,7),(7,8),(5,8)
    ]);
    return Connecting_c

def Connecting_d():
    Connecting_d=igraph.Graph();
    Connecting_d=Connecting_d.as_directed()
    Connecting_d.add_vertices(9);
    Connecting_d.add_edges([
        (0,1),(1,2),(2,5),(1,3),(3,6),(3,6),(6,8),(1,4),
        (4,7),(7,8),(5,8),(3,2),(6,5),(3,4),(6,7)
    ]);
    return Connecting_d

def Broadcast():
    K5 = igraph.Graph.Full(5);
    Broadcast = igraph.Graph.disjoint_union(K5, K5);
    Broadcast.add_edges([(0, 5), (2, 7)]);
    return Broadcast

# This reads an table of edges and creates a directed graph.
# If you want undirected, choose `directed=False`
# Note that the vertices are still labeled by numbers
# To get which label corresponds to which vertex,
# use `vs=igraph.VertexSeq(Dummy_Social_Network)`
# ```py
# for i in vs:
#    print(i)
# ```

# ```py
# igraph.read("smallgraph.edgelist", format="ncol", directed=False, names=True)
# dummy_weighted = igraph.Graph.Read_Ncol("Graphs/dummy_weighted_2",
#                                         directed=False)
# ```

# To use, in your console running the main script, incude
# ```py
# from ExampleGraphs import House
# ```
# Now a graph `House` is stored, and you can call `main(None,House,p,s,t,eps)`

# ```py
# import igraph.remote
# import igraph.remote.nexus
# # UNABLE TO EXECUTE VARIANTS ON THIS STEP
# karate = igraph.remote.nexus.get("karate")
# ```
