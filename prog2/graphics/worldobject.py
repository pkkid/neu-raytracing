#!/usr/bin/python2.4
"""
Base Class for World Objects
Created by M.Shepanski
"""

import color
from texture import Texture


class WorldObject:
    """ Base Class for World Objects. """
    
    def __init__(self, clr, kd=0.0, ks=0.0, se=6, kr=0.0, kt=0.0, ni=1.6):
        self.color = clr            # Object Base Color
        self.kd = kd                # Diffuse coefficient (float)
        self.ks = ks                # Specular coefficient (float)
        self.se = se                # Specular exponent (0 if ks = 0) (int)
        self.kr = kr                # Reflective coefficient
        self.kt = kt                # Transmitting coefficient (Refraction)
        self.ni = ni                # Index of Refraction
        
    def _verifySettings(self):
        """ Check settings for invalid options. """
        assert (self.kr >= 1.0), "Reflective coefficient (kr) must be 0 <= kr < 1."
        
    #############################
    #  Required Definitions
    #############################
        
    def __str__(self):
        """ String Representation of this World Object. """
        raise Exception("Function undefined: __str__")
    
    def __eq__(self, other):
        """ Return True if this object is the same as other. """
        raise Exception("Function undefined: __eq__")
    
    def intersect(self, p0, p1):
        """ Return a list of intersect Points and distance t from p0. """
        raise Exception("Function undefined: intersect")
    
    def normal(self, vec):
        """ Return the normal from the specified point on the object. """
        raise Exception("Function undefined: getNormal")
    
    def surfaceColor(self, vec):
        """ Return the surface color for the specified xyv coordinate.  If self.color
            is a tuple, then this World Object is a solid color, otherwise a callback
            function was specifed which will return the color for us.
        """
        if   (isinstance(self.color, tuple)):    return self.color
        elif (isinstance(self.color, Texture)):  return self.color.getColor(vec)
        raise Exception("Unknown Color Type: %s" % self.color)
    
    #############################
    #  Color Calculations
    #############################
    
    def getColorFromRay(self, scene, vec, viewPoint, recur=0):
        """ Given other objects in the scene, return the color at the specified point.
            @param scene: Scene object this World Object belongs to.
            @param vec: (x,y,z) Vector point to return the current color of. NOTE: We're
              assuming the passed in vec is on the surface of this object, that value is
              caclulated at using self.intersection(), but we avoid calculating it again.
            @param viewPoint: Current viewpoint we're looking at this object from.
            @param recur: Recursion Level (we'll stop at 3)
        """
        # Calculate Color from Ambient Light
        colorPoint = self._getColorAmbient(scene, vec)
        # Calculate Color from Light Sources
        for light in scene.lights:
            colorFromLight = self._getColorFromLight(scene, vec, light, viewPoint)
            colorPoint = color.add(colorPoint, colorFromLight)
        # Calculate Color from Reflection
        if (self.kr) and (recur <= 3):
            colorReflect = self._getColorFromReflect(scene, vec, viewPoint, recur)
            colorPoint = color.add(colorPoint, colorReflect)
        # Calculate Color from Refraction
        if (self.kt) and (recur <= 3):
            colorRefract = self._getColorFromRefract(scene, vec, viewPoint, recur)
            colorPoint = color.add(colorPoint, colorRefract)
        return colorPoint
    
    def _getColorAmbient(self, scene, vec):
        """ Return the color from ambient light for this World Object.
            @param scene:  Scene object this World Object belongs to.
        """
        surfaceColor = self.surfaceColor(vec)
        return color.mul(surfaceColor, scene.ka)
    
    def _getColorFromLight(self, scene, vec, light, viewPoint):
        """ Return the color of this point on the World Object prodecuded by the
            the specified light source.
            @param scene:  Scene object this World Object belongs to.
            @param vec:  (x,y,z) Vector point to return the current color of.
            @param light:  Light object to use when calculating color.
            @param viewPoint:  Current viewpoint we're looking at this object from.
        """
        # Calculate some variables to work with
        normObject = self.normal(vec)
        normLight  = (light.center - vec).normalize()
        isShadow   = scene.isShadow(vec, light, self)
        # Calculate the color from Lamberts Diffuse Algorithm
        kd = [self.kd, self.kd * 0.3][isShadow]
        surfaceColor = self.surfaceColor(vec)
        factorLambert = max(normObject * normLight, 0)
        colorLambert = color.mul(surfaceColor, factorLambert)
        colorLambert = color.mul(colorLambert, kd)
        # Calculate the color from Phongs Highlight Algorithm
        colorPhong = (0, 0, 0)
        if (not isShadow):
            normReflect = normLight.reflect(normObject)
            normToView  = (viewPoint - vec).normalize()
            factorPhong = pow(max(normReflect * normToView, 0), self.se)
            colorPhong = color.mul(light.color, factorPhong)
            colorPhong = color.mul(colorPhong, self.ks)
        return color.add(colorLambert, colorPhong)
        
    def _getColorFromReflect(self, scene, vec, viewPoint, recur):
        """ Return the color of this point from reflection.
            @param scene:  Scene object this World Object belongs to.
            @param vec:    (x,y,z) Vector point to return the current color of.
            @param recur:  Recursion Level (we'll stop at 3)
        """
        colorReflect = (0, 0, 0)
        # Calculate the Reflection Vector and RayPoint
        normToView  = (viewPoint - vec).normalize()
        normObject  = self.normal(vec)
        normReflect = normToView.reflect(normObject)
        rayPoint    = vec + normReflect
        # Get the Visible object and Color from that object
        visObj, visVec = scene.getVisibleObject(vec, rayPoint, self)
        if (visObj):
            colorReflect = visObj.getColorFromRay(scene, visVec, vec, recur + 1)
            colorReflect = color.mul(colorReflect, self.kr)
        return colorReflect
    
    def _getColorFromRefract(self, scene, vec, viewPoint, recur):
        """ Return the color of this point from refraction.
            @param scene:  Scene object this World Object belongs to.
            @param vec:    (x,y,z) Vector point to return the current color of.
            @param recur:  Recursion Level (we'll stop at 3)
        """
        try:
            colorRefract = (0, 0, 0)
            # Calculate the Refraction Vector and RayPoint from outside to inside
            normToView    = (viewPoint - vec).normalize()
            normObject    = self.normal(vec)
            normRefractIn = normToView.refract(normObject, scene.ni, self.ni)
            rayPointIn    = vec + normRefractIn
            # Calculate the Refraction Vector and RayPoint leaving the object
            newVec, t      = self.intersect(vec, rayPointIn)[-1]
            newNormToView  = normRefractIn * -1
            newNormObject  = self.normal(newVec) * -1
            normRefractOut = newNormToView.refract(newNormObject, self.ni, scene.ni)
            rayPointOut    = newVec + normRefractOut
            # Get the Visible object and Color from that object
            visObj, visVec = scene.getVisibleObject(newVec, rayPointOut, self)
            if (visObj):
                colorRefract = visObj.getColorFromRay(scene, visVec, newVec, recur + 1)
                colorRefract = color.mul(colorRefract, self.kt)
            # Log this function is requested
            if (scene.logging):
                try:
                    scene.log("vec:             %s" % str(vec))
                    scene.log("viewPoint:       %s" % str(viewPoint))
                    scene.log("normToView:      %s" % str(normToView))
                    scene.log("normObject:      %s" % str(normObject))
                    scene.log("angle in:        %s'" % rad2deg(normToView.angle(normObject)))
                    scene.log("angle out:       %s'" % rad2deg(normRefractIn.angle(normObject * -1)))
                    scene.log("normRefractIn:   %s" % str(normRefractIn))
                    scene.log("rayPointIn:      %s" % str(rayPointIn))
                    scene.log("----")
                    scene.log("newVec:          %s, t=%s" % (str(newVec), t))
                    scene.log("newNormToView:   %s" % str(newNormToView))
                    scene.log("newNormObject:   %s" % str(newNormObject))
                    scene.log("angle in:        %s'" % rad2deg(newNormToView.angle(newNormObject)))
                    scene.log("angle out:       %s'" % rad2deg(normRefractOut.angle(newNormObject * -1)))
                    scene.log("normRefractOut:  %s" % str(normRefractOut))
                    scene.log("rayPointOut:     %s" % rayPointOut)
                    scene.log("Back Wall:       %s" % str(visVec))
                except:
                    pass
        finally:
            return colorRefract

        
def rad2deg(rad):
    return 180 * rad / 3.14159  
        
        
        
        