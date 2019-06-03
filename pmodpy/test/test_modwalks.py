"""
Testing file for walk modulus
Uses *pytest*
To run testing unit, go to root of project and run on shell:
```sh
py.test
```
"""

from pmodpy import modwalks
from pmodpy.examplegraphs import examplegraphs

def test_modulus_walks_kite():
    kite = examplegraphs.Kite()
    kite_mod = modwalks.modulus_walks_density(kite, 0, 1, p=2)
    assert kite_mod[0] - 0.6 < 1e-4
    assert max(abs(kite_mod[1] - [i/5 for i in [1, 2, 3, 1]])) < 1e-4
    kite_mod = modwalks.modulus_walks(kite, 0, 1, p=2)
    assert kite_mod[0] - 0.6 < 1e-4
    assert kite_mod[1] - 0.6 < 1e-4
    assert max(abs(kite_mod[2] - [i/5 for i in [1, 2, 3, 1]])) < 1e-4

def test_modulus_walks_density_house():
    house = examplegraphs.House()
    house_mod = modwalks.modulus_walks_density(house, 0, 1, p=2)
    assert abs(house_mod[0] - 1.833333) < 1e-4;

def test_modulus_walks_routers():
    routers = examplegraphs.Routers()
    mod_report = 0.741024
    rho_mod_report = [
        0.296, 0.408, 0.295,
        0.144, 0.152,  0.176, 0.232, 0.142, 0.153,
        0.144, 0.139, 0.154, 0.06, 0.142, 0.132, 0.173,
        0.32, 0.125, 0.014, 0.214, 0.173,
        0.445, 0.555
    ]
    routers_mod = modwalks.modulus_walks(routers, 0, 14, p=2,eps=1e-15)
    assert abs(routers_mod[0] - mod_report) < 1e-6
    assert abs(routers_mod[1] - mod_report) < 1e-6
    assert max(abs(routers_mod[2] / routers_mod[0] - rho_mod_report)) < 1e-3

def test_modulus_walks_density_connecting_a():
    connecting_a = examplegraphs.Connecting_a()
    connecting_a_mod = modwalks.modulus_walks_density(connecting_a, 0, 8, p=2)
    assert abs(connecting_a_mod[0] - 0.4) < 1e-4

def test_modulus_walks_density_connecting_b():
    connecting_b = examplegraphs.Connecting_b()
    connecting_b_mod = modwalks.modulus_walks_density(connecting_b, 0, 8, p=2)
    assert abs(connecting_b_mod[0] - 0.5) < 1e-4

def test_modulus_walks_density_connecting_c():
    connecting_c = examplegraphs.Connecting_c()
    connecting_c_mod = modwalks.modulus_walks_density(connecting_c, 0, 8, p=2)
    assert abs(connecting_c_mod[0] - 0.5161) < 1e-4

def test_modulus_walks_density_connecting_d():
    connecting_d = examplegraphs.Connecting_d()
    connecting_d_mod = modwalks.modulus_walks_density(connecting_d, 0, 8, p=2)
    assert abs(connecting_d_mod[0] - 0.5169) < 1e-4

from pmodpy import powers

def test_moduli_walks_kite():
    kite = examplegraphs.Kite()
    p = powers.power_sequence(n = 5)
    kite_mods = modwalks.moduli_walks(kite, 0, 1, p)
