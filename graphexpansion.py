
from igraph import *

def expand_graph(graph):
    for i in range(1,len(g.es())+1):
        x=g.es.select("syn_group"==i)
        
        if len(x)==0:
            break
        else:
            target=x[0].target
            comp=graph.add_vertex("comp")
            for j in x:
                graph.add_edge(j.source,comp)
                
            graph.add_edge(comp,target)
            graph.delete_edges(x)
    return graph
            
            
    
            
         
            
    
    
