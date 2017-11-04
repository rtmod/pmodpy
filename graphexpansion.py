



from igraph import *

def expand_graph(g):
    graph=g.copy()
    for i in range(1,len(graph.es())+1):
        x=graph.es.select(syngroup_eq=i)
        
        if len(x)==0:
            break
        else:
            target=x[0].target
            graph.add_vertex(label="c"+str(i))
            comp=graph.vs.select(label_eq="c"+str(i))
            
#Look at this part.
            for j in x:
                graph.add_edge(j.source,comp[0])
#Look at this part.

            graph.delete_edges(x)
            graph.add_edge(comp[0],target)
    return graph






from igraph import *

def expand_graph(g):
    graph=g.copy()
    for i in range(1,len(graph.es())+1):
        x=graph.es.select(syngroup_eq=i)
        
        if len(x)==0:
            return "Did you forget the synergy list?"
        else:
            target=x[0].target
            graph.add_vertex(label="c"+str(i))
            comp=graph.vs.select(label_eq="c"+str(i))
            for j in x:
                graph.add_edge(j.source,comp[0])

            graph.delete_edges(x)
            graph.add_edge(comp[0],target)
    return graph


            
    
            
         
            
    
    
