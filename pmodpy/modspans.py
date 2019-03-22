import numpy
import cvxpy
import igraph


def spantree(dens, g):
    # Get a minimal spanning tree 'st'
    st = g.spanning_tree(weights=dens, return_tree=False)
    # Return an edge vector of indicators for membership in 'st'
    z = numpy.zeros(g.ecount())
    for i in st:
        z[i] += 1
    return numpy.asarray(z)


def modulus_spans_density(graph, p=2, eps=2e-36, verbose=0):
    if p == "inf":
        modulus_trees_inf(graph, eps=2e-36, verbose=0)
    else:
        # Creates a |E(G)|-by-1 cvxpy matrix variable type
        edge_count = graph.ecount()
        x = cvxpy.Variable(edge_count)
        # Note: This is the p-norm
        # not the sum of p^th powers as in the original paper
        obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
        z = spantree(None, graph)
        dens = numpy.zeros(graph.ecount())
        constraint_list = [x >= 0, 1 <= z * x]
        while (numpy.dot(z, dens) ** p < 1 - eps):
            prob = cvxpy.Problem(obj, constraint_list)
            y = prob.solve()
            dens = x.value
            # cvxpy allows negative 'dens' entries;
            # here we overwrite them
            if numpy.any(dens < 0):
                dens = numpy.maximum(dens, numpy.zeros(dens.shape))
                z = spantree(dens, graph)
                constraint_list.append(1 <= z * x)
        Edge_List = graph.get_edgelist()
        Density = numpy.asarray(dens)
    #
        if verbose != 0:
            print("Edge", "Density")
            for i in range(edge_count):
                print(Edge_List[i], Density[i])
                print(p, "-modulus is approximately", y ** p)
                print("Theoretical error = ", eps)
        return([y ** p, Density])


def modulus_spans_density_inf(graph, eps=2e-36, verbose=0):
    # Creates a |E(G)|-by-1 cvxpy matrix variable type
    edge_count = graph.ecount()
    x = cvxpy.Variable(edge_count)
    # Note: This is the p-norm,
    # not the sum of p^th powers as in the original papers
    obj = cvxpy.Minimize(cvxpy.pnorm(x, 'inf'))
    z = spantree(None, graph)
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
        # Possible bug in cvxpy allows negative 'dens' entries;
        # here we overwrite them
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = spantree(dens, graph)
        constraint_list.append(1 <= z * x)
    #
    Edge_List = graph.get_edgelist()
    Density = numpy.asarray(dens)
    #
    if verbose != 0:
        print("Edge", "Density")
        for i in range(edge_count):
            print(Edge_List[i], Density[i])
        print(p, "-modulus is approximately", y)
        print("Theoretical error = ", eps)
    #
    return([y, Density])
