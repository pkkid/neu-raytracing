#!/usr/bin/python2.4
"""
Represents a triangle
Created by M.Shepanski
"""

from point import randomPoint
from line import Line


class Triangle:
    """ Triangle object. """
    
    def __init__(self, p1, p2, p3):
        self.p1 = p1                  # First point in the triangle
        self.p2 = p2                  # Second point in the triangle
        self.p3 = p3                  # Third point in the triangle
        self.lines = [Line(p1, p2), Line(p2, p3), Line(p3, p1)]
    
    def __str__(self):
        """ String representation for this triangle. """
        return "Triangle(%s, %s, %s)" % (self.p1, self.p2, self.p3)
        
    def minX(self):  return min([self.p1[0], self.p2[0], self.p3[0]])
    def maxX(self):  return max([self.p1[0], self.p2[0], self.p3[0]])
    def minY(self):  return min([self.p1[1], self.p2[1], self.p3[1]])
    def maxY(self):  return max([self.p1[1], self.p2[1], self.p3[1]])
        
    def iterPoints(self):
        """ Iterate through pixels in the triangle.  This is done by first building a dictionary for
            each scan line of yVal => (minX, maxX).  After we have that we simply loop through each
            yVal and each xVal from min -> max.
        """
        borderPoints = self.getBorderPoints()
        for y in xrange(self.minY(), self.maxY() + 1):
            minX, maxX = borderPoints[y]
            for x in xrange(minX, maxX + 1):
                yield (x, y)
                
    def getBorderPoints(self):
        """ Return a list of all border points in relation to their Y values. Structure returned is a
            Dict of Tuples yVal => (minX, maxX).  NOTE: Because we are using Brensenham's line algorithm
            to trace the edges of the triangle, there is sometimes a point returned found just outside
            the boundries of the triangle.  The price to pay for efficiency I guess.
        """
        # Initialize Border Points
        borderPoints = {}
        for y in xrange(self.minY(), self.maxY() + 1):
            borderPoints[y] = []
        # Organize Points by their Y Coordinates
        for line in self.lines:            
            for point in line.iterPoints():
                borderPoints[point[1]].append(point[0])
        # Sort each List, and only takes the 2 ends
        for y, xVals in borderPoints.iteritems():
            xVals = sorted(xVals)
            borderPoints[y] = (xVals[0], xVals[-1])
        # Returns a Dict for each Y there are two entries for minX, maxX
        return borderPoints
                
    def iterBorderPoints(self):
        """ Iterate through pixels in the border.  This simply returns each pixel for all three
            lines in the triangle using Brensenham's line algorithm.
        """
        for point in Line(self.p1, self.p2).iterPoints():
            yield point
        for point in Line(self.p2, self.p3).iterPoints():
            yield point
        for point in Line(self.p3, self.p1).iterPoints():
            yield point
            
    def calcBarycentricCoordinates(self, point):
        """ Return the Barycentric Coordinates for the specified point.  Alpha, Beta, Gamma relates
            to p1, p2, p3 for this triangle.  The three return values will always add to 1.0.
        """
        alpha = self.calcBarycentricCoordinate(point, self.p2, self.p3, self.p1)
        beta  = self.calcBarycentricCoordinate(point, self.p3, self.p1, self.p2)
        gamma = self.calcBarycentricCoordinate(point, self.p1, self.p2, self.p3)
        return alpha, beta, gamma
    
    def calcBarycentricCoordinate(self, p, a, b, c):
        """ Return the Barycentric Coordinates for the specified point in relation to the three
            relative points of the trianble a,b,c.  The forumla's for doing this were pulled from
            H. Fell's lecture #1 slides at Northeastern University.
            fab(x,y) = (y-ya)(xb-xa) - (yb-ya)(x-xa)
            g = fab(x,y) / fab(xc,yc)
        """        
        fabXY   = float((p[1]-a[1]) * (b[0]-a[0]) - (b[1]-a[1]) * (p[0]-a[0]))
        fabXcYc = float((c[1]-a[1]) * (b[0]-a[0]) - (b[1]-a[1]) * (c[0]-a[0]))
        return fabXY / fabXcYc
        
    @staticmethod
    def random(maxX, maxY):
        """ Generate a triangle with 3 random points, staying within the boundries of maxX, maxY. """
        p1 = randomPoint(maxX, maxY)
        p2 = randomPoint(maxX, maxY)
        p3 = randomPoint(maxX, maxY)
        return Triangle(p1, p2, p3)
    
