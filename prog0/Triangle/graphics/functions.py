#!/usr/bin/python2.4
"""
General functions
Created by M.Shepanski
"""

from os.path import abspath
from os.path import dirname
import pygame


def initPyGame(assign):
    """ Initialize PyGame. """
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_caption("Assignment #%s - M. Shepanski" % assign)
    # Set the Window icon
    iconPath = "%s/resources/favicon.gif" % dirname(abspath(__file__))
    icon = pygame.image.load(iconPath)
    pygame.display.set_icon(icon)

    
def drawBigMessage(surface, message):
    """ Draw loading text to the screen. """
    surface.fill((0, 0, 0))
    font = getLiberationFont(50)
    text = font.render(message, 0, (30,30,30))
    rect = text.get_rect()
    rect.center = surface.get_rect().center
    surface.blit(text, rect)
    pygame.display.flip()

    
def renderSignatureTest(surface, assign, numPoints, duration):
    """ Render the signature text. """
    # Create the message to display
    numPoints = numPoints / 1000.0
    pointsPerSec = numPoints / duration
    msg = ["Michael Shepanski",
           "Assignment #%s - CSG140" % assign,
           "%sK points - %sK points/sec" % (round(numPoints, 1), round(pointsPerSec, 1))]
    # Render the Message
    font = getLiberationFont(10)
    color = (120, 120, 120)
    xPos = surface.get_width() - 5
    yPos = surface.get_height() - 3
    for line in reversed(msg):
        text = font.render(line, 0, color)
        rect = text.get_rect()
        rect.bottomright = xPos, yPos
        yPos = yPos - 12
        surface.blit(text, rect)


def getLiberationFont(size=10):
    """ Return Liberations Sans font. """
    path = "%s/resources/liberationsans.ttf" % dirname(abspath(__file__))
    font = pygame.font.Font(path, size)
    return font


def savePNG(surface, filename):
    """ Save a PNG file to disk. """
    print "Saving image: %s" % filename
    pygame.image.save(surface, filename)
    
    
def savePPM(surface, filename):
    """ Save a PPM file to disk. """
    print "Saving image: %s" % filename
    handle = open(filename, 'w')
    # Write the PPM Header
    handle.write("P3\n")
    handle.write("%s %s\n" % (surface.get_width(), surface.get_height()))
    handle.write("255\n\n")
    # Write the pixel information
    for y in xrange(surface.get_height()):
        for x in xrange(surface.get_width()):
            r,g,b,max = surface.get_at((x,y))
            #print color
            handle.write("%s %s %s  " % (r,g,b))
        handle.write("\n")
    handle.close()

