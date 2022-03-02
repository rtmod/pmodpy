"""
Implementation for the modulus function for families of spanning subgraphs.
"""

import numpy
import cvxpy
import igraph


def spantree(graph, dens):
    """
    Given a graph, return a *numpy* array of dimension |E(G)| indicating
    whether each edge is visited in a minimal spanning tree.

    Uses `spanning_tree` from *python-igraph*:
    http://igraph.org/python/

    Parameters:
    graph  -- *igraph* object
    dens   -- array of edge weights, defaults to `None`

    Note: Weighted graphs are not supported yet.

    """
    # Find a minimal spanning tree
    st = graph.spanning_tree(weights=dens, return_tree=False)
    # Create a zero array of length |E(G)|
    z = numpy.zeros(graph.ecount())
    # Indicate each edge visited
    for i in st:
        z[i] += 1
    # Return as a *numpy* array
    return numpy.asarray(z)


def modulus_spans_density(graph, p=2,
                          eps=1e-8, solver=cvxpy.CVXOPT, verbose=0):
    edge_count = graph.ecount()
    edge_list = graph.get_edgelist()
    x = cvxpy.Variable(edge_count)
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    z = spantree(graph=graph, dens=None)
    dens = numpy.zeros(edge_count)
    constraint_list = [x >= 0, 1 <= z @ x]
    if p == 'inf':
        exp = 1
    else:
        exp = p
    while (numpy.dot(z, dens) ** exp < 1 - eps):
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve(solver, verbose)
        dens = x.value
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = spantree(graph=graph, dens=dens)
        constraint_list.append(1 <= z @ x)
    rho = numpy.asarray(dens)
    if verbose != 0:
        print("Edge", "Density")
        for i in range(edge_count):
            print(edge_list[i], rho[i])
            print(p, "-modulus is approximately ", y ** exp)
            print("Theoretical error = ", eps)
    return([y ** p, rho])


def modulus_spans_full(graph, p=2,
                       eps=1e-8, solver=cvxpy.CVXOPT, verbose=False):
    edge_count = graph.ecount()
    x = cvxpy.Variable(edge_count)
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    dens = numpy.zeros(edge_count)
    z = spantree(graph=graph, dens=None)
    Gamma = z
    constraint_list = [x >= 0, 1 <= z @ x]
    while (numpy.dot(z, dens) ** p < 1 - eps):
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve(solver, verbose)
        dens = x.value
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = spantree(graph=graph, dens=dens)
        Gamma = numpy.c_[Gamma, z]
        constraint_list.append(1 <= z @ x)
    mod1 = y ** p
    rho = numpy.asarray(dens)

    n_objects = Gamma.shape[1]
    lam = cvxpy.Variable(n_objects)
    constraint_list = [lam >= 0]
    obj = cvxpy.Maximize(
        cvxpy.sum(lam) - (p - 1) * cvxpy.sum(
            cvxpy.power(
                Gamma @ lam / p,
                p / (p - 1)
            )
        )
    )
    prob = cvxpy.Problem(obj, constraint_list)
    mod2 = prob.solve(solver, verbose)
    mu = numpy.asarray(lam.value / sum(lam.value))

    diff = abs(mod1-mod2)
    if diff > 1e-7:
        print("Warning: The modulus estimates differ by more than 1e-7")

    return([mod1, mod2, rho, mu, Gamma])
