
from igraph import *

def expand_graph(g,picture=1):
#Che
    if not g.is_directed():
                return ("Make sure your graph is directed ")
    graph=g.copy()
   
        
    for i in range(1,len(graph.es())+1):
        
        
        x=graph.es.select(syngroup_eq=i)
        #This is a logical step to make sure the user does not have
        #edges in the same synergy group with distinct target
        #nodes
        
        if len(x)==0:
            break
        else:
            check=set()
            for edge in x:
                check.add(edge.target)
            if len(check)>1:
                 
                 return("Please check no nodes in the same synergy group have distinct targets")
                 
            
        
            target=x[0].target
            graph.add_vertex(label="c"+str(i),composite=True,color="Blue")
            comp=graph.vs.select(label_eq="c"+str(i))
            
            
#Look at this part.
            for j in x:
                graph.add_edge(j.source,comp[0])
#Look at this part.

            graph.delete_edges(x)
            graph.add_edge(comp[0],target)
    if picture==1:
        plot(graph)
                
    return graph




            
    
            
         
            
    
    
