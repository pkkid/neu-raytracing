#!/usr/bin/python2.4
"""
Represents a 3D Sphere.
Created by M.Shepanski
"""

import color
import math
from vector import Vector
from worldobject import WorldObject


class Sphere(WorldObject):
    """ Represents a 3D Sphere. """
    
    def __init__(self, center, radius, clr, kd=0.0, ks=0.0, se=6, kr=0.0, kt=0.0, ni=1.6):
        WorldObject.__init__(self, clr, kd, ks, se, kr, kt, ni)  # Call base class init
        self.center = center               # Center point of the sphere (vector)
        self.radius = radius               # Radius of the sphere (int)
        
    def __str__(self):
        """ String Representation of this Sphere. """
        rtn  = "%-15s  %s\n" % ("Sphere Center:", self.center)
        rtn += "%-15s  %s\n" % ("Sphere Radius:", self.radius)
        rtn += "%-15s  %s\n" % ("Sphere Color:",  self.color)
        return rtn
    
    def __eq__(self, other):
        """ Return True if this object is the same as other.
            @param other:  Object to use when comparing this.        
        """
        if (not isinstance(other, Sphere)): return False
        return ((self.center == other.center) and (self.radius == other.radius))
    
    def intersect(self, p0, p1):
        """ Given a ray, find the first intersection with this sphere.
            If the ray does not intersect with this sphere, return None.
            Ref: http://www.ccs.neu.edu/home/fell/CSU540/programs/RayTracingFormulas.htm
            @param p1:  Origin of the casting ray.
            @param p2:  Point on the casting ray.
        """
        intersects = []
        # Calculate the first few basic variables
        x0, y0, z0 = p0.val()
        x1, y1, z1 = p1.val()
        cx, cy, cz = self.center.val()
        dx, dy, dz = x1-x0, y1-y0, z1-z0
        # Calculate Quadradic Coefficients
        ta = dx*dx + dy*dy + dz*dz
        tb = 2*dx*(x0-cx) + 2*dy*(y0-cy) + 2*dz*(z0-cz)
        tc = cx*cx + cy*cy + cz*cz + x0*x0 + y0*y0 + z0*z0 + \
             -2*(cx*x0 + cy*y0 + cz*z0) - pow(self.radius, 2)
        # Use the Discriminant to know what to return
        discriminant = tb*tb - 4*ta*tc
        if (discriminant <= 0):
            return [(None, None)]
        # Calcuate the closer intersect
        t = (-1*tb - math.sqrt(discriminant)) / (2*ta)
        intersect = Vector(x0+t*dx, y0+t*dy, z0+t*dz)
        intersects.append((intersect, t))
        # Calculate the further intersect
        t = (-1*tb + math.sqrt(discriminant)) / (2*ta)
        intersect = Vector(x0+t*dx, y0+t*dy, z0+t*dz)
        intersects.append((intersect, t))
        return intersects
    
    def normal(self, vec):
        """ Return the normal from the specified point. """
        return (vec - self.center).normalize()
        
        