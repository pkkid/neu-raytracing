#!/usr/bin/python2.4
"""
Assignment:  #0 Color Triangles
Class:       CSG140 - Computer Graphics
Author:      Michael Shepanski
"""

import time
import pygame
from graphics import functions
from graphics.colortriangle import ColorTriangle


class ColorTriangleApp:
    """ Assignment 0 - Color Triangle. """
    
    def __init__(self):
        self.assign = 0                    # Assignment Number
        # PyGame Variables
        self.width = 600                   # Image width
        self.height = 400                  # Image height
        self.running = True                # Set False to quit the Application
        self.screen = None                 # PyGame window for drawing
        
    def run(self):
        """ Run the Program. """
        # Initialize the display
        functions.initPyGame(self.assign)
        self.screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        # Draw first Image and wait for Events
        self._drawTriangle()
        pygame.display.flip()
        while (self.running):
            self._checkEvents()
            clock.tick(30)
            
    def _checkEvents(self):
        """ Check any window events. """
        for event in pygame.event.get():
            # Quit - Save Images and Close Application
            if (event.type == pygame.QUIT):
                self._saveImages()
                self.running = False
            # MouseUp - Draw a new triangle
            elif (event.type == pygame.MOUSEBUTTONUP):
                self._drawTriangle()
            
    def _drawTriangle(self):
        """ Draw the initial trangle. """
        # Draw the "Loading.." message; Init Variables
        functions.drawBigMessage(self.screen, "Loading..")
        startTime = time.time()
        numPoints = 0
        # Render the Triangle
        self.screen.fill((0, 0, 0))
        triangle = ColorTriangle.random(self.width, self.height)
        print "Redering: %s" % triangle
        for point in triangle.iterPoints():
            numPoints += 1
            try:
                color = triangle.getColorAt(point)
                if (color != None):
                    self.screen.set_at(point, color)
            except TypeError, err:
                print "ERROR: %s; %s; %s" % (err, point, color)
        # Add the signature and update the screen
        duration = time.time() - startTime
        functions.renderSignatureTest(self.screen, self.assign, numPoints, duration)
        pygame.display.flip()
    
    def _saveImages(self):
        """ Save images of the picture to disk. """
        #functions.drawBigMessage(self.screen, "Saving Images..")
        functions.savePNG(self.screen, "a%s.mshepanski.png" % self.assign)
        functions.savePPM(self.screen, "a%s.mshepanski.ppm" % self.assign)

                
#############################
# Command Line Interface
#############################

if (__name__ == "__main__"):
    ColorTriangleApp().run()

