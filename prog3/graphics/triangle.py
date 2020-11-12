#!/usr/bin/python2.4
"""
Represents a Triangle on a plane.
Created by M.Shepanski
"""

import color
from plane import Plane
from vector import Vector
from worldobject import WorldObject


class Triangle(Plane):
    """ Represents a 3D Sphere. """
    
    def __init__(self, p1, p2, p3, clr, kd=0.0, ks=0.0, se=6, kr=0.0):
        """ When passing in the 3 points of the triangle, it is important that you
            specifiy the ponits in a clockwise order.
        """
        Plane.__init__(self, p1, p2, p3, clr, kd, ks, se, kr)  # Call parent init
        
    def __str__(self):
        """ String Representation of this Plane. """
        rtn  = "%-15s  %s\n" % ("Triangle P1:", self.p1)
        rtn += "%-15s  %s\n" % ("Triangle P2:", self.p2)
        rtn += "%-15s  %s\n" % ("Triangle P3:", self.p3)
        return rtn
    
    def __eq__(self, other):
        """ Return True if this object is the same as other.
            @param other:  Object to use when comparing this.        
        """
        if (not isinstance(other, Triangle)): return False
        return ((self.p1 == other.p1) and (self.p2 == other.p2) and (self.p3 == other.p3))
    
    def intersect(self, p0, p1):
        """ Given a ray, find the first intersection with this triangle.
            If the ray does not intersect with this triangle, return None.
            Ref: http://www.experts-exchange.com/Programming/Game/3D_Prog./Q_20174959.html
            @param p1:  Origin of the casting ray.
            @param p2:  Point on the casting ray.
        """
        # Get the intersect from the Plane
        vec, t = Plane.intersect(self, p0, p1)[0]
        if (not vec):
            return [(None, None)]
        # We hit the Plane, now see if we're in the Triangle. Calculate the barycentric
        # coordinates of the point.  If any of alpha, beta, gamma is < 0 then we are
        # outside the triangle and should not return an intersect.
        areaABC = self.norm * pow(self.p2-self.p1, self.p3-self.p1)
        areaPBC = self.norm * pow(self.p2-vec, self.p3-vec)
        areaPCA = self.norm * pow(self.p3-vec, self.p1-vec)
        alpha   = areaPBC / areaABC
        beta    = areaPCA / areaABC
        gamma   = 1.0 - alpha - beta
        if (alpha < 0) or (beta < 0 ) or (gamma < 0):
            return [(None, None)]
        return [(vec, t)]
        
        
##############################
#  Unit Test
##############################
    
if (__name__ == "__main__"):
    tri = Triangle(Vector(0, 0, 10), Vector(10, 0, 10), Vector(0, 10, 10), color.RED)
    print tri.plane
    print tri.intersect(Vector(5,5,30), Vector(5,5,0))
    