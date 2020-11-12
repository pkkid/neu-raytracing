#!/usr/bin/python2.4
"""
Represents a Light Source.
Created by M.Shepanski
"""

class Light:
    """ Represents a Light Source. """    
    
    def __init__(self, center, color=(255, 255, 255)):
        self.center = center        # Center point of the sphere (vector)
        self.color = color          # Color of the sphere (color)
    
    def __str__(self):
        """ String representation for this vector. """
        return "Light(%s, %s)" % (self.center, self.color)
    
    