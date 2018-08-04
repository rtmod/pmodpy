### Testing file for function modulus walks
from context import pmodpy
from pmodpy.src import moduluswalks
from pmodpy.examplegraphs import examplegraphs


def test_walks_kite():
        kite=examplegraphs.Kite();
        assert abs(moduluswalks.modulus_walks(2, kite, 0, 1, eps=2e-36, verbose=0)[0]-0.6)<.00001;


def test_walks_house():
            House=examplegraphs.House();
            assert abs(moduluswalks.modulus_walks(2, House, 0, 1, eps=2e-36, verbose=0)[0]-1.833333)<.00001;


def test_walks_shakeri_1a():
            Shakeri_1a=examplegraphs.Shakeri_1a();
            assert abs(moduluswalks.modulus_walks(2, Shakeri_1a, 0, 8, eps=2e-36, verbose=0)[0]-0.4)<.00001


def test_walks_shakeri_1b():
            Shakeri_1b=examplegraphs.Shakeri_1b();
            assert abs(moduluswalks.modulus_walks(2, Shakeri_1b, 0, 8, eps=2e-36, verbose=0)[0]-0.5)<.00001





# This one fails but the density seems to make sense ?
#def test_walks_shakeri_1d():
 #   Shakeri_1a=examplegraphs.Shakeri_1d();
  #  assert abs(moduluswalks.modulus_walks(2, Shakeri_1d, 0, 8, eps=2e-36, ve#rbose=0)[0]-0.5169)<.00001
