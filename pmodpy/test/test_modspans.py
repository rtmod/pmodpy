"""
Testing file for span modulus
Uses py.test
To run testing unit, go to root of project and run on shell:
py.test
"""

from pmodpy import modspans
from pmodpy.examplegraphs import examplegraphs


def test_modulus_spans_full_routers():
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
    assert abs(routers_mod[1] - mod_report) < 1e-5
    assert max(abs(routers_mod[2] / routers_mod[0] - rho_mod_report)) < 1e-5
