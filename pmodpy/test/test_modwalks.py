"""
Testing file for walk modulus
Uses py.test
To run testing unit, go to root of project and run on shell:
py.test
"""

from pmodpy import modwalks
from pmodpy.examplegraphs import examplegraphs


def test_modulus_walks_density_kite_2():
    kite = examplegraphs.Kite()
    kite_mod = modwalks.modulus_walks_density(kite, 0, 1, p=2)
    assert kite_mod[0] - 0.6 < 1e-5
    assert max(abs(kite_mod[1] - [i / 5 for i in [1, 2, 3, 1]])) < 1e-5


def test_modulus_walks_full_kite():
    kite = examplegraphs.Kite()
    kite_mod = modwalks.modulus_walks_full(kite, 0, 1, p=2)
    assert kite_mod[0] - 0.6 < 1e-5
    assert kite_mod[1] - 0.6 < 1e-5
    assert max(abs(kite_mod[2] - [i / 5 for i in [1, 2, 3, 1]])) < 1e-5


def test_modulus_walks_density_house():
    house = examplegraphs.House()
    house_mod = modwalks.modulus_walks_density(house, 0, 1, p=2)
    assert abs(house_mod[0] - 1.833333) < 1e-5;


def test_modulus_walks_full_routers():
    routers = examplegraphs.Routers()
    mod_report = 0.741024
    rho_mod_report = [
        0.296, 0.408, 0.295,
        0.144, 0.176, 0.232, 0.152, 0.142, 0.153,
        0.144, 0.139, 0.154, 0.060, 0.142, 0.132, 0.173,
        0.320, 0.125, 0.014, 0.214, 0.173,
        0.445, 0.555
    ]
    routers_mod = modwalks.modulus_walks_full(routers, 0, 14, p=2)
    assert abs(routers_mod[0] - mod_report) < 1e-5
    assert abs(routers_mod[1] - mod_report) < 1e-5
    assert max(abs(routers_mod[2] / routers_mod[0] - rho_mod_report)) < 1e-5


def test_modulus_walks_density_shakeri1a():
    shakeri1a = examplegraphs.Shakeri_1a()
    shakeri1a_mod = modwalks.modulus_walks_density(shakeri1a, 0, 8, p=2)
    assert abs(shakeri1a_mod[0] - 0.4) < 1e-5


def test_modulus_walks_density_shakeri1b():
    shakeri1b = examplegraphs.Shakeri_1b()
    shakeri1b_mod = modwalks.modulus_walks_density(shakeri1b, 0, 8, p=2)
    assert abs(shakeri1b_mod[0] - 0.5) < 1e-5


def test_modulus_walks_density_shakeri1d():
    shakeri1d = examplegraphs.Shakeri_1d()
    shakeri1d_mod = modwalks.modulus_walks_density(shakeri1d, 0, 8, p=2)
    assert abs(shakeri1d_mod[0] - 0.5169) < 1e-5
