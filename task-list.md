## Issues and tasks for implementations of the $p$-modulus on graphs

Convert these notes to HTML using Pandoc:
```sh
pandoc cory-notes.md -o cory-notes.html
```

### Python implementation

Functionality:

* Characterize the step function from `eps` to accuracy
* Test case $p=\infty$ for relationship between tolerance `eps` and accuracy of `y`

Issues:

* Construct a minimal reproducible example of the `cvxpy` bug that produces negative `dens` entries

Extensions:

* Weighted graphs
* Figure out how to get more examples through `igraph.remote.nexus`
* Get a signal transduction network example
* Implement graph-reading functions to facilitate use of new examples
* Other families of edges (e.g. [minimal spanning trees](http://igraph.org/python/doc/igraph.Graph-class.html))
* Validate on larger and denser graphs (e.g. Medicare)

### R implementation

First get convex optimization working in R.

R packages for convex optimization:

- [CVXfromR](http://faculty.bscb.cornell.edu/~bien/cvxfromr.html)
- [cvxr](https://github.com/anqif/cvxr)
