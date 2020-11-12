Assignment:  #2 - Reflection & Refraction
Class:       CSG140 - Computer Graphics
Author:      Michael Shepanski


Files Included
==============

prog2.py                    # CLI and base code for Program.
graphics/__init__.py        # Declares directory 'graphics' a Python module.
graphics/color.py           # Useful function for dealing with color tuples.
graphics/light.py           # Library for rendering a Light in the Scene.
graphics/plane.py           # Represents a 3D-Plane.
graphics/pygametools.py     # One-off functions for drawing in PyGame window.
graphics/scene.py           # Represents a Scene (what we're looking at).
graphics/sphere.py          # Represents a 3D-Sphere.
graphics/texture.py         # Dumping ground for new Texture functions.
graphics/triangle.py        # Represents a 2D Triangle on a 3D Plane.
graphics/vector.py          # Vector class for dealing with 3D-Vectors.
graphics/worldobject.py     # Base Class for all 3D-Objects.
graphics/resources/...      # Image and Font resources used.


Running the Application
=======================

All Scene files are located in the scenes directory.  To execute a particular
scene you can use the command line option '-s'.  You can run the program by
executing the commands:
>> python prog2.py -s bumpmap
>> python prog2.py -s imagemap

Closing the PyGame window will generate images in a newly created 'images'
directory.  A PNG and a PPM file will both be saved.


Known Issues
============

None
    

