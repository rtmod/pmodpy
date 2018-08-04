#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 14:54:41 2017

@author: luissordovieira
Kite graph 
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

