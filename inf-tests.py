execfile("main.py")
execfile("ExampleGraphs.py")

modulus_walks_inf(House, 0, 1, 10e-2, verbose = 0)[0]
modulus_walks_inf(House, 0, 1, 10e-3, verbose = 0)[0]
modulus_walks_inf(House, 0, 1, 10e-6, verbose = 0)[0]
modulus_walks_inf(House, 0, 1, 10e-10, verbose = 0)[0]
modulus_walks_inf(House, 0, 1, 10e-15, verbose = 0)[0]
modulus_walks_inf(House, 0, 1, 10e-21, verbose = 0)[0]

modulus_walks_inf(Contacts, 3, 20, 10e-2, verbose = 0)[0]
modulus_walks_inf(Contacts, 3, 20, 10e-3, verbose = 0)[0]
modulus_walks_inf(Contacts, 3, 20, 10e-6, verbose = 0)[0]
modulus_walks_inf(Contacts, 3, 20, 10e-10, verbose = 0)[0]
modulus_walks_inf(Contacts, 3, 20, 10e-15, verbose = 0)[0]
modulus_walks_inf(Contacts, 3, 20, 10e-21, verbose = 0)[0]
