Assignment:  #1 - World of Spheres
Class:       CSG140 - Computer Graphics
Author:      Michael Shepanski


Files Included
==============

prog1.py                    # CLI and base code for Program #1.
graphics/__init__.py        # Declares directory 'graphics' a Python module.
graphics/color.py           # Useful function for dealing with color tuples.
graphics/light.py           # Library for rendering a Light in the Scene.
graphics/pygametools.py     # One-off functions for drawing in PyGame window.
graphics/scene.py           # Represents a Scene (what we're looking at).
graphics/sphere.py          # Library for rendering a Sphere in the Scene.
graphics/vector.py          # Vector class for dealing with 3D-Vectors.
graphics/resources/...      # Image and Font resources used.
scene/basetest.scene        # Generic Scene used for debugging weird things.
scene/fellsdemo.scene       # Scene pulled from Fell's class notes.
scene/fellsdemo2.scene      # Another Scene (sorta) pulled from class notes.
scene/shadow.scene          # Scene shows a good shadow on another sphere.


Running the Application
=======================

You can run the program by executing the command:
>> python prog1.py

All Scene files are located in the scenes directory.  To execute a particular
scene you can use the command line option '-s'.  For example, if I wanted to
render the scene file fellsdemo2, you can execute the command:
>> python prog1.py -s fellsdemo2

Closing the PyGame window will generate images in a newly created 'images'
directory.  A PNG and a PPM file will both be saved.


Known Issues
============

1.) Multible lights are giving me some weird effects on the spheres.  However,
    this is not required for assignment #1 so I have some more time to debug.

