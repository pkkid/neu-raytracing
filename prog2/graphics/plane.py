#!/usr/bin/python2.4
"""
Represents a 3D Plane.
Created by M.Shepanski
"""

import color
import math
from vector import Vector
from worldobject import WorldObject

class Plane(WorldObject):
    """ Represents a 3D Sphere. """
    
    def __init__(self, norm, dist, clr, kd=0.0, ks=0.0, se=6, kr=0.0):
        WorldObject.__init__(self, clr, kd, ks, se, kr)   # Call base class init
        self.norm = norm.normalize()                      # Normal to the Plane
        self.dist = dist                                  # Scalar Distance from origin
        
    def __str__(self):
        """ String Representation of this Plane. """
        rtn  = "%-15s  %s\n" % ("Plane Norm:", self.norm)
        rtn += "%-15s  %s\n" % ("Plane Dist:", self.dist)
        return rtn
    
    def __eq__(self, other):
        """ Return True if this object is the same as other.
            @param other:  Object to use when comparing this.        
        """
        if (not isinstance(other, Plane)): return False
        return ((self.pn == other.pn) and (self.dist == other.dist))
    
    def intersect(self, p0, p1):
        """ Given a ray, find the first intersection with this sphere.
            If the ray does not intersect with this plane, return None.
            Ref: http://www.siggraph.org/education/materials/HyperGraph/raytrace/rayplane_intersection.htm
            @param p1:  Origin of the casting ray.
            @param p2:  Point on the casting ray.
        """
        denominator = (p1 - p0) * self.norm
        if (denominator >= 0):
            return [(None, None)]
        numerator = -((p0 * self.norm) + self.dist)
        t = numerator / denominator
        if (t <= 0):
            return [(None, None)]
        intersect = p0 + (p1 - p0) * t
        return [(intersect, t)]
    
    def normal(self, vec):
        """ Return the normal to the plane. """
        return self.norm
    
    
##############################
#  Unit Test
##############################
    
if (__name__ == "__main__"):
    plane = Plane(Vector(1, 0, 0), -1, color.RED)
    p0 = Vector(3, 0, 0)
    p1 = p0 + Vector(-1, 0, 0)
    intersect, t = plane.intersect(p0, p1)[0]
    print plane
    print "p0: %s" % str(p0)
    print "p1: %s" % str(p1)
    print str(intersect), t
    print "-----------------"
    print "Example from Website:"
    plane = Plane(Vector(1, 0, 0), -7, color.RED)
    print plane
    p0 = Vector(2, 3, 4)
    p1 = Vector(3, 4, 5)
    intersect, t = plane.intersect(p0, p1)[0]
    print str(intersect), t
        
        