#!/usr/bin/python2.4
"""
Represents a 3D Sphere.
Created by M.Shepanski
"""

import color
import math
from vector import Vector


class Sphere:
    """ Represents a 3D Sphere. """
    
    def __init__(self, center, radius, scolor, kd=0.0, ks=0.0, se=6):
        self.center = center        # Center point of the sphere (vector)
        self.radius = radius        # Radius of the sphere (int)
        self.color = scolor         # Color of the sphere (color)
        # Light Interactions
        self.kd = kd                # Diffuse coefficient (float)
        self.ks = ks                # Specular coefficient (float)
        self.se = se                # Specular exponent (0 if ks = 0) (int)
        
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
        return ((self.center == other.center) and (self.radius == other.radius)
                and (self.color == other.color) and (self.kd == other.kd)
                and (self.ks == other.ks) and (self.se == other.se))
    
    def get_at(self, scene, vec):
        """ Given other objects in the scene, return the color at the specified point.
            @param scene:  Scene object this Sphere belongs to.
            @param vec:    (x,y,z) Vector point to return the current color of.  NOTE: We're
                           assuming the passed in vec is on the surface of this object,
                           that value is caclulated at using self.intersection(), but we want
                           to avoid calculating it again.
        """
        colorPoint = self._getColorAmbient(scene)
        for light in scene.lights:
            colorFromLight = self._getColorFromLight(scene, vec, light)
            colorPoint = color.add(colorPoint, colorFromLight)
        return colorPoint
    
    def _getColorAmbient(self, scene):
        """ Return the color from ambient light for this sphere.
            @param scene:  Scene object this Sphere belongs to.
        """
        return color.mul(self.color, scene.ka)
    
    def _getColorFromLight(self, scene, vec, light):
        """ Return the color of this point on the sphere prodecuded by the
            the specified light source.
            @param scene:  Scene object this Sphere belongs to.
            @param vec:    (x,y,z) Vector point to return the current color of.
            @param light:  Light object to use when calculating color.
        """
        # Calculate some variables to work with
        normSphere = (vec - self.center).normalize()
        normLight  = (light.center - vec).normalize()
        isShadow   = scene.isShadow(vec, light, self)
        # Calculate the color from Lamberts Diffuse Algorithm
        kd = [self.kd, self.kd * 0.3][isShadow]
        factorLambert = max(normSphere * normLight, 0)
        colorLambert = color.mul(self.color, factorLambert)
        colorLambert = color.mul(colorLambert, kd)
        # Calculate the color from Phongs Highlight Algorithm
        colorPhong = (0, 0, 0)
        if (not isShadow):
            normReflect = normLight.reflect(normSphere)
            normToView  = (scene.viewPoint - vec).normalize()
            factorPhong = pow(max(normReflect * normToView, 0), self.se)
            colorPhong = color.mul(light.color, factorPhong)
            colorPhong = color.mul(colorPhong, self.ks)
        return color.add(colorLambert, colorPhong)
            
    def intersect(self, p0, p1):
        """ Given a ray, find the first intersection with this sphere.
            If the ray does not intersect with this sphere, return None.
            Ref: http://www.ccs.neu.edu/home/fell/CSU540/programs/RayTracingFormulas.htm
            @param p1:  Origin of the casting ray.
            @param p2:  Point on the casting ray at value t=1.
        """
        # Calculate the first few basic variables
        x0, y0, z0 = p0.val()
        x1, y1, z1 = p1.val()
        cx, cy, cz = self.center.val()
        dx, dy, dz = x1-x0, y1-y0, z1-z0
        # Calculate Quadradic Coefficients
        ta = dx*dx + dy*dy + dz*dz
        tb = 2*dx*(x0-cx) + 2*dy*(y0-cy) + 2*dz*(z0-cz)
        tc = cx*cx + cy*cy + cz*cz + x0*x0 + y0*y0 + z0*z0 +\
             -2*(cx*x0 + cy*y0 + cz*z0) - pow(self.radius, 2)
        # Use the Discriminant to know what to return
        discriminant = tb*tb - 4*ta*tc
        if (discriminant <= 0):
            return None, None
        t = min((-1*tb - math.sqrt(discriminant)) / (2*ta), 1.0)
        intersect = Vector(x0+t*dx, y0+t*dy, z0+t*dz)
        return intersect, t
        
