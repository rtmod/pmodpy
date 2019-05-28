"""
Implementation for the modulus function for families of walks.
"""

import numpy
import cvxpy
import igraph


def shortest(graph, source, target, dens=None):
    """
    Given a graph, return a *numpy* array of dimension |E(G)| indicating
    whether each edge is visited in a shortest path from source to target.

    Uses `get_shortest_paths` from *python-igraph*:
    http://igraph.org/python/

    Parameters:
    graph  -- *igraph* object
    source -- source node of `graph`
    target -- target node of `graph`
    dens   -- array of edge weights, defaults to `None`

    Note: Weighted graphs are not supported yet.

    """
    # Find a shortest path
    sp = graph.get_shortest_paths(source, to=target, weights=dens,
                                  mode="OUT", output="epath")
    # Create a zero array of length |E(G)|
    z = numpy.zeros(graph.ecount())
    # Indicate each edge visited
    for i in sp:
        z[i] += 1
    # Return as a *numpy* array
    return numpy.asarray(z)


def modulus_walks_density(graph, source, target, p=2,
                          eps=1e-8, solver=cvxpy.CVXOPT, verbose=False):
    """
    Compute the modulus of the family of walks in a graph
    from a source node to a target node.

    Parameters:
    p       -- modulus parameter, defaults to 2
    graph   -- *igraph* object
    source  -- source node of `graph`
    target  -- target node of `graph`
    eps     -- theoretical error, defaults to 2e-36
    solver  -- solver to use in `prob.solve()`
    verbose -- whether to print status messages, defaults to `False`

    Note: Weighted graphs are not supported yet.

    Warning: For high values of `p`, the following error may obtain:
    `ZeroDivisionError('Fraction(%s, 0)' % numerator)`

    """
    #if graph.is_weighted():
        #weight_vector=graph.es["weight"];
    #else:
        #weight_vector=numpy.ones(graph.ecount());

    #scaled_weight_vector=numpy.power(weight_vector,1/p)

    # Store the edge count and edge list
    edge_count = graph.ecount()
    edge_list = graph.get_edgelist()
    # Create a |E(G)|-by-1 *cvxpy* matrix variable type
    x = cvxpy.Variable(edge_count)

    # Calculate the p-norm of the edge count matrix
    # Note: This is not the sum of p^th powers as in the original papers
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    # Store the shortest path under the given edge weights
    z = shortest(graph=graph, source=source, target=target, dens=None)
    # Initialize the extremal density estimate
    dens = numpy.zeros(edge_count)
    # Initialize the constraints for the optimization problem
    constraint_list = [x >= 0, 1 <= z * x]
    # Define the appropriate stopping criterion
    # if p == 'inf':x
    # def stop_criterion(internal_z, internal_dens):
    # numpy.dot(internal_z, internal_dens) >= 1
    # else:
    # def stop_criterion(internal_z, internal_dens):
    # (numpy.dot(internal_z, internal_dens)) ** p >= 1 - eps
    # While the extremal length estimate is not within the error tolerance of 1
    while (numpy.dot(z, dens) ** p < 1 - eps):
        # Set up the optimization problem
        prob = cvxpy.Problem(obj, constraint_list)
        # Solve the optimization problem
        y = prob.solve(solver, verbose)
        # Update the extremal density estimate
        dens = x.value
        # Overwrite negative density estimates to zero
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        # Calculate the shortest path under the new extremal density estimate
        z = shortest(graph=graph, source=source, target=target, dens=dens)
        # Augment the constraints
        constraint_list.append(1 <= z * x)

    # Note: Right now, we are getting a scaled density vector,
    # since we are multiplying \rho_i by w_i^(1/p),
    # where w_i is the ith coordinate of the weight vector.
    # It makes no difference if the graph is unweighted.

    # Store the final extremal density estimate
    rho = numpy.asarray(dens)
    # Print the extremal density by edge nodes
    if verbose:
        print("Edge", "Density")
        for i in range(edge_count):
            print(edge_list[i], rho[i])
        print(p, "-modulus is approximately ", y ** p)
        print("Theoretical error = ", eps)
    # Return the modulus estimate and the extremal density estimate
    return([y ** p, rho])


def modulus_walks_density_inf(graph, source, target,
                              eps=1e-8, solver=cvxpy.CVXOPT, verbose=0):
    # Warning: For high values of `p` the following error may obtain:
    # `ZeroDivisionError('Fraction(%s, 0)' % numerator)`

    # Store the edge count and edge list
    edge_count = graph.ecount()
    edge_list = graph.get_edgelist()
    # Create a |E(G)|-by-1 *cvxpy* matrix variable type
    x = cvxpy.Variable(edge_count)

    # Calculate the infinity norm of the edge count matrix
    obj = cvxpy.Minimize(cvxpy.pnorm(x, 'inf'))
    # Store the shortest path under the given edge weights
    z = shortest(graph=graph, source=source, target=target, dens=None)
    # Initialize the extremal density estimate
    dens = numpy.zeros(edge_count)
    # Initialize the constraints for the optimization problem
    constraint_list = [x >= 0, 1 <= z * x]
    # While the extremal length estimate is not within the error tolerance of 1
    # Note: A relationship between the tolerance `eps` and the accuracy of `y`
    # has not been proved in the published literature.
    # TEST THE RELATIONSHIP BETWEEN `eps` AND THE ACCURACY OF `y`
    while (numpy.dot(z, dens) < 1 - eps):
        # Set up the optimization problem
        prob = cvxpy.Problem(obj, constraint_list)
        # Solve the optimization problem
        y = prob.solve(solver, verbose)
        # Update the extremal density estimate
        dens = x.value
        # Overwrite negative density estimates to zero
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        # Calculate the shortest path under the new extremal density estimate
        z = shortest(graph=graph, source=source, target=target, dens=dens)
        # Augment the constraints
        constraint_list.append(1 <= z * x)

    # Store the final extremal density estimate
    rho = numpy.asarray(dens)
    # Print the extremal density by edge nodes
    if verbose != 0:
        print("Edge", "Density")
        for i in range(edge_count):
            print(edge_list[i], rho[i])
        print("Infinity-modulus is approximately ", y)
        print("Theoretical error = ", eps)
    # Return the modulus estimate and the extremal density estimate
    return([y, rho])


def modulus_walks_full(graph, source, target, p=2,
                       eps=1e-8, solver=cvxpy.CVXOPT, verbose=False):
    """
    1. Computes the modulus and extremal density using @Albin2014 Algorithm 1,
        collecting a minimal subfamily in the process.
    2. Computes the modulus and optimal pmf using @Albin2016a Equation 2.9,
        based on the minimal subfamily.
    3. Verifies that the modulus calculations agree.
    4. Returns the modulus, extremal density, and optimal pmf.
    """

    # Estimate the modulus with the extremal density
    # while accumulating a minimal subfamily
    edge_count = graph.ecount()
    x = cvxpy.Variable(edge_count)
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    dens = numpy.zeros(edge_count)
    z = shortest(graph=graph, source=source, target=target, dens=None)
    Gamma = z
    constraint_list = [x >= 0, 1 <= z * x]
    while (numpy.dot(z, dens) ** p < 1 - eps):
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve(solver, verbose)
        dens = x.value
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = shortest(graph=graph, source=source, target=target, dens=dens)
        Gamma = numpy.c_[Gamma, z]
        constraint_list.append(1 <= z * x)
    mod1 = y ** p
    rho = numpy.asarray(dens)

    # Estimate the modulus with the optimal probability mass function
    # using the minimal subfamily
    n_objects = Gamma.shape[1]
    lam = cvxpy.Variable(n_objects)
    constraint_list = [lam >= 0]
    obj = cvxpy.Maximize(
        cvxpy.sum(lam) - (p - 1) * cvxpy.sum(
            cvxpy.power(
                Gamma * lam / p,
                p / (p - 1)
            )
        )
    )
    prob = cvxpy.Problem(obj, constraint_list)
    mod2 = prob.solve(solver, verbose)
    mu = numpy.asarray(lam.value / sum(lam.value))

    # Check that the modulus estimates concord
    diff = abs(mod1-mod2)
    if diff > 1e-7:
        print("Warning: The modulus estimates differ by more than 1e-7")

    return([mod1, mod2, rho, mu, Gamma])
