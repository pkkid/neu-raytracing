#!/usr/bin/python2.4
"""
Represents a single color.
Created by M.Shepanski
"""

import random


def blend(color1, color2):
    """ Return a new color of the two colors blended together. """
    r = int(color1[0] + color2[0])
    g = int(color1[1] + color2[1])
    b = int(color1[2] + color2[2])
    return (r, g, b)
    

def toHex(color):
    """ Return the color in hex. """
    hexstr = "#"
    for channel in [color[0], color[1], color[2]]:
        if (channel <= 15): hexstr += "0%s" % hex(channel)[2:]
        else: hexstr += hex(channel)[2:]
    return hexstr


def darken(color, percent):
    """ Darken this color to the specified percent. 
        @param percent:  Float in the range 0-1.
    """
    r = int(color[0] * percent)
    g = int(color[1] * percent)
    b = int(color[2] * percent)
    return (r, g, b)


def randomColor():
    """ Return a random color. """
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)
    return (r, g, b)

