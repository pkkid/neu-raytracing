Assignment:  #0 - Triangles
Class:       CSG140 - Computer Graphics
Author:      Michael Shepanski


COLOR Triangles
===============

The first assignment for Computer Graphics with Harriet Fell.  This will draw
a triangle to the screen with 3 random end points.  Each endpoint will contain
a randomly selected color.  The triangle will be shaded in with a gradual
transition between the colors.


Install Dependencies
--------------------

This applications requires both Python and an additional Python component
called PyGame.  Follow the setup instructions below:

For Windows:
* Download and install Python-2.5 for your OS from Python.org:
  http://python.org/download/releases/2.5.4/
* Download and install PyGame-1.8.1 for Python-2.5 for your OS from Pygame.org:
  http://www.pygame.org/download.shtml
    
For Linux:
* Use your systems package manager to install PyGame.
  Ubuntu >> sudo apt-get install python-pygame
  Fedora >> sudo yum install pygame


Running the Application
-----------------------

This application is very simple.  After starting the application with the
command line 'python triangleapp.py' you will be presented with the first
random color triangle.  Click anywhere in the screen the generate a new
triangle.  When you are happy with the triangle presented simply close the
window.  Before quitting, A PNG and PPM file of the current image on the
screen will be saved to disk.


Known Issues
------------

ISSUE #1 - Invalid Color:
  Sometimes an error is raised when plotting a point saying the specified
  color is invalid.  This is believed to be due the the fact that the
  Brensenham's Line Algorithm sometimes returns a point outside the actual
  boundries of the triangle.  This ripples down when calculating the 
  Barycentric Coordinates, which could return values outside the triangle.
  
  Since we are only calculating the Barycentric Coordinates for points
  inside the triangle (because we already ran the Brensenham's Line Algorithm)
  we can assume these slightly off values can safely be drawn and simply chop
  the colors off at 0 or 256 respectivly (seen in ColorTriangle.getColorAt()).

  By doing this and not simply removing any points that produce a negative
  value in the Barycentric Coordinates, we also remove the clipping that can
  be seen for very this triangles.
  

