import igraph, numpy, cvxpy
#Given a graph g, the function shortest returns a matrix
#counting the edge ids of edges visited in a shortest path from s to t
def shortest(dens,g,s,t): 
#Uses http://igraph.org/python/ get_shortest_paths. See website for details.
    x=g.get_shortest_paths(s,t,dens,"OUT","epath");
#Creates a vector of length |Edge Set of g| of all zeros    
    z=numpy.zeros(g.ecount());
#For loop is simply to create a counter for each edge visited. 
    for i in x:
        z[i]+=1;
    return numpy.asmatrix(z)



#Given a graph G, if you have an approximate density
#substitute it for dens
#Otherwise type None
#p is for the computation of p-modulus
#s is the input node
#t is the output node
#eps is the theoretical error given in Modulus of Families of Walks on Graphs

def main(dens,g,p,s,t,eps,verbose=0):
    #For high values of p there is an error:
    #  raise ZeroDivisionError('Fraction(%s, 0)' % numerator)
#Creates a cvxpy variable type of length |Edge set of G|
    number_of_edges=g.ecount()
    
    x= cvxpy.Variable(number_of_edges)
    
#The is the objective function to be minimized 
    obj = cvxpy.Minimize(cvxpy.power(cvxpy.pnorm(x,p),p))
    z=shortest(None,g,s,t)
    dens=numpy.zeros(g.ecount())
    list_of_constraints=[x>=0, 1 <= z*x]
    while((numpy.dot(z,dens))**p < 1-eps):
        prob = cvxpy.Problem(obj, list_of_constraints)
        y=prob.solve()
        #This line was here before, and it did not work:
        #x= Variable(g.ecount())
        dens=x.value
        if numpy.any(dens < 0):
            dens = numpy.maximum(dens, numpy.zeros(dens.shape))
        z=shortest(dens,g,s,t)
        list_of_constraints.append(1 <= z*x)
    Edge_List=g.get_edgelist()
    Density=numpy.asarray(dens)
    if verbose==0:
        return([y,Density])
    else:
        print("Edge", " Density Value ")
        for i in range(number_of_edges):
            print(Edge_List[i],Density[i])
        print(p,"- modulus is approximately", y)
        print("Theoretical error = ", eps)
        return([y,Density])

def modulus_walks(p, graph, source, target, eps = 2e-36, verbose = 0):
	# Warning: For high values of 'p' the following error may obtain:
	# "ZeroDivisionError('Fraction(%s, 0)' % numerator)"
	# 
	# Creates a |E(G)|-by-1 cvxpy matrix variable type
	edge_count = graph.ecount()
	x = cvxpy.Variable(edge_count)
	# Note: This is the p-norm,
	# not the sum of p^th powers as in the original papers
	obj = cvxpy.Minimize(cvxpy.pnorm(x, p))
	z = shortest(None, graph, source, target)
	dens = numpy.zeros(graph.ecount())
	constraint_list = [x >= 0, 1 <= z * x]
	# Define the appropriate stopping criterion
	#if p == 'inf':
	#	def stop_criterion(internal_z, internal_dens):
	#		numpy.dot(internal_z, internal_dens) >= 1
	#else:
	#	def stop_criterion(internal_z, internal_dens):
	#		(numpy.dot(internal_z, internal_dens)) ** p >= 1 - eps
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
		z = shortest(dens, graph, source, target)
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

def modulus_walks_inf(graph, source, target, eps = 2e-36, verbose = 0):
	# Warning: For high values of 'p' the following error may obtain:
	# "ZeroDivisionError('Fraction(%s, 0)' % numerator)"
	# 
	# Creates a |E(G)|-by-1 cvxpy matrix variable type
	edge_count = graph.ecount()
	x = cvxpy.Variable(edge_count)
	# Note: This is the p-norm,
	# not the sum of p^th powers as in the original papers
	obj = cvxpy.Minimize(cvxpy.pnorm(x, 'inf'))
	z = shortest(None, graph, source, target)
	dens = numpy.zeros(graph.ecount())
	constraint_list = [x >= 0, 1 <= z * x]
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
		z = shortest(dens, graph, source, target)
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

