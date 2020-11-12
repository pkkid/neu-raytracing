#!/usr/bin/python2.4
"""
Various callback functions for coloring objects
Created by M.Shepanski
"""

import color
import math
import pygame
import random

RANDOM_SIZE  = 39
TEXTURE_SIZE = (200, 200)
RED   = 0
GREEN = 1
BLUE  = 2


###############################
#  Texture Base Class
###############################

class Texture:
    """ Base Class for all Textures. """
    
    def getColor(self, vec):
        """ Return the color at the specified vector. """
        raise Exception("Function not defined: getColor()")
    

###############################
#  Checkerboard Texture
###############################

class CheckerBoard(Texture):
    """ Checkerboard Color. """
    OFFSET = (10000, 10000)
    
    def __init__(self, color1, color2, sqSize, resolution):
        self.resolution = resolution   # Texture Width & Height (for mapping)
        self._color1  = color1         # First color in Checkerboard
        self._color2  = color2         # Second color in Checkerboard
        self._sqSize  = sqSize         # Half width (for math)
        
    def getColor(self, pos):
        """ Return the color. """
        # We add 10,000 to avoid seeing duplicate colors at the origin.
        if (((((pos[0] + CheckerBoard.OFFSET[0]) % (self._sqSize*2)) < self._sqSize and
              ((pos[1] + CheckerBoard.OFFSET[1]) % (self._sqSize*2)) < self._sqSize)) or
            ((((pos[0] + CheckerBoard.OFFSET[0]) % (self._sqSize*2)) >= self._sqSize and
              ((pos[1] + CheckerBoard.OFFSET[1]) % (self._sqSize*2)) >= self._sqSize))):
            return self._color1
        return self._color2
    
    
###############################
#  Image Texture
###############################

class Image(Texture):
    """ Image. """
    
    def __init__(self, imagePath, scale=1.0):
        self._image = pygame.image.load(imagePath)        # Image to Map this texture to
        self.scale  = scale                               # Amount to scale the image
        self.resolution = (self._image.get_width(), self._image.get_height())
        
    def getColor(self, pos):
        """ Return the color. """
        xPos = pos[0] % (self.resolution[0] * (1 / self.scale))
        yPos = pos[1] % (self.resolution[1] * (1 / self.scale))
        return self._image.get_at((xPos, yPos))
    
    
###############################
#  Perlin Texture
###############################
    
class Perlin(Texture):
    """ Some Perlin Noise Up in 'Da House. """
    OFFSET = (10000, 10000)
    
    def __init__(self, textureName):
        self.textureName = textureName         # Texture Name to Render
        self.resolution = (100000, 100000)     # Resolution (Really big, never repeat)
        # Perlin Stuff
        self.noise   = self._renderNoise()     # Noise Array of Random Integers
        self.divisor = 100                     # Divisor used to Spread out Noise
        
    def getColor(self, pos):
        """ Return the color at the specified position. """
        x = (pos[0] + Perlin.OFFSET[0]) / self.divisor
        y = (pos[1] + Perlin.OFFSET[1]) / self.divisor
        # Render the correct Texture
        if   (self.textureName == 'clouds'):     colorPoint = self._renderClouds(x, y)
        elif (self.textureName == 'marble'):     colorPoint = self._randerMarble(x, y)
        elif (self.textureName == 'spruce'):     colorPoint = self._renderSpruce(x, y)
        elif (self.textureName == 'radiation'):  colorPoint = self._renderRadiation(x, y)
        elif (self.textureName == 'stucco'):     colorPoint = self._renderStucco(x, y)
        elif (self.textureName == 'water'):      colorPoint = self._renderCrappyWater(x, y)
        elif (self.textureName == 'leaves'):     colorPoint = self._renderLeaves(x, y)
        else:  raise Exception("Unknown texture: %s" % self.textureName)
        return colorPoint
    
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
        self.divisor = 100
        spinnyness = 3
        turbulance = self._getLinearTurbulance(x, y, RED) / 255.0
        factor = math.sqrt((x - 200.0 / self.divisor) * (x - 200.0 / self.divisor)
                         + (y - 200.0 / self.divisor) * (y - 200.0 / self.divisor))
        factor = abs(math.cos(factor + spinnyness * turbulance))
        color1 = (23, 51, 112)    # Dark Blue
        color2 = (172, 196, 182)  # Light Green
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
        noise = pygame.Surface((RANDOM_SIZE+1, RANDOM_SIZE+1))
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
    
    
########################
#  Testing
########################
if (__name__ == "__main__"):
    myChecker = CheckerBoard((0, 0, 0), (1, 1, 1), 50, (100, 100))
    print myChecker.getColor((1, 10))
    print myChecker.getColor((51, 10))
    print myChecker.getColor((101, 10))
    print myChecker.getColor((151, 10))
    print myChecker.getColor((201, 10))
    
