"""
Implementation for the modulus function for families of spanning subgraphs.
"""

import numpy
import cvxpy
import igraph

def minimum_span_usage(graph, dens=None):
    """
    Given a graph, return a *numpy* array of dimension |E(G)| indicating
    the usage of each edge by a minimum spanning subgraph.

    Uses `spanning_tree` from *python-igraph*:
    http://igraph.org/python/
    (Minimum spanning subgraphs are necessarily minimum spanning trees.)

    Parameters:
    `graph`  -- *igraph* object
    `dens`   -- array of edge weights, defaults to `None`

    Note: Weighted graphs are not supported yet.
    """
    # Find a minimum spanning tree
    st = graph.spanning_tree(weights=dens, return_tree=False)
    # Create a zero array of length |E(G)|
    z = numpy.zeros(graph.ecount())
    # Indicate each edge visited
    for i in st:
        z[i] += 1
    # Return as a *numpy* array
    return numpy.asarray(z)

def modulus_spans_density(graph, p=2,
                          subfamily=False,
                          eps=1e-8, solver=cvxpy.CVXOPT, verbose=False):
    """
    Compute the span modulus of a graph.

    Parameters:
    `graph`     -- *igraph* object
    `p`         -- modulus parameter, defaults to `2`
    `subfamily` -- whether to return the (attempted) minimal subfamily
    `eps`       -- theoretical error, defaults to `2e-36`
    `solver`    -- solver to use in `prob.solve()`, defaults to `CVXOPT`
    `verbose`   -- whether to print status messages, defaults to `False`

    Note: Weighted graphs are not supported yet.
    """
    #
    # Store the edge count and edge list
    edge_count = graph.ecount()
    edge_list = graph.get_edgelist()
    # Create a |E(G)|-by-1 *cvxpy* matrix variable type
    x = cvxpy.Variable(edge_count)
    #
    # Calculate the p-norm of the edge count matrix
    # Note: This is not the sum of p^th powers as in the original papers
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    # Store a minimum span under the given edge weights
    z = minimum_span_usage(graph)
    # Initialize the extremal density estimate
    dens = numpy.zeros(edge_count)
    # Initialize the minimal subfamily
    if subfamily:
        Gamma = numpy.empty((edge_count, 0))
    # Initialize the constraints for the optimization problem
    constraint_list = [x >= 0, 1 <= z @ x]
    #
    # Define the continuation criterion for the optimization loop
    if p in [numpy.inf, 'inf', 'Inf']:
        def continue_criterion(z_, dens_):
            return(numpy.dot(z, dens) < 1 - eps)
    else:
        def continue_criterion(z_, dens_):
            return((numpy.dot(z_, dens_)) ** p < 1 - eps)
    # Iterate until the extremal length estimate is within `eps` of 1
    while continue_criterion(z, dens):
        # Augment the minimal subfamily
        if subfamily:
            Gamma = numpy.c_[Gamma, z]
        # Set up the optimization problem
        prob = cvxpy.Problem(obj, constraint_list)
        # Solve the optimization problem
        sol = prob.solve(solver, verbose)
        # Update the extremal density estimate
        dens = x.value
        # Overwrite negative density estimates to zero
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        # Calculate a minimum span under the new extremal density estimate
        z = minimum_span_usage(graph, dens=dens)
        # Augment the constraints
        constraint_list.append(1 <= z @ x)
    #
    # Note: Right now, we are getting a scaled density vector,
    # since we are multiplying \rho_i by w_i^(1/p),
    # where w_i is the ith coordinate of the weight vector.
    # It makes no difference if the graph is unweighted.
    #
    # Store the final modulus and extremal density estimates
    if p in [numpy.inf, 'inf', 'Inf']:
        Mod = sol
    else:
        Mod = sol ** p
    rho = numpy.asarray(dens)
    # Print the extremal density by edge nodes
    if verbose:
        print("Edge", "Density")
        for i in range(edge_count):
            print(edge_list[i], rho[i])
        print(p, "-modulus is approximately ", Mod)
        print("Theoretical error = ", eps)
    # Return the modulus estimate and the extremal density estimate
    if subfamily:
        return([Mod, rho, Gamma])
    else:
        return([Mod, rho])

def modulus_spans(graph, p=2,
                  subfamily=False,
                  eps=1e-8, solver=cvxpy.CVXOPT, verbose=False):
    #
    # Compute the modulus, extremal density, and minimal subfamily
    res = modulus_spans_density(graph, p=p, subfamily=True,
                                eps=eps, solver=solver, verbose=verbose)
    Mod = res[0]
    rho = res[1]
    Gamma = res[2]
    #
    # Estimate the modulus with the optimal probability mass function
    n_objects = Gamma.shape[1]
    lam = cvxpy.Variable(n_objects)
    # Define the appropriate objective function
    if p == 1:
        constraint_list = [Gamma * lam <= 1, lam >= 0]
        obj = cvxpy.Maximize(cvxpy.sum(lam))
    elif p in [numpy.inf, 'inf', 'Inf']:
        eta = cvxpy.Variable(Gamma.shape[0])
        constraint_list = [Gamma @ lam <= eta, cvxpy.sum(eta) == 1, lam >= 0]
        obj = cvxpy.Maximize(cvxpy.sum(lam))
    else:
        constraint_list = [lam >= 0]
        obj = cvxpy.Maximize(
            cvxpy.sum(lam) - (p - 1) * cvxpy.sum(
                cvxpy.power(
                    Gamma @ lam / p,
                    p / (p - 1)
                )
            )
        )
    #
    # Set up the optimization problem
    prob = cvxpy.Problem(obj, constraint_list)
    # Solve the optimization problem
    Mod_pmf = prob.solve(solver, verbose)
    # Calculate the optimal pmf estimate
    mu = numpy.asarray(lam.value / sum(lam.value))
    #
    # Check that the modulus estimates concord
    diff = abs(Mod - Mod_pmf)
    if diff > eps:
        print("Warning: The modulus estimates differ by more than `eps`.")
    # Return the modulus, extremal density, and optimal pmf estimates
    if subfamily:
        return([Mod, Mod_pmf, rho, mu, Gamma])
    else:
        return([Mod, Mod_pmf, rho, mu])

def moduli_spans(graph, p=[1, 2, 'inf'],
                 eps=1e-8, solver=cvxpy.CVXOPT):
    return([
        modulus_spans_density(graph, p=q, eps=eps, solver=solver)[0]
        for q in p
    ])
