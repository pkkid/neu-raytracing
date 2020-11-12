#!/usr/bin/python2.4
"""
Represents a 3D Ellipse.
Created by M.Shepanski
"""

import color
import math
from vector import Vector
from vector import rad2deg
from worldobject import WorldObject


class Ellipse(WorldObject):
    """ Represents a 3D Sphere. """
    
    def __init__(self, center, a, b, c, clr, kd=0.0, ks=0.0, se=6, kr=0.0, kt=0.0, ni=1.6):
        WorldObject.__init__(self, clr, kd, ks, se, kr, kt, ni)  # Call base class init
        self.center = center         # Center point of the sphere (vector)
        self.a = a                   # Radius of the sphere on X Axis
        self.b = b                   # Radius of the sphere on Y Axis
        self.c = c                   # Radius of the sphere on Z Axis
        
    def __str__(self):
        """ String Representation of this Sphere. """
        rtn  = "%-15s  %s\n" % ("Ellipse Center: %s", self.center)
        rtn += "%-15s  %s\n" % ("A, B, C Radius: %s", str((self.a, self.b, self.c)))
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
            A = a*xd*xd + b*yd*yd + c*zd*zd + 2[d*xd*yd + e*yd*zd + f*xd*zd
            B = 2*[a*x0*xd + b*y0*yd + c*z0*zd + d*(x0*yd + xd*y0 )
                + e*(y0*zd + yd*z0 ) + f*(x0*zd + xd*z0 )
                + g*xd + h*yd + j*zd]
            C = a*x0*x0 + b*y0*y0 + c*z0*z0
                + 2*[d*x0*y0 + e*y0*z0 + f*x0*z0 + g*x0 + h*y0 + j*z0] + k
            @param p1:  Origin of the casting ray.
            @param p2:  Point on the casting ray.
        """
        intersects = []
        # Calculate the first few basic variables
        a, b, c = (self.a, self.b, self.c)
        x0, y0, z0 = p0.val()
        x1, y1, z1 = p1.val()
        cx, cy, cz = self.center.val()
        dx, dy, dz = x1-x0, y1-y0, z1-z0
        # Calculate Quadradic Coefficients
        ta = (dx*dx)/(a*a) + (dy*dy)/(b*b) + (dz*dz)/(c*c)
        tb = (2*cx*dx)/(a*a) + (2*cy*dy)/(b*b) + (2*cz*dz)/(c*c)
        tc = (cx*cx)/(a*a) + (cy*cy)/(b*b) + (cz*cz)/(c*c) - 1

        #ta = a*dx*dx + b*dy*dy + c*dz*dz
        #tb = 2*a*dx*(x0-cx) + 2*b*dy*(y0-cy) + 2*c*dz*(z0-cz)
        #tc = a*(x0-cx)*(x0-cx) + b*(y0-cy)*(y0-cy) + c*(z0-cz)*(z0-cz)
        
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
    
    def uvCoordinates(self, vec, resolution):
        """ Return the uv coordinates to grab from a texture. """
        # Make sure we're not directly above or below
        normToPoint = (vec - self.center).normalize()
        if (abs(normToPoint.y) == 1):
            return (1, 1)
        # Calculate U
        vecBack = Vector(0, 0, -1).normalize()
        xzRay = (vec - self.center)
        xzVec = Vector(xzRay.x, 0, xzRay.z).normalize()
        theta = vecBack.angle(xzVec)
        if (vec.x > self.center.x):
            theta = math.pi + math.pi - theta
        uPercent = theta / (math.pi * 2)
        # Calculate V
        phi = math.acos((self.center.y - vec.y) / self.radius)
        vPercent = phi / math.pi
        return (int(uPercent * resolution[0]), int(vPercent * resolution[1]))
        

##############################
#  Unit Test
##############################
    
if (__name__ == "__main__"):
    pass

        