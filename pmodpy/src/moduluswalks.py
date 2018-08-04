
# Given a graph g, the function shortest returns a matrix
# counting the edge ids of edges visited in a shortest path from s to t

import igraph
import numpy
import cvxpy


def shortest(dens, g, s, t):
    # Uses http://igraph.org/python/ get_shortest_paths.
    # See website for details.
    x = g.get_shortest_paths(s, t, dens, "OUT", "epath")
# Creates a vector of length |Edge Set of g| of all zeros
    z = numpy.zeros(g.ecount())
# For loop is simply to create a counter for each edge visited.
    for i in x:
        z[i] += 1
    return numpy.asmatrix(z)


# Given a graph G, if you have an approximate density
# substitute it for dens
# Otherwise type None
# p is for the computation of p-modulus
# s is the input node
# t is the output node
# eps is the theoretical error given in Modulus of Families of Walks on Graphs

def modulus_walks(p, graph, source, target, eps=2e-36, verbose=0):
    # Warning: For high values of 'p' the following error may obtain:
    # "ZeroDivisionError('Fraction(%s, 0)' % numerator)"
    # Creates a |E(G)|-by-1 cvxpy matrix variable typ
    edge_count = graph.ecount()

    if graph.is_weighted():
        weight_vector=graph.es["weight"];
        print("weighted")
    else:
        weight_vector=numpy.ones(graph.ecount());
        
    
    scaled_weight_vector=numpy.power(weight_vector,1/p)
    
    x = cvxpy.Variable(edge_count)


    # Note: This is the p-norm,
    # not the sum of p^th powers as in the original papers
    obj = cvxpy.Minimize(cvxpy.pnorm(scaled_weight_vector*x, p))
    z = shortest(None, graph, source, target)
    dens = numpy.zeros(graph.ecount())
    constraint_list = [x >= 0, 1 <= z * x]
    # Define the appropriate stopping criterion
    # if p == 'inf':
    # def stop_criterion(internal_z, internal_dens):
    # numpy.dot(internal_z, internal_dens) >= 1
    # else:
    # def stop_criterion(internal_z, internal_dens):
    # (numpy.dot(internal_z, internal_dens)) ** p >= 1 - eps
    while (numpy.dot(z, dens) ** p < 1 - eps):
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve()
        # A previous line of code produced errors:
        # "x = Variable(graph.ecount())"
        dens = x.value
        # cvxpy allows negative 'dens' entries
        # here we overwrite them
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = shortest(dens, graph, source, target)
        constraint_list.append(1 <= z * x)
    Edge_List = graph.get_edgelist()

    ##Notice that right now, we are getting a scaled density vector since we are multiplying \rho_i by w_i^(1/p) where w_i is the ith coordinate of the weight vector. It makes no difference if the graph is unweighted.
    
    Density = numpy.asarray(dens)
    Density =Density/scaled_weight_vector;
    if verbose != 0:
        print("Edge", "Density")
        for i in range(edge_count):
            print(Edge_List[i], Density[i])
        print(p, "-modulus is approximately", y ** p)
        print("Theoretical error = ", eps)
    return([y ** p, Density])


def modulus_walks_inf(graph, source, target, eps=2e-36, verbose=0):
    # Warning: For high values of 'p' the following error may obtain:
    # "ZeroDivisionError('Fraction(%s, 0)' % numerator)"
    # Creates a |E(G)|-by-1 cvxpy matrix variable type
    edge_count = graph.ecount()
    x = cvxpy.Variable(edge_count)
    # Note: This is the p-norm,
    # not the sum of p^th powers as in the original papers
    obj = cvxpy.Minimize(cvxpy.pnorm(x, 'inf'))
    z = shortest(None, graph, source, target)
    dens = numpy.zeros(graph.ecount())
    constraint_list = [x >= 0, 1 <= z * x]
    # Note: A relationship between the tolerance 'eps' and the accuracy of 'y'
    # has not been proved in the published literature.
    # TEST THE RELATIONSHIP BETWEEN 'eps' AND THE ACCURACY OF 'y'
    while (numpy.dot(z, dens) < 1 - eps):
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve()
        # A previous line of code produced errors:
        # "x = Variable(graph.ecount())"
        dens = x.value
        # Due to inherent machine precision erros, some very small components
        # might have negative signs
        # here we overwrite them
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = shortest(dens, graph, source, target)
        constraint_list.append(1 <= z * x)
    Edge_List = graph.get_edgelist()
    Density = numpy.asarray(dens)
    if verbose != 0:
        print("Edge", "Density")
        for i in range(edge_count):
            print(Edge_List[i], Density[i])
    print(p, "-modulus is approximately", y)
    print("Theoretical error = ", eps)
    return([y, Density])
