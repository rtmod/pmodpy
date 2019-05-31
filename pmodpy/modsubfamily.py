"""
Implementation for the modulus function for any family of objects.
"""

import numpy
import cvxpy
import igraph

def minimum_object_usage(graph, family, dens=None):
    """
    Given a graph and a family of objects (subgraphs),
    return a *numpy* array of dimension |E(G)| indicating
    the usage of each edge by a minimum object.

    Parameters:
    `graph`     -- *igraph* object
    `family`    -- family of objects in (subgraphs of) `graph`
    `dens`      -- array of edge weights, defaults to `None`

    Note: Weighted graphs are not supported yet.
    """
    # Unit density if weights not provided
    if dens is None:
        dens = [float(1)] * graph.ecount()
    # Initialize minimum weight
    min_wt = float("inf")
    # Iterate over members of the family
    for mem in family:
        # Calculate the weight of the member
        wt = sum([dens[x] for x in mem])
        # If the weight is less than the current minimum weight, update
        if wt < min_wt:
            min_wt = wt
            min_mem = mem
    # Encode the mimimum object by whether each edge is used
    z = [int(i in min_mem) for i in range(graph.ecount())]
    # Return as a *numpy* array
    return numpy.asarray(z)

def modulus_family_density(graph, family, p=2,
                           subfamily=False,
                           eps=1e-8, solver=cvxpy.CVXOPT, verbose=False):
    """
    Compute the modulus of a family of objects of a graph.

    Parameters:
    `graph`     -- *igraph* object
    `family`    -- family of objects in `graph`, as lists of edge IDs
    `p`         -- modulus parameter, defaults to `2`
    `subfamily` -- whether to return the (attempted) minimal subfamily
    `eps`       -- theoretical error, defaults to `2e-36`
    `solver`    -- solver to use in `prob.solve()`, defaults to `CVXOPT`
    `verbose`   -- whether to print status messages, defaults to `False`

    Note: Weighted graphs are not supported yet.

    Warning: For high values of `p` the following error may obtain:
    `ZeroDivisionError('Fraction(%s, 0)' % numerator)`
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
    # Store a minimum object under the given edge weights
    z = minimum_object_usage(graph, family)
    # Initialize the extremal density estimate
    dens = numpy.zeros(edge_count)
    # Initialize the minimal subfamily
    if subfamily:
        Gamma = numpy.empty((edge_count, 0))
    # Initialize the constraints for the optimization problem
    constraint_list = [x >= 0, 1 <= z * x]
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
        # Calculate a minimum object under the new extremal density estimate
        z = minimum_object_usage(graph, family, dens)
        # Augment the constraints
        constraint_list.append(1 <= z * x)
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

def modulus_family_pmf(graph, family, p=2,
                       solver=cvxpy.CVXOPT, verbose=False):
    # preliminary calculations
    n_objects = len(family)
    usage = numpy.asmatrix(
        [[int(i in j) for i in range(graph.ecount())] for j in family]
    )
    # CVX variables
    lam = cvxpy.Variable(n_objects)
    constraint_list = [lam >= 0]
    # Throw errors if not `1 < p < 'inf'`
    if p == 1:
        raise ValueError("Optimal pmf modulus is not implemented for `p=1`.")
    elif p in [numpy.inf, 'inf', 'Inf']:
        raise ValueError("Optimal pmf modulus is not implemented for `p='inf'`.")
    # CVX optimization problem
    obj = cvxpy.Maximize(
        cvxpy.sum(lam) - (p - 1) * cvxpy.sum(
            cvxpy.power(
                numpy.transpose(usage) * lam / p,
                p / (p - 1)
            )
        )
    )
    prob = cvxpy.Problem(obj, constraint_list)
    # modulus and optimal probability mass function
    Mod = prob.solve(solver, verbose)
    mu = lam.value / sum(lam.value)
    return([Mod, mu])

def modulus_family(graph, family, p=2,
                   subfamily=False,
                   eps=2e-8, solver=cvxpy.CVXOPT, verbose=False):
    #
    # Compute the modulus, extremal density, and minimal subfamily
    res = modulus_walks_density(graph, source, target, p=p, subfamily=True,
                                eps=eps, solver=solver, verbose=verbose)
    Mod = res[0]
    rho = res[1]
    Gamma = res[2]
    #
    # Estimate the modulus with the optimal probability mass function
    n_objects = Gamma.shape[1]
    lam = cvxpy.Variable(n_objects)
    constraint_list = [lam >= 0]
    # Define the appropriate objective function
    if p == 1:
        print("Warning: Optimal pmf modulus is not implemented for `p=1`.")
        if subfamily:
            return([Mod, float('nan'), rho, numpy.asarray(float('nan')), Gamma])
        else:
            return([Mod, float('nan'), rho, numpy.asarray(float('nan'))])
    elif p in [numpy.inf, 'inf', 'Inf']:
        print("Warning: Optimal pmf modulus is not implemented for `p='inf'`.")
        if subfamily:
            return([Mod, float('nan'), rho, numpy.asarray(float('nan')), Gamma])
        else:
            return([Mod, float('nan'), rho, numpy.asarray(float('nan'))])
    else:
        obj = cvxpy.Maximize(
            cvxpy.sum(lam) - (p - 1) * cvxpy.sum(
                cvxpy.power(
                    Gamma * lam / p,
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
