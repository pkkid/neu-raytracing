#!/usr/bin/python2.4
"""
Various callback functions for coloring objects
Created by M.Shepanski
"""

import pygame


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
    OFFSET = (10000, 10000)
    
    def __init__(self, color1, color2, sqSize, resolution):
        self.resolution = resolution   # Texture Width & Height (for mapping)
        self._color1  = color1         # First color in Checkerboard
        self._color2  = color2         # Second color in Checkerboard
        self._sqSize  = sqSize         # Half width (for math)
        
    def getColor(self, pos):
        """ Return the color. """
        # We add 10,000 to avoid seeing duplicate colors at the origin.
        if (((((pos[0] + CheckerBoard.OFFSET[0]) % (self._sqSize*2)) < self._sqSize and
              ((pos[1] + CheckerBoard.OFFSET[1]) % (self._sqSize*2)) < self._sqSize)) or
            ((((pos[0] + CheckerBoard.OFFSET[0]) % (self._sqSize*2)) >= self._sqSize and
              ((pos[1] + CheckerBoard.OFFSET[1]) % (self._sqSize*2)) >= self._sqSize))):
            return self._color1
        return self._color2
    
    
###############################
#  Image Texture
###############################

class Image(Texture):
    """ Image. """
    
    def __init__(self, imagePath, scale=1.0):
        self._image = pygame.image.load(imagePath)        # Image to Map this texture to
        self.scale  = scale                               # Amount to scale the image
        self.resolution = (self._image.get_width(), self._image.get_height())
        
    def getColor(self, pos):
        """ Return the color. """
        xPos = pos[0] % (self.resolution[0] * (1 / self.scale))
        yPos = pos[1] % (self.resolution[1] * (1 / self.scale))
        return self._image.get_at((xPos, yPos))
    
    
########################
#  Testing
########################
if (__name__ == "__main__"):
    myChecker = CheckerBoard((0,0,0), (1,1,1), 50, (100, 100))
    print myChecker.getColor((1,10))
    print myChecker.getColor((51,10))
    print myChecker.getColor((101,10))
    print myChecker.getColor((151,10))
    print myChecker.getColor((201,10))
    
