"""
Implementation for the modulus function for a general family of objects.
"""

import numpy
import cvxpy
import igraph


def get_minimum(graph, subfamily, dens=None):
    """
    Given a graph and a family of objects (subgraphs),
    return a *numpy* array of dimension |E(G)| indicating
    whether each edge is a member of a minimum element of the family.

    Parameters:
    graph     -- *igraph* object
    subfamily -- family of objects in (subgraphs of) `graph`
    dens      -- array of edge weights, defaults to `None`

    Note: Weighted graphs are not supported yet.

    """
    # Unit density if weights not provided
    if dens is None:
        dens = [float(1)] * graph.ecount()
    # Initialize minimum weight
    min_wt = float("inf")
    # Iterate over members of the family
    for mem in subfamily:
        # Calculate the weight of the member
        wt = sum([dens[x] for x in mem])
        # If the weight is less than the current minimum weight, update
        if wt < min_wt:
            min_wt = wt
            min_mem = mem
    # Encode the mimimum object by whether each edge is involved
    z = [int(i in min_mem) for i in range(graph.ecount())]
    # Return as a *numpy* array
    return numpy.asarray(z)


<<<<<<< HEAD
def modulus_subfamily_density(graph, subfamily, p=2, eps=2e-36, solver=cvxpy.CVXOPT, verbose=False):
    """
    Compute the modulus of a family of objects of a graph.

    Parameters:
    graph     -- *igraph* object
    subfamily -- family of objects in (subgraphs of) `graph`
    p         -- modulus parameter, defaults to 2
    eps       -- theoretical error, defaults to 2e-36
    solver    -- solver to use in `prob.solve()`
    verbose   -- whether to print status messages, defaults to `False`

    Note: Weighted graphs are not supported yet.

    Warning: For high values of `p` the following error may obtain:
    `ZeroDivisionError('Fraction(%s, 0)' % numerator)`
=======
def modulus_subfamily_density(graph, subfamily, p=2, eps=2e-36,
                                  verbose=False, solver=cvxpy.CVXOPT):
    """ Modulus subfamily
>>>>>>> bc4f436e431f1546f80861748918ee955d18a1b1

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
    # Store the minimum family member under the given edge weights
    z = get_minimum(graph, subfamily)
    # Initialize the extremal density estimate
    dens = numpy.zeros(edge_count)
    # Initialize the constraints for the optimization problem
    constraint_list = [x >= 0, 1 <= z * x]
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
        # Calculate the minimum family member under the new density estimate
        z = get_minimum(graph, subfamily, dens)
        # Augment the constraints
        constraint_list.append(1 <= z * x)
    #
    # Store the final extremal density estimate
    rho = numpy.asarray(dens)
    # Print the extremal density by edge nodes
    if verbose:
        print("Edge", "Density")
        for i in range(edge_count):
            print(edge_list[i], rho[i])
        print(p, "-modulus is approximately", y ** p)
        print("Theoretical error = ", eps)
    # Return the modulus estimate and the extremal density estimate
    return([y ** p, rho])


# @Albin2016a, Equation 2.9
# unweighted graphs
def modulus_subfamily_mass(graph, subfamily, p=2, solver=cvxpy.CVXOPT, verbose=False):
    # preliminary calculations
    n_objects = len(subfamily)
    usage = numpy.asmatrix(
        [[int(i in j) for i in range(graph.ecount())] for j in subfamily]
    )
    # CVX variables
    lam = cvxpy.Variable(n_objects)
    constraint_list = [lam >= 0]
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
    # p-modulus and optimal probability mass function
    mod = prob.solve(solver, verbose)
    mu = lam.value / sum(lam.value)
    return([mod, mu])

<<<<<<< HEAD
def modulus_subfamily_full(graph, subfamily, p=2, eps=2e-24, solver=cvxpy.CVXOPT, verbose=False):
=======
def modulus_subfamily_full(graph, subfamily, p=2, eps=2e-24, verbose=False,
                               solver=cvxpy.CVXOPT):
    '''rho is the extremal density, mu is the optimal probability mass 
function.'''
>>>>>>> bc4f436e431f1546f80861748918ee955d18a1b1
    # preliminary calculations
    edge_count = graph.ecount()
    dens = numpy.zeros(edge_count)
    # CVX variables
    x = cvxpy.Variable(edge_count)
    constraint_list = [x >= 0]
    # CVX optimization problem
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    # find minimum configuration for uniform density
    z = get_minimum(graph, subfamily)
    Gamma = z
    constraint_list.append(1 <= z * x)
    # iteratively append lengths of members of Gamma to constraints
    while (numpy.dot(z, dens) ** p < 1 - eps):
        # iteration of optimization process
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve()
        dens = x.value
        # overwrite negative values
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = get_minimum(graph, subfamily, dens)
        Gamma = numpy.c_[Gamma, z]
        constraint_list.append(1 <= z * x)
    #
    # modulus and extremal density
    mod1 = y ** p
    rho = numpy.asarray(dens)
    #
    # preliminary calculations
    n_objects = Gamma.shape[1]
    # CVX variables
    lam = cvxpy.Variable(n_objects)
    constraint_list = [lam >= 0]
    # CVX optimization problem
    obj = cvxpy.Maximize(
        cvxpy.sum(lam) - (p - 1) * cvxpy.sum(
            cvxpy.power(
                Gamma * lam / p,
                p / (p - 1)
            )
        )
    )
    prob = cvxpy.Problem(obj, constraint_list)
    # modulus and optimal probability mass function
    mod2 = prob.solve(solver, verbose)
    mu = numpy.asarray(lam.value / sum(lam.value))
    #
    # concordance between modulus calculations
    diff = abs(mod1-mod2)
    if diff > 1e-7:
        print("Warning: The modulus computed via different methods differ by more than 1e-7")
    #
    return([mod1, mod2, rho, mu])
