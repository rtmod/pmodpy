"""
Testing file for span modulus
Uses *pytest*
To run testing unit, go to root of project and run on shell:
```sh
py.test
```
"""

import numpy
from pmodpy import modspans
from pmodpy.examplegraphs import examplegraphs

def test_modulus_spans_paw():
    paw = examplegraphs.Paw()
    paw_mod = modspans.modulus_spans_density(paw, p=2)
    assert paw_mod[0] - 3/7 < 1e-5
    assert max(abs(paw_mod[1] - [i/7 for i in [3, 2, 2, 2]])) < 1e-5
    paw_mod = modspans.modulus_spans(paw, p=2, subfamily=True)
    assert paw_mod[4].shape == (4, 3)
    assert numpy.count_nonzero(paw_mod[4], axis=0).tolist() == [3, 3, 3]
    assert numpy.count_nonzero(paw_mod[4], axis=1).tolist() == [3, 2, 2, 2]

def test_modulus_spans_density_routers():
    routers = examplegraphs.Routers()
    mod_report = 0.11734
    rho_mod_report = [
        0.611, 0.611, 0.611,
        0.611, 0.611, 0.611, 0.611, 0.611, 0.611,
        0.611, 0.600, 0.600, 0.600, 0.611, 0.611, 0.611,
        0.611, 0.611, 0.600, 0.600, 0.611,
        0.611, 0.611
    ]
    routers_mod = modspans.modulus_spans_density(routers, p=2)
    assert abs(routers_mod[0] - mod_report) < 1e-5
    assert max(abs(routers_mod[1] / routers_mod[0] - rho_mod_report)) < 1e-3
    routers_mod = modspans.modulus_spans(routers, p=2, subfamily=True)
    assert len(routers_mod[4]) == 22

from pmodpy import powers

def test_moduli_spans_kite():
    kite = examplegraphs.Kite()
    p = powers.power_sequence(n = 5)
    kite_mods = modspans.moduli_spans(kite, p)
