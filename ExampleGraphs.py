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

Kite=igraph.Graph()
Kite.add_vertices(4)
Kite.add_edges([(0,2),(0,3),(1,3),(2,3)])

House=igraph.Graph()
House.add_vertices(5)
House.add_edges([(0,1),(0,4),(4,1),(0,3),(3,2),(2,1)])

Contacts=igraph.Graph()
Contacts.add_vertices(21)
Contacts.add_edges([
	(0,1),
	(1,2),(1,3),(1,4),(2,3),(4,3),
	(2,5),(3,5),(5,6),(6,7),(7,8),(8,9),
	(3,10),(10,11),(11,12),(12,13),(13,14),
	(3,15),(4,15),(15,16),(16,17),(17,18),(18,19),
	(9,20),(14,20),(19,20)
	])

#To use, in your console running the main script, incude
#from ExampleGraphs import House
#Now there is a graph House stored, and you can call the main(None,House,p,s,t,eps)

import igraph.remote
import igraph.remote.nexus
# UNABLE TO EXECUTE VARIANTS ON THIS STEP
karate = igraph.remote.nexus.get("karate")
