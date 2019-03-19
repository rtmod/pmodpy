#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 14:54:41 2017

@author: luissordovieira
Kite and House graphs from "Modulus of families of walks on Graphs" by Albin et al.
https://arxiv.org/abs/1401.7640
Contacts graph from Albin et al (2015) *Conf Geo Dyn*
http://www.ams.org/journals/ecgd/2015-19-13/S1088-4173-2015-00287-8/
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


def Contacts():
    contacts = igraph.Graph()
    contacts.add_vertices(21)
    contacts.add_edges([(0, 1), (1, 2), (1, 3), (1, 4), (2, 3), (4, 3), (2, 5), (3, 5), (5, 6), (6, 7), (7, 8), (8, 9), (3, 10), (
        10, 11), (11, 12), (12, 13), (13, 14), (3, 15), (4, 15), (15, 16), (16, 17), (17, 18), (18, 19), (9, 20), (14, 20), (19, 20)])
    return contacts


def Routers():
    routers = igraph.Graph()
    routers.add_vertices(15)
    routers.add_edges([
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 7), (2, 8), (2, 6), (3, 6), (3, 7),
        (4, 8), (5, 9), (5, 13), (5, 10), (6, 10), (7, 10), (7, 11),
        (8, 12), (9, 12), (9, 13), (10, 13), (11, 13),
        (12, 14), (13, 14)
    ])
    return Routes

def Shakeri_1c():
    Shakeri_1c=igraph.Graph();
    Shakeri_1c=Shakeri_1c.as_directed()
    Shakeri_1c.add_vertices(9);
    Shakeri_1c.add_edges([(0,1),(1,2),(2,5),(1,3),(3,6),(6,8),(1,4),(4,7),(7,8),(5,8)]);
    Shakeri_1c.es["weight"]=1.0;
    Shakeri_1c[3, 6] = 2;
    return Shakeri_1c

def Shakeri_1b():
    Shakeri_1b=igraph.Graph();
    Shakeri_1b=Shakeri_1b.as_directed()
    Shakeri_1b.add_vertices(9);
    Shakeri_1b.add_edges([(0,1),(1,2),(2,5),(1,3),(3,6),(6,8),(1,4),(4,7),(7,8),(5,8)]);
    return Shakeri_1b

def Shakeri_1a():
    Shakeri_1a=igraph.Graph();
    Shakeri_1a=Shakeri_1a.as_directed()
    Shakeri_1a.add_vertices(9);
    Shakeri_1a.add_edges([(0,1),(1,2),(2,5),(3,1),(6,3),(8,6),(1,4),(4,7),(7,8),(5,8)]);
    return Shakeri_1a

def Shakeri_1d():
    Shakeri_1d=igraph.Graph();
    Shakeri_1d=Shakeri_1d.as_directed()
    Shakeri_1d.add_vertices(9);
    Shakeri_1d.add_edges([(0,1),(1,2),(2,5),(1,3),(3,6),(3,6),(6,8),(1,4),(4,7),(7,8),(5,8),(3,2),(6,5),(3,4),(6,7)]);
    return Shakeri_1d


    


# This reads an table of edges and creates a directed graph. If you want undirected,
# choose directed False
# Note that the vertices are still labeled by numbers
# To get which label corresponds to which vertex,
# use vs = igraph.VertexSeq(Dummy_Social_Network)
# for i in vs:
#    print(i)

#igraph.read("smallgraph.edgelist", format="ncol", directed=False, names=True)
#dummy_weighted = igraph.Graph.Read_Ncol("Graphs/dummy_weighted_2", directed=False)

# To use, in your console running the main script, incude
# from ExampleGraphs import House
# Now there is a graph House stored, and you can call the main(None,House,p,s,t,eps)

# import igraph.remote
# import igraph.remote.nexus
# UNABLE TO EXECUTE VARIANTS ON THIS STEP
# karate = igraph.remote.nexus.get("karate")
