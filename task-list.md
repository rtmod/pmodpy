## Issues and tasks for implementations of the $p$-modulus on graphs

Convert these notes to HTML using Pandoc:
```sh
pandoc cory-notes.md -o cory-notes.html
```

### Python implementation

Functionality:

* Implement special case $p=\infty$ using [the `'inf'` option in `cvxpy.pnorm`](http://www.cvxpy.org/en/latest/tutorial/functions/pnorm.html)
* Figure out why the functions terminate with `eps = 0` (but only about `10e-10` precision)
* Validate on larger and denser graphs (e.g. Medicare)

Extensions:

* Weighted graphs
* Other families of edges (e.g. [minimal spanning trees](http://igraph.org/python/doc/igraph.Graph-class.html))

### R implementation

First get convex optimization working in R.

R packages for convex optimization:

- [CVXfromR](http://faculty.bscb.cornell.edu/~bien/cvxfromr.html)
- [cvxr](https://github.com/anqif/cvxr)
