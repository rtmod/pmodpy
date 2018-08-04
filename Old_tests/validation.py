execfile("main.py")
execfile("ExampleGraphs.py")

# walks

# Validate toy example
# https://arxiv.org/abs/1401.7640
# p. 4
main(None, Kite, 2, 0, 1, 10e-12)

# Validate house example
# https://arxiv.org/abs/1401.7640
# p. 5-7
main(None, House, 1, 0, 1, 10e-12)
main(None, House, 2, 0, 1, 10e-12)

modulus_walks_inf(House, 0, 1, 10e-12)

modulus_walks(1, House, 0, 1, 10e-12, verbose = 1)
modulus_walks(2, House, 0, 1, 10e-12, verbose = 1)
modulus_walks('inf', House, 0, 1, 10e-12, verbose = 1)

# Validate illustrative example
# http://www.ams.org/journals/ecgd/2015-19-13/S1088-4173-2015-00287-8/
# p. 299
main(None, Contacts, 1, 0, 1, 10e-12)
main(None, Contacts, 1, 1, 3, 10e-12)
main(None, Contacts, 1, 3, 20, 10e-12)
main(None, Contacts, 2, 0, 1, 10e-12)
main(None, Contacts, 2, 1, 3, 10e-12)
main(None, Contacts, 2, 3, 20, 10e-12)
main(None, Contacts, "inf", 0, 1, 10e-12)
main(None, Contacts, "inf", 1, 3, 10e-12)
main(None, Contacts, "inf", 3, 20, 10e-12)

modulus_walks(2, Contacts, 3, 20, eps = 10e-12)

# routers example
# https://link.springer.com/article/10.1007/s41478-016-0002-9
modulus_walks(1, Routers, 0, 14, 10e-12)
modulus_walks(2, Routers, 0, 14, 10e-12)
modulus_walks_inf(Routers, 0, 14, 10e-12)

# read in a comorbidity graph
medicare3 = igraph.Graph.Read_Ncol("../data/medicare1993-3.txt", directed = False)
main(None, medicare3, 1, 0, 1, 10e-12)
main(None, medicare3, 2, 0, 1, 10e-12)

# spanning trees

# toy example
# https://arxiv.org/abs/1401.7640
modulus_trees(1, Kite, 10e-12)
modulus_trees(2, Kite, 10e-12)
modulus_trees_inf(Kite, 10e-12)

# house example
# https://arxiv.org/abs/1401.7640
modulus_trees(1, House, 10e-12)
modulus_trees(2, House, 10e-12)
modulus_trees_inf(House, 10e-12)

# illustrative contacts example
# http://www.ams.org/journals/ecgd/2015-19-13/S1088-4173-2015-00287-8/
modulus_trees(1, Contacts, 10e-12)
modulus_trees(2, Contacts, 10e-12)
modulus_trees_inf(Contacts, 10e-12)

# routers example
# https://link.springer.com/article/10.1007/s41478-016-0002-9
modulus_trees(1, Routers, 10e-12)
modulus_trees(2, Routers, 10e-12)
modulus_trees_inf(Routers, 10e-12)
