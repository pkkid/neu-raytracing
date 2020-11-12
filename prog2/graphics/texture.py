#!/usr/bin/python2.4
"""
Various callback functions for coloring objects
Created by M.Shepanski
"""


###############################
#  Texture Base Class
###############################

class Texture:
    """ Base Class for all Textures. """
    
    def getColor(self, vec):
        """ Return the color at the specified vector. """
        raise Exception("Function not defined: getColor()")
    

###############################
#  Checkerboard Texture
###############################

class CheckerBoard(Texture):
    """ Checkerboard Color. """

    def __init__(self, color1, color2, width=50, offset=(10000, 10000)):
        self.color1 = color1        # First color in Checkerboard
        self.color2 = color2        # Second color in Checkerboard
        self.width  = width * 2     # Width of the squares
        self.half   = width         # Half width (for math)
        self.offset = offset        # X,Y Offset

    def getColor(self, vec):
        """ Return the color. """
        # We add 10,000 to avoid seeing duplicate colors at the origin.
        if (((((vec.x + self.offset[0]) % self.width) < self.half and
              ((vec.y + self.offset[1]) % self.width) < self.half)) or
            ((((vec.x + self.offset[0]) % self.width) >= self.half and
              ((vec.y + self.offset[1]) % self.width) >= self.half))):
            return self.color1
        return self.color2


class CheckerBoardZ(Texture):
    """ Checkerboard Color. """

    def __init__(self, color1, color2, width=50, offset=(10000, 10000)):
        self.color1 = color1        # First color in Checkerboard
        self.color2 = color2        # Second color in Checkerboard
        self.width  = width * 2     # Width of the squares
        self.half   = width         # Half width (for math)
        self.offset = offset        # X,Y Offset

    def getColor(self, vec):
        """ Return the color. """
        # We add 10,000 to avoid seeing duplicate colors at the origin.
        if (((((vec.x + self.offset[0]) % self.width) < self.half and
              ((vec.z + self.offset[1]) % self.width) < self.half)) or
            ((((vec.x + self.offset[0]) % self.width) >= self.half and
              ((vec.z + self.offset[1]) % self.width) >= self.half))):
            return self.color1
        return self.color2
