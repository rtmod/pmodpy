# Graph modulus in Python

This repo contains a work-in-progress Python module for approximating the modulus for graphs introduced by Albin, Poggi-Corradini, and their colleagues.


## Dependencies

Our code relies on the following modules:

- `numpy` for ...
- `python-igraph` for constructing and manipulating mathematical graphs
- `cvxpy` for solving convex optimization problems

See the file `installation-notes.txt` for more detail.


## Organization

It is structured as a python module and can be installed on a shell as follows:
```python
pip3 install ./pmodpy/
```

The main functions can be called as follows:
```python
from pmodpy import modsubfamily
from pmodpy import modspans
from pmodpy import modwalks
```

If you would like to use the example graphs, include the following line:
```python
from pmodpy.examplegraphs import examplegraphs
```

Then, one of the examples can be called as follow:
```python
House=examplegraphs.House()
```
where House is the name of one of the example graphs.

If you want to compute the 2-modulus of walks from node 0 to node 1 on
House graph with verbose option, then we do:
```python
modwalks.modulus_walks_density(House, 0, 1, p=2, eps=2e-36, verbose=0)
```

``` python
##This graph is giving a different modulus as reported from the Shakeri paper.
Shakeri_1d =examplegraphs.Shakeri_1d()
```

## Testing uses py.test


## Acknowledgments

This is a limited adaptation of methods developed by the [NODE Group at Kansas State University](https://node.math.ksu.edu/). Original work is licensed under the GNU Public License version 2.
