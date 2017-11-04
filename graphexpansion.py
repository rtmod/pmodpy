



from igraph import *

def expand_graph(graph):
    for i in range(1,len(graph.es())+1):
        x=graph.es.select(syngroup_eq=i)
        
        if len(x)==0:
            break
        else:
            target=x[0].target
            graph=graph.add_vertex(name="c"+str(i))
            comp=g.vs.select(name_eq="c"+str(i))
#Look at this part.
            for j in x:
                graph=graph.add_edge(j.source,comp)
#Look at this part.

            graph=graph.delete_edges(x)
            graph=graph.add_edge(comp,target)
    return graph
#Look at this
#Logical checks





            
    
            
         
            
    
    
