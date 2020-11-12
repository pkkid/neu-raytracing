#!/usr/bin/python2.4
"""
A Moving Triangle. :)
Created by M.Shepanski
"""

import color
from point import randomPoint
from triangle import Triangle


class ColorTriangle(Triangle):
    """ Extend Triangle to add color. """
    
    def __init__(self, p1, p2, p3):
        Triangle.__init__(self, p1, p2, p3)
        self.p1c = color.randomColor()
        self.p2c = color.randomColor()
        self.p3c = color.randomColor()
        
    def __str__(self):
        """ String representation for this triangle. """
        return "ColorTriangle(%s, %s, %s)" % (self.p1, self.p2, self.p3)
        
    def getColorAt(self, point):
        """ Return the color of the specified point. Returns None if the
            specified point is outside the triangle boundries.
        """
        alpha, beta, gamma = self.calcBarycentricCoordinates(point)
        # Point it outside the triangle; However, because if we assume we are already
        # are using triangle.iterPoints to iterate through all the points in the
        # triangle, we can safely set the negative values to 0, which has the side
        # effect of removing the clipping.
        if (alpha < 0):  alpha = 0.0
        if (beta < 0):   beta  = 0.0
        if (gamma < 0):  gamma = 0.0
        if (alpha > 1):  alpha = 1.0
        if (beta > 1):   beta  = 1.0
        if (gamma > 1):  gamma = 1.0
        #if (alpha < 0) or (beta < 0) or (gamma < 0):
        #    return None
        # Calculate the new blended color
        p1cBlend = color.darken(self.p1c, alpha)
        p2cBlend = color.darken(self.p2c, beta)
        p3cBlend = color.darken(self.p3c, gamma)
        return color.blend(color.blend(p1cBlend, p2cBlend), p3cBlend)
        
    @staticmethod
    def random(maxX, maxY):
        """ Generate a random triangle. """
        p1 = randomPoint(maxX, maxY)
        p2 = randomPoint(maxX, maxY)
        p3 = randomPoint(maxX, maxY)
        return ColorTriangle(p1, p2, p3)
        
        