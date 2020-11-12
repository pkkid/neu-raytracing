#!/usr/bin/python2.4
"""
Assignment:  #1 World of Spheres
Class:       CSG140 - Computer Graphics
Author:      Michael Shepanski
"""
import math
import os
import pygame
import random
from graphics import color
from graphics import pygametools
from optparse import OptionParser
from os.path import abspath
from os.path import dirname
from pygame.surface import Surface


ASSIGNMENT   = 4
WINDOWTITLE  = "Assignment #%s - M. Shepanski" % ASSIGNMENT
FAVICON      = "%s/graphics/resources/favicon.gif" % dirname(abspath(__file__))
FONTCOLOR    = (128, 128, 128)
FOOTERHEIGHT = 43
RANDOM_SIZE  = 39
TEXTURE_SIZE = (200, 200)


RED   = 0
GREEN = 1
BLUE  = 2


class PerlinNoise:
    """ Assignment 1 - World of Spheres """

    def __init__(self, textureName):
        # PyGame Window Settings
        self.resolution = None                                 # Screen Resolution
        self.screen     = None                                 # Main PyGame Screen 
        self.running    = True                                 # Set False to quit the Application
        # Perlin Noise Settings
        self.textureName = textureName                         # Texture Name
        self.noise       = self._renderNoise()                 # Noise Array of Random Integers
        self.divisor     = 100                                 # Divisor used to Spread out Noise
        self.texture     = self._getTexture(textureName)       # Texture to produce
        # Lets go do Stuff!! :)
        self._initPyGame()                                     # Init basic PyGame settings

    def _initPyGame(self):
        """ Initialize the PyGame window. """
        icon = pygame.image.load(FAVICON)
        pygame.display.init()
        pygame.display.set_caption(WINDOWTITLE)
        pygame.display.set_icon(icon)
        # Find the Screen resolution (with footer)
        self.resolution = (600, 400 + FOOTERHEIGHT)
        self.screen = pygame.display.set_mode(self.resolution)

    def run(self):
        """ Run the Program. """
        clock = pygame.time.Clock()
        #self.scene.renderScene(self.screen)
        self._flipScreen()
        while (self.running):
            self._processEvents()
            clock.tick(10)

    def _getTexture(self, textureName):
        """ Return a texture surface from the texture name. """
        surface = Surface(TEXTURE_SIZE)
        self.divisor = 32
        for v in range(0, TEXTURE_SIZE[0]):
            for h in range(0, TEXTURE_SIZE[1]):
                x = float(h) / self.divisor
                y = float(v) / self.divisor
                # Render the correct Texture
                if   (textureName == 'clouds'):     colorPoint = self._renderClouds(x, y)
                elif (textureName == 'marble'):     colorPoint = self._randerMarble(x, y)
                elif (textureName == 'spruce'):     colorPoint = self._randerSpruce(x, y)
                elif (textureName == 'radiation'):  colorPoint = self._renderRadiation(x, y)
                elif (textureName == 'stucco'):     colorPoint = self._renderStucco(x, y)
                elif (textureName == 'water'):      colorPoint = self._renderCrappyWater(x, y)
                elif (textureName == 'leaves'):     colorPoint = self._renderLeaves(x, y)
                else:  raise Exception("Unknown texture: %s" % textureName)
                # Paint the Canvas
                surface.set_at((h, v), colorPoint)
        return surface
    
    #################################
    #  Defined Textures
    #################################
    
    def _renderLeaves(self, x, y):
        self.divisor = 20
        turbulance = self._getLinearTurbulance(x, y, RED) / 255.0
        factor = abs(math.sin(x + turbulance * 80))
        color1 = (20, 132, 19)
        color2 = (24, 53, 24)
        return self._calcFactorColor(color1, color2, factor)
    
    def _renderCrappyWater(self, x, y):
        """ Generate some Marble. """
        self.divisor = 50
        spinnyness = 3
        turbulance = self._getLinearTurbulance(x, y, RED) / 255.0
        factor = math.sqrt((x - 200.0 / self.divisor) * (x - 200.0 / self.divisor)
                         + (y - 200.0 / self.divisor) * (y - 200.0 / self.divisor))
        factor = abs(math.cos(factor + spinnyness * turbulance))
        color1 = (23, 51, 112)    # Dark Blue
        color2 = (172, 196, 182)  # Light Green
        #if (factor < 0.6):
        #    color1 = (23, 90, 112)
        #    return self._calcFactorColor(color1, color2, factor)
        return self._calcFactorColor(color1, color2, factor)
    
    def _renderStucco(self, x, y):
        """ Test bed for making new textures. """
        self.divisor = 20
        turbulance = self._getLinearTurbulance(x, y, RED) / 255.0
        factor = abs(math.sin(x + turbulance * 10))
        color1 = (184, 145, 102)
        color2 = (116, 109, 91)
        if (factor > 0.3):
            color3 = (155, 130, 96)
            return random.choice((color1, color3))
        else:
            return self._calcFactorColor(color1, color2, factor)
    
    def _renderClouds(self, x, y):
        """ Generate some Stucco. """
        self.divisor = 75
        factor = self._getLinearTurbulance(x, y, RED) / 255.0
        return self._calcFactorColor((50, 50, 255), color.WHITE, factor)
        
    def _renderSpruce(self, x, y):
        """ Test bed for making new textures. """
        self.divisor = 20
        turbulance = self._getLinearTurbulance(x, y, RED) / 255.0
        factor = abs(math.sin(x + turbulance * 10))
        return self._calcFactorColor(color.WHITE, (190, 178, 159), factor)
    
    def _randerMarble(self, x, y):
        """ Generate some Marble. """
        self.divisor = 20
        turbulance = self._getLinearTurbulance(x, y, RED) / 255.0
        factor = abs(math.sin(x + turbulance * 3))
        return self._calcFactorColor((58, 50, 37), (107, 93, 69), factor)
    
    def _renderRadiation(self, x, y):
        """ Some Radioactive Material. """
        self.divisor = 50
        radioactivness = 10
        turbulance = self._getLinearTurbulance(x, y, RED) / 255.0
        factor = math.sqrt((x - 200.0 / self.divisor) * (x - 200.0 / self.divisor)
                             + (y - 200.0 / self.divisor) * (y - 200.0 / self.divisor))
        factor = abs(math.cos(factor + radioactivness * turbulance))
        return self._calcFactorColor((120, 207, 12), (255, 218, 0), factor)
        
    #################################
    #  Perlin Noise Stuff
    #################################

    def _renderNoise(self):
        """ Generate a Random square of noise. """
        noise = Surface((RANDOM_SIZE+1, RANDOM_SIZE+1))
        for i in range(0, RANDOM_SIZE):
            for j in range(RANDOM_SIZE):
                red   = random.randint(0, 255)
                green = random.randint(0, 255)
                blue  = random.randint(0, 255)
                noise.set_at((i, j), (red, green, blue))
        # Set the last row and column to match the first row and column
        for i in range(0, RANDOM_SIZE):
            noise.set_at((RANDOM_SIZE, i), noise.get_at((0, i)))
            noise.set_at((i, RANDOM_SIZE), noise.get_at((i, 0)))
        # Set the last corner to complete the wrap
        noise.set_at((RANDOM_SIZE, RANDOM_SIZE), noise.get_at((0, 0)))
        return noise

    def _getLinearTurbulance(self, u, v, channel):
        """ Return a Turbulance color (between 0 and 1) """
        t = 0.0
        scale = 1.0
        count = 0
        while (scale >= (1.0 / self.divisor)):
            uScale = float(u) / scale
            vScale = float(v) / scale
            t += self._getLinearNoise(uScale, vScale, channel) * scale
            scale /= 2
            count += 1
            if (self.textureName == 'water') and (count == 2):
                return t
        return t / 2
    
    def _getLinearNoise(self, u, v, channel):
        """ Return a linear Noise Color. """
        iu = int(u)              # Integer part of U
        iv = int(v)              # Integer part of V               (iu,iq)-----(ip,iq)
        du = float(u) - iu       # Fractional part of U               |     |     |
        dv = float(v) - iv       # Fractional part of V               |     *     |
        iu = iu % RANDOM_SIZE    # Intergral part of U & V..          |     |     |
        iv = iv % RANDOM_SIZE    # ..mapped to ints 0 to size-1    (iu,iv)-----(ip,iv)
        ip = (iu + 1)            # (ip, iu) lattice point 
        iq = (iv + 1)            # ...
        # Top gets noise from linear function across the top of the square
        # Bot gets noise from linear function across the bottom of the square
        # Go a distance du along the top and bottom of the square
        chanBL = self.noise.get_at((iu, iv))[channel]
        chanBR = self.noise.get_at((ip, iv))[channel]
        chanTL = self.noise.get_at((iu, iq))[channel]
        chanTR = self.noise.get_at((ip, iq))[channel]
        chanB  = chanBL + du * (chanBR - chanBL)
        chanT  = chanTL + du * (chanTR - chanTL)
        return   chanB  + dv * (chanT  - chanB)
    
    def _calcFactorColor(self, color1, color2, factor):
        """ Given 2 colors anda factor, return the color in between. """
        colorR = ((color1[0] - color2[0]) * factor) + color2[0]
        colorG = ((color1[1] - color2[1]) * factor) + color2[1]
        colorB = ((color1[2] - color2[2]) * factor) + color2[2]
        return (colorR, colorG, colorB)

    #################################
    #  PyGame Rendering Functions
    #################################

    def _flipScreen(self):
        """ Flip the image (Update the screen).
            @param statPos:  Current mouse (x,y) position.
        """
        self.screen.fill((0, 0, 0))                     # Clear the Screen
        self.screen.blit(self.noise, (10, 10))          # Draw the Random Noise
        self.screen.blit(self.texture, (120, 10))       # Draw the Main Texture
        self._renderFooter(self.screen)                 # Draw the Footer info
        pygame.display.flip()                           # Send it all out

    def _renderFooter(self, surface):
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

    def _renderSignature(self, surface):
        """ Render Signature to Lower Right on specified surface.
            @param surface:  PyGame Surface object to render the signature onto.
        """
        # Create the message to display    
        message  = "Michael Shepanski\n"
        message += "Assignment #%s - CSG140\n" % ASSIGNMENT
        # Render the Message
        xPos, yPos = surface.get_width()-5, surface.get_height()-3
        for msgline in reversed(message.split('\n')):
            text = pygametools.FONTTINY.render(msgline, True, FONTCOLOR)
            rect = text.get_rect()
            rect.bottomright = xPos, yPos
            yPos = yPos - 12
            surface.blit(text, rect)
            
    def _processEvents(self):
        """ Check any window events. """
        for event in reversed(pygame.event.get()):
            if (event.type == pygame.QUIT):
                self.running = False


###############################
#  Command Line Interface
###############################

if (__name__ == "__main__"):
    parser = OptionParser()
    parser.add_option("-t", "--texture",  default="stucco", help="Texture to produce: {stucco, bark, wood, clouds, water}")
    options, args = parser.parse_args()
    PerlinNoise(options.texture).run()

