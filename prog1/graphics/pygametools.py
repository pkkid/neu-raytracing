#!/usr/bin/python2.4
"""
General functions
Created by M.Shepanski
"""

import pygame
from os.path import basename
from os.path import dirname

pygame.font.init()
FONTPATH   = "%s/resources/liberationsans.ttf" % dirname(__file__)
LOGOPATH   = "%s/resources/avatar.png" % dirname(__file__)
LOGO       = pygame.image.load(LOGOPATH)
FONTBIG    = pygame.font.Font(FONTPATH, 50)
FONTMEDIUM = pygame.font.Font(FONTPATH, 20)
FONTTINY   = pygame.font.Font(FONTPATH, 10)
FONTCOLOR  = (128, 128, 128)


def flipLoadingMessage(surface, percent, duration):
    """ Flip the Loading message to the screen.
        @param surface:   PyGame Surface object to render loading message onto.
        @param percent:   Current percent complete in scene render.
        @param duration:  Seconds passed since Scene render started.
    """
    surface.fill((0, 0, 0))
    # Draw the grey background
    barWidth = surface.get_width()
    barTop = int(surface.get_height() / 2) - 50
    barRec = pygame.Rect((0, barTop), (barWidth, 100))
    pygame.draw.rect(surface, (10, 10, 10), barRec)
    pygame.draw.line(surface, (25, 25, 25), (0, barTop), (barWidth, barTop))
    pygame.draw.line(surface, (25, 25, 25), (0, barTop+100), (barWidth, barTop+100))
    surface.blit(LOGO, (80, barTop+19))
    # Render the Loading text
    loadingMsg  = "Loading.. %s%%" % int(round(percent))
    loadingText = FONTBIG.render(loadingMsg, True, FONTCOLOR)
    surface.blit(loadingText, (145, barTop+10))
    # Render the Time Left text
    if (percent and duration):
        totalTime = (float(duration) / percent) * 100
        timeLeft  = int(totalTime - duration)
        minLeft   = int(timeLeft / 60)
        secLeft   = timeLeft - (minLeft * 60)    
        timeleftMsg  = "Time Left: %s:%s" % (minLeft, str(secLeft).zfill(2))
        timeLeftText = FONTMEDIUM.render(timeleftMsg, True, FONTCOLOR)
        surface.blit(timeLeftText, (148, barTop+60))
    # Finish Up, Draw the text
    pygame.display.flip()

def getDurationString(duration):
    """ Return a nicely formatted string for duration.
        @param duration:  Seconds passed to return duration string for.
    """
    durations = []
    duration = int(duration)
    if (duration >= 3600):
        hours = int(duration / 3600)
        duration = duration - hours * 3600
        durations.append("%sh" % hours)
    if (duration >= 60):
        mins = int(duration / 60)
        duration = duration - mins
        durations.append("%sm" % mins)
    if (duration):
        durations.append("%ss" % duration)
    return " ".join(durations)
    
def savePNG(surface, filename):
    """ Save a PNG file to disk.
        @param surface:   PyGame Surface object to use for saving image.
        @param filename:  Filename to use for saving image.
    """
    dirName = basename(dirname(filename))
    print "Saving: %s/%s" % (dirName, basename(filename))
    pygame.image.save(surface, filename)
    
def savePPM(surface, filename):
    """ Save a PPM file to disk.
        @param surface:   PyGame Surface object to use for saving image.
        @param filename:  Filename to use for saving image.
    """
    dirName = basename(dirname(filename))
    print "Saving: %s/%s" % (dirName, basename(filename))
    handle = open(filename, 'w')
    # Write the PPM Header
    handle.write("P3\n")
    handle.write("%s %s\n" % (surface.get_width(), surface.get_height()))
    handle.write("255\n\n")
    # Write the pixel information
    for y in xrange(surface.get_height()):
        for x in xrange(surface.get_width()):
            r, g, b = surface.get_at((x, y))[0:3]
            handle.write("%s %s %s  " % (r, g, b))
        handle.write("\n")
    handle.close()

def getLiberationFont(size=10):
    """ Return Liberations Sans font.
        @param size:  Size of the font to return.    
    """
    font = pygame.font.Font(FONTPATH, size)
    return font

