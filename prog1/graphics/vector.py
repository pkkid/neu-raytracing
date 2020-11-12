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
    
    @staticmethod
    def random(maxX, maxY, maxZ):
        """ Return a random vector. """
        return Vector(random.randrange(maxX), random.randrange(maxY), random.randrange(maxZ))
    

#########################
#  Unit Tests
#########################
    
if (__name__ == "__main__"):
    # Define a simple test function
    def test(strOp, expVal):
        """ Run a simple UnitTest given the op string and it's expected value. """
        try:
            result = str(eval(strOp))
            if (result == expVal): print " PASS: %s = %s" % (strOp, expVal)
            else: print "!FAIL: %s != %s (recieved: %s)" % (strOp, expVal, result)
        except Exception, err:
            if (expVal == "ERROR"): print " PASS: %s = ERROR; %s" % (strOp, err)
            else: print "!FAIL: %s != %s; %s" % (strOp, expVal, err)
    # Test Basic Vector Creation, Add, and Subtract
    test("Vector(0, 0, 0)",                              "Vector(0.0, 0.0, 0.0)")
    test("Vector(0, 0, 0) + Vector(1, 1, 1)",            "Vector(1.0, 1.0, 1.0)")
    test("Vector(-1, 0.1, 99) + Vector(2, 4, 6)",        "Vector(1.0, 4.1, 105.0)")
    test("Vector(-1, 0.1, 99) + 2",                      "Vector(1.0, 2.1, 101.0)")
    test("Vector(0, 0, 0) - Vector(0, 0, 0)",            "Vector(0.0, 0.0, 0.0)")
    test("Vector(2, 4, 6) - Vector(7, 8, 1.1)",          "Vector(-5.0, -4.0, 4.9)")
    # Test Multiply and Divide
    test("Vector(0, 0, 0) * Vector(0, 0, 0)",            "0.0")
    test("Vector(1, 2, 3) * Vector(4, 5, 6)",            "32.0")
    test("Vector(1.0, -2, 0.001) * Vector(0, 1.4, 2.0)", "-2.798")
    test("Vector(1.0, 2.0, -1) * 3.0",                   "Vector(3.0, 6.0, -3.0)")
    test("Vector(0, 0, 0) / 0",                          "ERROR")
    test("Vector(10, 9, 8) / 2",                         "Vector(5.0, 4.5, 4.0)")
    test("Vector(0.0, 3.3, 12.1) / 3",                   "Vector(0.0, 1.1, 4.03333333333)")
    # Test Equal and isZero
    test("Vector(1, 2, 3) == Vector(1.0, 2.0, 3.0)",     "True")
    test("Vector(1, 2, 3) == Vector(1.0, 2.00001, 3.0)", "False")
    test("Vector(1, 2, 3).isZero()",                     "False")
    test("Vector(0, 0.0, 0).isZero()",                   "True")
    # Test Length and Normalize
    test("Vector(1, 1, 0).length()",                     "1.41421356237")
    test("Vector(-1, -1, 0).length()",                   "1.41421356237")
    test("Vector(1, 1, 1).length()",                     "1.73205080757")
    test("Vector(2, 4, 6).length()",                     "7.48331477355")
    test("Vector(10, 0, 0).normalize()",                 "Vector(1.0, 0.0, 0.0)")
    test("Vector(1, 1, 0).normalize()",                  "Vector(0.707106781187, 0.707106781187, 0.0)")
    test("Vector(-2, 12, 5).normalize()",                "Vector(-0.152057184254, 0.912343105524, 0.380142960635)")
    # Test Cross and Angle
    test("pow(Vector(1, 0, 0), Vector(0, 1, 0))",        "Vector(0.0, 0.0, 1.0)")
    test("pow(Vector(1, 1, 0), Vector(-1, -1, 0))",      "Vector(0.0, 0.0, 0.0)")
    test("pow(Vector(1, 0, 0), Vector(0, 1, 0))",        "Vector(0.0, 0.0, 1.0)")
    test("Vector(1, 0, 0).angle(Vector(0, 1, 0))",       "1.57079632679")
    test("Vector(0, 1, 0).angle(Vector(1, 0, 0))",       "1.57079632679")
    test("Vector(1, 0, 0).angle(Vector(1, 1, 0))",       "0.785398163134")
    test("Vector(1, 1, 1).angle(Vector(-1, 0, 0))",      "2.18627603529")
    test("Vector(1, 1, 0).angle(Vector(-1, -1, 0))",     "3.14159265359")
    test("Vector(0, 1, 1).angle(Vector(0, 1, 0))",       "0.785398163134")
    test("Vector(1, 1, 1).angle(Vector(-1, -1, -1))",    "3.14159265359")
    # Test Reflection Angles
    test("Vector(1, 1, 0).reflect(Vector(0, 1, 0))",     "Vector(-0.707106781187, 0.707106781187, 0.0)")
    test("Vector(1, 1, 1).reflect(Vector(0, 1, 0))",     "Vector(-0.57735026919, 0.57735026919, -0.57735026919)")
    
    

