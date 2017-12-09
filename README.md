# graph $p$-modulus in Python

This repo contains a work-in-progress Python module for approximating the $p$-modulus for graphs introduced by Albin, Poggi-Corradini, and their colleagues.

## Dependencies

Our code relies on the following modules:

- `numpy` for ...
- `cvxpy` for ...
- `python-igraph` for constructing and manipulating mathematical graphs

See the file `installation-notes.txt` for more detail.

##

It is structured as a python package.

The main functions can be called as follows:

from pmodpy.src import modsubfamily
from pmodpy.src import modulustrees
from pmodpy.src import moduluswalks


If you would like to use the example graphs, include the following line:

from pmodpy.examplegraphs import examplegraphs

Then, one of the examples can be called as follow:

House=examplegraphs.House()

where House is the name of one of the example graphs.

If you want to compute the 2-modulus of walks from node 0 to node 1 on
House graph with verbose option, then we do:
moduluswalks.modulus_walks(2, House, 0, 1, eps=2e-36, verbose=0)



## Acknowledgments






This is a limited adaptation of methods developed by the [NODE Group at Kansas State University](https://node.math.ksu.edu/). Original work is licensed under the GNU Public License version 2.
