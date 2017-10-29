## Issues and tasks for implementations of the $p$-modulus on graphs

Convert these notes to HTML using Pandoc:
```sh
pandoc cory-notes.md -o cory-notes.html
```

### Python implementation

Functionality:

* Characterize the step function from `eps` to accuracy
* Test case $p=\infty$ for relationship between tolerance `eps` and
accuracy of `y`
* Implement MFR algorithm.
* Implement Probabilistic interpretation of Modulus.


Issues:

Extensions:

* Weighted graphs
* Figure out how to get more examples through `igraph.remote.nexus`
  (remote nexus is not working, the link simply does not work)
* Get a signal transduction network example
* Implement graph-reading functions to facilitate use of new examples
(Done 10/24/2017)
* Other families of edges (e.g. [minimal spanning trees](http://igraph.org/python/doc/igraph.Graph-class.html))
* Validate on larger and denser graphs (e.g. Medicare)

### R implementation

First get convex optimization working in R.

R packages for convex optimization:

- [CVXfromR](http://faculty.bscb.cornell.edu/~bien/cvxfromr.html)
- [cvxr](https://github.com/anqif/cvxr)
