#!/usr/bin/python2.4
"""
Represents a Line.
Created by M.Shepanski
"""

class Line:
    """ Represents a vector point in 3D Space. """
    
    def __init__(self, p1, p2):
        """ Create a new vector from p1 -> p2. """
        self.p1 = p1
        self.p2 = p2
        
    def __str__(self):
        """ String representation for this line. """
        return "Line(%s, %s)" % (self.p1, self.p2)
        
    def iterPoints(self):
        """ Iterate through the points using Brensenham's line algorithm.
            http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm        
        """
        x0 = self.p1[0]
        y0 = self.p1[1]
        x1 = self.p2[0]
        y1 = self.p2[1]
        steep = abs(y1 - y0) > abs(x1 - x0)
        if (steep):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if (x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        deltax = x1 - x0
        deltay = abs(y1 - y0)
        error = 0.0
        deltaerr = float(deltay) / deltax
        y = y0
        if (y0 < y1): ystep = 1
        else: ystep = -1
        for x in xrange(x0, x1 + 1):
            if steep: yield (y, x)
            else: yield (x, y)
            error = error + deltaerr
            if (error >= 0.5):
                y = y + ystep
                error = error - 1

        
        