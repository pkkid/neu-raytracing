#!/usr/bin/python2.4
"""
Assignment:  #1 World of Spheres
Class:       CSG140 - Computer Graphics
Author:      Michael Shepanski
"""

import cProfile
import os
import pygame
from graphics import pygametools
from graphics.scene import Scene
from optparse import OptionParser
from os.path import abspath
from os.path import dirname

ASSIGNMENT   = 4
WINDOWTITLE  = "Assignment #%s - M. Shepanski" % ASSIGNMENT
FAVICON      = "%s/graphics/resources/favicon.gif" % dirname(abspath(__file__))
FONTCOLOR    = (128, 128, 128)
FOOTERHEIGHT = 43


class WorldOfSpheres:
    """ Assignment 1 - World of Spheres """
    
    def __init__(self, sceneFile):
        # Scene object we're rendering
        self.sceneFile = sceneFile                      # Scene File to render
        self.scene = Scene.createFromFile(sceneFile)    # Assignment Number
        # Pygame screen object
        self.resolution = None                          # Screen Resolution
        self.screen = None                              # Main PyGame Screen 
        self.running = True                             # Set False to quit the Application
        self._initPyGame()                              # Init basic PyGame settings
        
    def _initPyGame(self):
        """ Initialize the PyGame window. """
        icon = pygame.image.load(FAVICON)
        pygame.display.init()
        pygame.display.set_caption(WINDOWTITLE)
        pygame.display.set_icon(icon)
        # Find the Screen resolution (with footer)
        sceneRes = self.scene.resolution
        self.resolution = (sceneRes[0], sceneRes[1] + FOOTERHEIGHT)
        self.screen = pygame.display.set_mode(self.resolution)
        
    def run(self):
        """ Run the Program. """
        clock = pygame.time.Clock()
        print "%s%s" % (self.scene, '-' * 10)
        self.scene.renderScene(self.screen)
        self._flipScreen()
        while (self.running):
            self._processEvents()
            clock.tick(10)
            
    def displayPointStats(self, pos):
        """ Display Stats for the single specified (x, y) position.
            @param pos: (x,y) coordinate on the window you want to calculate        
        """
        print self.scene.get_at(pos)
            
    #################################
    #  Event Processing
    #################################            
            
    def _processEvents(self):
        """ Check any window events. """
        mouseMotionUpdated = False
        for event in reversed(pygame.event.get()):
            if (event.type == pygame.QUIT):               self._eventQuit(event)
            elif (event.type == pygame.MOUSEBUTTONDOWN):  self._eventMountButtonDown(event)
            elif (event.type == pygame.MOUSEMOTION):
                if (not mouseMotionUpdated):
                    self._eventMouseMotion(event)
                    mouseMotionUpdated = True
                
    def _eventQuit(self, event):
        """ Save the images to disk and quit the application.
            @param event: PyGame event object
        """
        # Find the images directory and save the files 
        baseDir = "%s/images" % dirname(abspath(__file__))
        if (not os.path.exists(baseDir)):
            os.mkdir(baseDir)
        pygametools.savePNG(self.screen, "%s/a%s.%s.png" % (baseDir, ASSIGNMENT, self.scene.name))
        pygametools.savePPM(self.screen, "%s/a%s.%s.ppm" % (baseDir, ASSIGNMENT, self.scene.name))
        # Set our running flag to False
        self.running = False
                
    def _eventMountButtonDown(self, event):
        """ Drop the current point information to Command Line.
            @param event: PyGame event object
        """
        objinfo = self.scene.coordinfo.get(event.pos)
        message  = "Pos:   %s\n" % str(event.pos)
        message += "Color: %s\n" % str(self.screen.get_at(event.pos)[0:3])
        if (objinfo): message += objinfo
        print "\n%s" % message
        
    def _eventMouseMotion(self, event):
        """ Redraw the screen with new stats.
            @param event: PyGame event object
        """
        self._flipScreen(event.pos)
                        
    #################################
    #  PyGame Rendering Functions
    #################################
    
    def _flipScreen(self, statPos=(0, 0)):
        """ Flip the image (Update the screen).
            @param statPos:  Current mouse (x,y) position.
        """
        self.screen.fill((0, 0, 0))                     # Clear the Screen
        self.screen.blit(self.scene.image, (0, 0))      # Draw the Image
        self._renderFooter(self.screen, statPos)        # Draw the Footer info
        pygame.display.flip()                           # Send it all out
        
    def _renderFooter(self, surface, statPos):
        """ Render Footer text on the specified surface.
            @param surface:  PyGame Surface object to render the footer onto.
            @param statPos:  Current mouse (x,y) position.
        """
        # Draw the grey background
        footerTopLeft = (0, self.resolution[1] - FOOTERHEIGHT)
        footerRec = pygame.Rect(footerTopLeft, (self.resolution[0], FOOTERHEIGHT))
        pygame.draw.rect(surface, (10, 10, 10), footerRec)
        # Draw the divider line
        footerTopRight = [self.resolution[0], footerTopLeft[1]]
        pygame.draw.line(surface, (25, 25, 25), footerTopLeft, footerTopRight)
        # Add the Stats and Signature text
        self._renderSignature(self.screen)
        self._renderStatistics(self.screen, statPos)
        
    def _renderSignature(self, surface):
        """ Render Signature to Lower Right on specified surface.
            @param surface:  PyGame Surface object to render the signature onto.
        """
        # Create the message to display    
        message  = "Michael Shepanski\n"
        message += "Assignment #%s - CSG140\n" % ASSIGNMENT
        if (self.scene.duration):
            numPointsK    = round(self.scene.pointsRendered / 1000.0, 1)
            pointsKPerSec = int(numPointsK / self.scene.duration)
            durationStr   = pygametools.getDurationString(self.scene.duration)
            message += "%sK points in %s (%sK pts/sec)" % (numPointsK, durationStr, pointsKPerSec)
        # Render the Message
        xPos, yPos = surface.get_width()-5, surface.get_height()-3
        for msgline in reversed(message.split('\n')):
            text = pygametools.FONTTINY.render(msgline, True, FONTCOLOR)
            rect = text.get_rect()
            rect.bottomright = xPos, yPos
            yPos = yPos - 12
            surface.blit(text, rect)
        
    def _renderStatistics(self, surface, statPos):
        """ Render Stats to Lower Left on specified surface.
            @param surface:  PyGame Surface object to render the stats onto.
            @param statPos:  Current mouse (x,y) position.
        """
        # Create the message to display
        objinfo = self.scene.coordinfo.get(statPos)
        posColor = self.screen.get_at(statPos)[0:3]
        message  = "Pos: %s\n"   % str(statPos)
        message += "Color: %s\n" % str(posColor)
        if (objinfo): message += objinfo
        # Render the Message
        xPos, yPos = 5, surface.get_height()-3
        for msgline in reversed(message.split('\n')):
            text = pygametools.FONTTINY.render(msgline, True, FONTCOLOR)
            rect = text.get_rect()
            rect.bottomleft = xPos, yPos
            yPos = yPos - 12
            surface.blit(text, rect)
            # Add the color box
            if (msgline.startswith("Color:")):
                colorLeft = rect.left + rect.width + 5
                colorRec  = pygame.Rect((colorLeft, rect.top+3), (8, 8))
                pygame.draw.rect(surface, posColor, colorRec)
            
            
###############################
#  Command Line Interface
###############################

if (__name__ == "__main__"):
    parser = OptionParser()
    parser.add_option("-s", "--scene",   default="basetest", help="FileName of Scene to render (without .py)")
    parser.add_option("-p", "--point",   help="Only calculate the specified point (x, y).")
    options, args = parser.parse_args()
    if (options.point != None):
        myScene = Scene.createFromFile(options.scene)
        myScene.logging = True
        color = myScene.get_at(eval(options.point))
    else:
        WorldOfSpheres(options.scene).run()
            
            