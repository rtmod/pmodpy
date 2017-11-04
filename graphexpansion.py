



from igraph import *

def expand_graph(graph):
    for i in range(1,len(graph.es())+1):
        x=graph.es.select(syngroup_eq=i)
        
        if len(x)==0:
            break
        else:
            target=x[0].target
            comp=graph.add_vertex(name="c"+str(i))
            for j in x:
                graph.add_edge(j.source,comp)
            graph.delete_edges(x)
            graph.add_edge(comp,target)
    return graph
            
            
    
            
         
            
    
    
