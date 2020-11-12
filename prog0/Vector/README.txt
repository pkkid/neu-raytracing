Assignment:  #0 - Vector Class
Class:       CSG140 - Computer Graphics
Author:      Michael Shepanski


Vector.py
=========

A 3D Vector class written in Python for use in Computer Graphics.


Running the Unit Tests
----------------------

To run the built in unit tests in Vector.py simply run the command line:
>> python vector.py

You will see a series of tests performed, preceded by it's PASS / FAIL result.
Each test performs an eval() operation on a string and compares it with a
passed in expected result.


Known Issues
------------

Issue #1 - Floating Point Arithmetic:
  Floating point math is a bit fuzzy around the edges.  For example: -1.0 * 0.0
  will return the result -0.0 (notice the negative sign).  This is a limitation
  of Python representing as binary fractions and not true decimal fractions.
  These limitations can be seen by the two failing Vector unit tests.
 
  An implemented work around is to round the numbers at a some precision
  after performing a float * float operation.  I found the solution at
  the link below, but would like to discuss it a little more in class.
  http://www.velocityreviews.com/forums/t303022-java-float-problem.html

