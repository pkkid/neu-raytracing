#!/usr/bin/python2.4
"""
Represents a Vector.
Created by M.Shepanski
"""

import math
import random


class Vector:
    """ Represents a Vector in 3D. """
    
    def __init__(self, x, y, z):
        self.x = float(x)       # X Coordinate
        self.y = float(y)       # Y Coordinate
        self.z = float(z)       # Z Coordiante
     
    def __str__(self):
        """ String representation for this vector. """
        return "Vector(%s, %s, %s)" % (self.x, self.y, self.z)

    def __add__(self, other):
        """ Return Vector+Vector or Vector+Scalar.
            @param other:  Other Vector object to use when adding.
        """
        if (isinstance(other, Vector)):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Vector(self.x + other, self.y + other, self.z + other)
    
    def __sub__(self, other):
        """ Return Vector-Vector or Vector-Scalar.
            @param other:  Other Vector object to use when subtracting.
        """
        if (isinstance(other, Vector)):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Vector(self.x - other, self.y - other, self.z - other)
    
    def __mul__(self, other):
        """ Multiply Vector*Vector (dot product) or Vector * Scalar.
            @param other:  Other Vector object to use when taking dot product.
        """
        if (isinstance(other, Vector)):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            return Vector(self.x * other, self.y * other, self.z * other)
        
    def __pow__(self, other):
        """ Return VectorxVector (cross product).
            @param other:  Other Vector object to use when taking cross product.
        """
        x = round(self.y * other.z, 9) - round(self.z * other.y, 9)
        y = round(self.z * other.x, 9) - round(self.x * other.z, 9)
        z = round(self.x * other.y, 9) - round(self.y * other.x, 9)
        return Vector(x, y, z)
        
    def __div__(self, num):
        """ Divide a Vector by a non-zero scalar.
            @param num:  Scalar number to multiply this Vector by.
        """
        return Vector(self.x / num, self.y / num, self.z / num)
    
    def __eq__(self, other):
        """ Return true if two vectors are equal.
            @param other:  Other Vector object to use when comparing.
        """
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
    
    def __cmp__(self, other):
        """ Compare two vectors.  This is simply an __eq__.
            @param other:  Other Vector object to use when comparing.
        """
        return self.__eq__(other)
    
    def val(self):
        """ Return a tuple value for this vector. """
        return self.x, self.y, self.z
    
    def angle(self, other):
        """ Compute the angle between two vectors.
            @param other:  Other Vector object to use when comparing.
        """
        return math.acos((self * other) / round(self.length() * other.length(), 9))
    
    def isZero(self):
        """ Return True if this vector is zero. """
        return (self.x == 0) and (self.y == 0) and (self.z == 0)
    
    def length(self):
        """ Return the length of this vector. """
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))
    
    def normalize(self):
        """ Return this vector, but with a length of 1.0 """
        length = self.length()
        return Vector(self.x / length, self.y / length, self.z / length)
    
    def reflect(self, normVec):
        """ Reflect this vector across the specified normalVec.
            @param normVec:  Vector object to reflect this vector across.
        """
        sNorm = self.normalize()
        nNorm = normVec.normalize()
        return ((nNorm * (2 * (sNorm * nNorm))) - sNorm)
    
    def refract(self, normVec, ni, nt):
        """ Calculate the refraction between two medians.
            @param normVec:  Normal Vector at the point of intersection
            @param ni:       Indice of Refraction for this surface
            @param nt:       Indice of Refraction for new surface
            Common Refraction Indicies:
              Vacuum       1.0          |   Liquid Water:    1.333
              Helium       1.000036     |   Glass:           1.5 to 1.9
              Air at STP:  1.0002926    |   Cubic Zirconia:  2.15 to 2.18
              Water Ice:   1.31         |   Diamond:         2.419
        """
        try:
            iNorm = self.normalize()
            nNorm = normVec.normalize()
            cosThetaI = math.cos(nNorm.angle(iNorm))
            cosThetaT = math.sqrt(1 - pow(ni/nt, 2) * (1 - pow(nNorm*iNorm, 2)))
            vecRefract = nNorm * ((cosThetaT - ((ni/nt) * cosThetaI)) * -1) - (iNorm * (ni/nt))
            return vecRefract
        except:
            return None
    
    @staticmethod
    def random(maxX, maxY, maxZ):
        """ Return a random vector. """
        return Vector(random.randrange(maxX), random.randrange(maxY), random.randrange(maxZ))
    
    


###########################
#  Unit Tests Functions
###########################
    
def rad2deg(rad):
    return 180 * rad / 3.14159    
    

def test(strOp, expVal):
    """ Run a simple UnitTest given the op string and it's expected value. """
    try:
        result = str(eval(strOp))
        if (result == expVal): print " PASS: %s = %s" % (strOp, expVal)
        else: print "!FAIL: %s != %s (recieved: %s)" % (strOp, expVal, result)
    except Exception, err:
        if (expVal == "ERROR"): print " PASS: %s = ERROR; %s" % (strOp, err)
        else: print "!FAIL: %s != %s; %s" % (strOp, expVal, err)
    
        
###########################
#  Unit Tests
###########################

if (__name__ == "__main__"):
    air   = 1.00
    glass = 1.52
    #---
    vec1  = Vector(-1.0, -1.111, 0)
    nrm1  = Vector(0, -1, 0)
    ang1  = vec1.angle(nrm1)
    vec2 = vec1.refract(nrm1, air, glass)
    nrm2 = nrm1 * -1
    ang2 = vec2.angle(nrm2)
    print "vec1: %s"   % vec1
    print "nrm1: %s"   % nrm1
    print "ang1: %s'"  % rad2deg(ang1)
    print "vec2: %s'"  % vec2
    print "ang2: %s'"  % rad2deg(ang2)
    print "-----"
    #-----------
    vec1  = Vector(-0.4401, -0.8979, 0)
    nrm1  = Vector(0, -1, 0)
    ang1  = vec1.angle(nrm1)
    vec2 = vec1.refract(nrm1, glass, air)
    nrm2 = nrm1 * -1
    ang2 = vec2.angle(nrm2)
    print "vec1: %s"   % vec1
    print "nrm1: %s"   % nrm1
    print "ang1: %s'"  % rad2deg(ang1)
    print "vec2: %s'"  % vec2
    print "ang2: %s'"  % rad2deg(ang2)
    
    
    
    
    
    

