#!/usr/bin/python2.4
"""
Represents a 3D Plane.
Created by M.Shepanski
"""

import color
from vector import Vector
from worldobject import WorldObject

class Plane(WorldObject):
    """ Represents a 3D Sphere. """
    
    def __init__(self, p1, p2, p3, clr, kd=0.0, ks=0.0, se=6, kr=0.0):
        WorldObject.__init__(self, clr, kd, ks, se, kr)   # Call base class init
        self.p1 = p1                                      # 1st point on the Plane
        self.p2 = p2                                      # 2nd point on the Plane
        self.p3 = p3                                      # 3rd point on the Plane
        self.norm  = pow(p2-p1, p3-p1).normalize()        # Normal to the Plane
        self.dist  = self.norm * p1 * -1                  # Distance from the origin
        self.uNorm = (p2-p1).normalize()                  # U-Axis for uv coordinates
        self.vNorm = pow(self.norm, p2-p1).normalize()    # V-Axis for uv coordinates
        
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
        return ((self.norm == other.norm) and (self.dist == other.dist))
    
    def intersect(self, p0, p1):
        """ Given a ray, find the first intersection with this plane.
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
    
    def uvCoordinates(self, vec, resolution):
        """ Return the uv coordinates to grab from a texture.
            v = (Px*Dy - Py*Dx - Ax*Dy + Ay*Dx) / (Cx*Dy - Cy*Dx)
            u = (Px - Ax - v + Cx) / Dx
        """
        Ax, Ay, Az = self.p1.val()
        Cx, Cy, Cz = self.uNorm.val()
        Dx, Dy, Dz = self.vNorm.val()
        Px, Py, Pz = vec.val()
        # Calculate V
        if ((Cx*Dy) or (Cy*Dx)):  u = (Px*Dy - Py*Dx - Ax*Dy + Ay*Dx) / (Cx*Dy - Cy*Dx)
        if ((Cx*Dz) or (Cz*Dx)):  u = (Px*Dz - Pz*Dx - Ax*Dz + Az*Dx) / (Cx*Dz - Cz*Dx)
        if ((Cy*Dz) or (Cz*Dy)):  u = (Py*Dz - Pz*Dy - Ay*Dz + Az*Dy) / (Cy*Dz - Cz*Dy)
        # Calculate U
        if (Dx):  v = (Px - Ax - u*Cx) / Dx
        if (Dy):  v = (Py - Ay - u*Cy) / Dy
        if (Dz):  v = (Pz - Az - u*Cz) / Dz
        # Return the coordinates % our resolution
        return (u % resolution[0], v % resolution[1])
    
    
##############################
#  Unit Test
##############################
    
if (__name__ == "__main__"):
    print "\n--- Test 1 ---"
    plane = Plane(Vector(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0), color.RED)
    print plane.uvCoordinates(Vector(6, 2, 0), (100, 100))
    
    print "\n--- Test 1 ---"
    plane = Plane(Vector(0, 0, 10), Vector(0, 0, 0), Vector(0, 10, 10), color.RED)
    print plane.uvCoordinates(Vector(0, 6, 1), (100, 100))
        
        