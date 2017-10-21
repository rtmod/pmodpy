execfile("main.py")
execfile("ExampleGraphs.py")

modulus_walks(1, House, 0, 1, 10e-2, verbose = 0)[0]
modulus_walks(1, House, 0, 1, 10e-6, verbose = 0)[0]
modulus_walks(1, House, 0, 1, 10e-12, verbose = 0)[0]
modulus_walks(1, House, 0, 1, 10e-20, verbose = 0)[0]

modulus_walks(2, House, 0, 1, 10e-2, verbose = 0)[0]
modulus_walks(2, House, 0, 1, 10e-6, verbose = 0)[0]
modulus_walks(2, House, 0, 1, 10e-12, verbose = 0)[0]
modulus_walks(2, House, 0, 1, 10e-20, verbose = 0)[0]

modulus_walks(1, Contacts, 3, 20, 10e-2, verbose = 0)[0]
modulus_walks(1, Contacts, 3, 20, 10e-6, verbose = 0)[0]
modulus_walks(1, Contacts, 3, 20, 10e-12, verbose = 0)[0]
# NEED TO REPORT A BUG IN cvxpy HERE
modulus_walks(1, Contacts, 3, 20, 10e-20, verbose = 0)[0]

modulus_walks(2, Contacts, 3, 20, 10e-2, verbose = 0)[0]
modulus_walks(2, Contacts, 3, 20, 10e-6, verbose = 0)[0]
modulus_walks(2, Contacts, 3, 20, 10e-12, verbose = 0)[0]
modulus_walks(2, Contacts, 3, 20, 10e-20, verbose = 0)[0]
