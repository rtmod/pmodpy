
import igraph
import numpy
import cvxpy


def get_minimum(graph, subfamily, dens=None):
    if dens is None:
        dens = [float(1)] * graph.ecount()
    min_wt = float("inf")
    for mem in subfamily:
        wt = sum([dens[x] for x in mem])
        if wt < min_wt:
            min_wt = wt
            min_mem = mem
    z = [int(i in min_mem) for i in range(graph.ecount())]
    return numpy.asarray(z)


def modulus_subfamily(p, graph, subfamily, eps=2e-36, verbose=0):
    # Warning: For high values of 'p' the following error may obtain:
    # "ZeroDivisionError('Fraction(%s, 0)' % numerator)"
    #
    # Creates a |E(G)|-by-1 cvxpy matrix variable type
    edge_count = graph.ecount()
    x = cvxpy.Variable(edge_count)
    # Note: This is the p-norm,
    # not the sum of p^th powers as in the original papers
    obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
    z = get_minimum(graph, subfamily)
    dens = numpy.zeros(edge_count)
    constraint_list = [x >= 0, 1 <= z * x]
    # Define the appropriate stopping criterion
    # if p == 'inf':
    #    def stop_criterion(internal_z, internal_dens):
    #        numpy.dot(internal_z, internal_dens) >= 1
    # else:
    #    def stop_criterion(internal_z, internal_dens):
    #        (numpy.dot(internal_z, internal_dens)) ** p >= 1 - eps
    #
    while (numpy.dot(z, dens) ** p < 1 - eps):
        prob = cvxpy.Problem(obj, constraint_list)
        y = prob.solve()
        # A previous line of code produced errors:
        # "x = Variable(graph.ecount())"
        dens = x.value
        # Possible bug in cvxpy allows negative 'dens' entries;
        # here we overwrite them
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z = get_minimum(graph, subfamily, dens)
        constraint_list.append(1 <= z * x)
    #
    Edge_List = graph.get_edgelist()
    Density = numpy.asarray(dens)
    #
    if verbose != 0:
        print("Edge", "Density")
        for i in range(edge_count):
            print(Edge_List[i], Density[i])
        print(p, "-modulus is approximately", y ** p)
        print("Theoretical error = ", eps)
    #
    return([y ** p, Density])


# Albin & Poggi-Corradini (2016), Equation (2.9)
# unweighted graphs
def modulus_subfamily_dual(p, graph, subfamily):
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
    g = prob.solve()
    mu = lam.value / sum(lam.value)
    return([g, mu])

def modulus_subfamily_full(p, graph, subfamily, eps=2e-24):
    '''rho is the extremal density, mu is the optimal probability mass function.'''
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
        Gamma = numpy.r_[Gamma, z]
        constraint_list.append(1 <= z * x)
    #
    # modulus and extremal density
    mod1 = y ** p
    rho = numpy.asarray(dens)
    #
    # preliminary calculations
    n_objects = Gamma.shape[0]
    # CVX variables
    lam = cvxpy.Variable(n_objects)
    constraint_list = [lam >= 0]
    # CVX optimization problem
    obj = cvxpy.Maximize(
        cvxpy.sum(lam) - (p - 1) * cvxpy.sum(
            cvxpy.power(
                numpy.transpose(Gamma) * lam / p,
                p / (p - 1)
            )
        )
    )
    prob = cvxpy.Problem(obj, constraint_list)
    # modulus and optimal probability mass function
    mod2 = prob.solve()
    mu = numpy.asarray(lam.value / sum(lam.value))
    diff=abs(mod1-mod2)
    if diff > 2e-8:
        print("Warning: The modulus computed via different methods differ by more than 2e-8")
    
    return([mod1, mod2, rho, mu])
