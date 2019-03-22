
import igraph
import numpy
import cvxpy


def shortest(graph, source, target, dens=None):
    """
    Given a graph g, the function shortest returns a numpyt array
    counting the edge ids of edges visited in a shortest path from s to t.

    Uses http://igraph.org/python/ get_shortest_paths.

    Key Variables
    graph --igraph object.
    s -- Source node.
    t-- Target node.
    dens -- Weights of edges as an edge list. NOT IMPLEMENTED YET. (default=None)

    """
    x = graph.get_shortest_paths(source, to=target, weights=dens, mode="OUT", output="epath")
## Creates a vector of length |Edge Set of g| of all zeros
    z = numpy.zeros(graph.ecount())
## For loop is simply to create a counter for each edge visited.
    for i in x:
        z[i] += 1
    return numpy.asarray(z)



def modulus_walks_density(graph, source, target, p=2, eps=2e-36, verbose=False, solver=cvxpy.CVXOPT):
    """
    Computes the modulus of the family of walks from  source node to target node.

    Key variables:
    p -- Value of p-modulus for the p-modulus function. Default = 2.
    graph -- igraph object
    source -- source node id
    target -- Target node id
    eps -- theoretical error given in Modulus of Families of Walks on GraphsY (default= 2e-36)
    verbose -- How much information to print to console. Default =False
    solver-- Which solver to use for CVXOPT

    Note: Weighted graphs are not supported yet.

    Warning: For high values of 'p' the following error may obtain:

    "ZeroDivisionError('Fraction(%s, 0)' % numerator)"

    """
    # Creates a |E(G)|-by-1 cvxpy matrix variable typ
    edge_count = graph.ecount()

    #if graph.is_weighted():
        #weight_vector=graph.es["weight"];
    #else:
        #weight_vector=numpy.ones(graph.ecount());


    #scaled_weight_vector=numpy.power(weight_vector,1/p)

    x = cvxpy.Variable(edge_count)


    # Note: This is the p-norm,
    # not the sum of p^th powers as in the original papers
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    #Later, dens can be substituted with an approximate density, or a weight.
    z = shortest(dens=None, graph=graph, source=source, target=target)
    dens = numpy.zeros(graph.ecount())
    constraint_list = [x >= 0, 1 <= z * x]
    # Define the appropriate stopping criterion
    # if p == 'inf':x
    # def stop_criterion(internal_z, internal_dens):
    # numpy.dot(internal_z, internal_dens) >= 1
    # else:
    # def stop_criterion(internal_z, internal_dens):
    # (numpy.dot(internal_z, internal_dens)) ** p >= 1 - eps
    while (numpy.dot(z, dens) ** p < 1 - eps):
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve(solver,verbose)
        # A previous line of code produced errors:
        # "x = Variable(graph.ecount())"
        dens = x.value
        # cvxpy allows negative 'dens' entries
        # here we overwrite them
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = shortest(dens=dens, graph=graph, source=source, target=target)
        constraint_list.append(1 <= z * x)
    Edge_List = graph.get_edgelist()

    ##Notice that right now, we are getting a scaled density vector since we are multiplying \rho_i by w_i^(1/p) where w_i is the ith coordinate of the weight vector. It makes no difference if the graph is unweighted.

    Density = numpy.asarray(dens)
    if verbose:
        print("Edge", "Density")
        for i in range(edge_count):
            print(Edge_List[i], Density[i])
        print(p,"modulus is approximately", y ** p)
        print("Theoretical error = ", eps)
    return([y ** p, Density,Edge_List])


def modulus_walks_density_inf(graph, source, target, eps=2e-36, verbose=0):
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
    print(p,"modulus is approximately", y)
    print("Theoretical error = ", eps)
    return([y, Density])
