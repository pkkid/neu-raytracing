#!/usr/bin/python2.4
"""
Represents a single color.
Created by M.Shepanski
"""

import random

# Solid Colors
BLACK   = (0,   0,   0)
RED     = (255, 0,   0)
ORANGE  = (255, 128, 0)
YELLOW  = (255, 255, 0)
GREEN   = (0,   255, 0)
CYAN    = (0,   255, 255)
BLUE    = (0,   0,   255)
MAGENTA = (255, 0,   255)
PINK    = (255, 0,   128)
WHITE   = (255, 255, 255)

# Off Colors - Named from Chir.ag
# http://chir.ag/projects/name-that-color/
DESERT        = (190, 66, 28)
SARATOGA      = (81, 107, 20)
TEAK          = (237, 205, 154)
THUNDER       = (45, 42, 47)
ORANGE_ROUGHY = (196, 87, 25)


def add(color1, color2):
    """ Return a new color of the two colors blended together.
        @param color1:  (r,g,b) First Color object to add. 
        @param color2:  (r,g,b) Second Color object to add. 
    """
    r = min(int(color1[0] + color2[0]), 255)
    g = min(int(color1[1] + color2[1]), 255)
    b = min(int(color1[2] + color2[2]), 255)
    return (r, g, b)


def mul(color, num):
    """ Darken this color to the specified percent.
        @param color:    (r,g,b) Color object to multiply.
        @param num:      Float multiplier
    """
    num = max(num, 0)
    r = min(int(color[0] * num), 255)
    g = min(int(color[1] * num), 255)
    b = min(int(color[2] * num), 255)
    return (r, g, b)


def toHex(color):
    """ Return the color in hex.
        @param color:   (r,g,b) Color object to return Hex value for.
    """
    hexstr = "#"
    for channel in [color[0], color[1], color[2]]:
        if (channel <= 15): hexstr += "0%s" % hex(channel)[2:]
        else: hexstr += hex(channel)[2:]
    return hexstr


def randomColor():
    """ Return a random Color object. """
    r = random.randrange(256)
    g = random.randrange(256)
    b = random.randrange(256)
    return (r, g, b)

