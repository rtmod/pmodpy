"""
Generate sequences and samples from [0, inf] via log-stereographic projection.
"""

import math
import random

def map_stereograph(x):
    return(2 ** (math.tan((math.pi / 2) * x)))

def power_sequence(n=3):
    powers = [
        round(map_stereograph(i / (n - 1)), 14)
        for i in range(n - 1)
    ]
    powers.append(float('inf'))
    return(powers)

def power_sample(n=1):
    powers = [
        round(map_stereograph(random.random()), 14)
        for i in range(n)
    ]
    return(powers)
