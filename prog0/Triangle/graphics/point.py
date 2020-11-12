#!/usr/bin/python2.4
"""
Helpful Point functions.
Created by M.Shepanski
"""

import random


def randomPoint(maxX, maxY):
    """ Return a random point with a random color. """
    x = random.randrange(maxX)
    y = random.randrange(maxY)
    return (x, y)

