#!/usr/bin/python2.4
"""
Represents a 3D Scene.
Created by M.Shepanski
"""

import color
import os
import pygametools
import time
from pygame.surface import Surface
from light import Light
from sphere import Sphere
from vector import Vector


class Scene:
    """ Represents a 3D Scene. """
    
    def __init__(self, name=None):
        self.resolution = (600, 400)              # Resolution of the drawing canvas
        self.viewPoint = Vector(300, 200, 1000)   # View Point (location of out eye)
        # Items in the Scene 
        self.lights  = []                         # List of lights in our scene
        self.objects = []                         # List of objects in our scene
        self.ka = 0.0                             # Ambient light coefficient
        # Resources for on-screen rendering
        self.name = name or "3D Scene"            # Optional name for this scene
        self.image = Surface(self.resolution)     # PyGame Surface to render Window
        self.coordinfo = {}                       # (x,y) => Coordinate Information
        self.pointsRendered = 0                   # Number of points currently rendered
        self.duration = None                      # Seconds it took to render the image
    
    def __str__(self):
        """ String representation for this scene. """
        rtn  = "%-15s  %s\n" % ("Scene Name:",    self.name)
        rtn += "%-15s  %s\n" % ("Resolution:",    self.resolution)
        rtn += "%-15s  %s\n" % ("View Point:",    self.viewPoint)
        rtn += "%-15s  %s\n" % ("Ambient Light:", self.ka)
        for light in self.lights:
            rtn += "%-15s  %s\n" % ("Light Source:", light)
        for obj in self.objects:
            rtn += "\n%s" % obj
        return rtn
        
    def renderScene(self, surface):
        """ Render this scene onto self.image.
            @param surface: Surface to use when rendering Loading message.
        """
        # Draw the "Loading.." message; Init Variables
        pygametools.flipLoadingMessage(surface, 0, 0)
        totalPoints = float(self.resolution[0] * self.resolution[1])
        starttime = time.time()
        # Render the Scene
        percentComplete = 0
        self.pointsRendered = 0
        for y in xrange(self.resolution[1]):
            for x in xrange(self.resolution[0]):
                self.pointsRendered += 1
                colorxy = self.get_at((x, y))
                if (colorxy): self.image.set_at((x, y), colorxy)
                # Update the Percent Complete (only when changed)
                percent = int((self.pointsRendered / totalPoints) * 100)
                if (percentComplete != percent):
                    percentComplete = percent
                    self.duration = time.time() - starttime
                    pygametools.flipLoadingMessage(surface, percent, self.duration)
        return self.image
        
    def get_at(self, pos):
        """ Return the color at the specified point.
            @param pos: (x,y) Position in the window to return the color of.
        """
        obj, vec = self.getVisibleObject(pos)
        if (obj):
            # Update coordinfo (for footer); And return object's color
            objName = obj.__class__.__name__
            simpVec = tuple(map(int, vec.val()))
            self.coordinfo[pos] = "%s: %s" % (objName, simpVec)
            return obj.get_at(self, vec)
        else:
            # TODO: This should be removed, its a fake BG for prog1
            vec = Vector(pos[0], pos[1], 0)
            bgColor = (255, 255, 255)
            bgkd = 0.7
            colorPoint = color.mul(bgColor, self.ka)
            for light in self.lights:
                normLight  = (light.center - vec).normalize()
                isShadow   = self.isShadow(vec, light)
                # Calculate the color from Lamberts Diffuse Algorithm
                kd = [bgkd, bgkd * 0.3][isShadow]
                factorLambert = max(Vector(0, 0, 1) * normLight, 0)
                colorLambert = color.mul(bgColor, factorLambert)
                colorLambert = color.mul(colorLambert, kd)
                colorPoint = color.add(colorPoint, colorLambert)
            return colorPoint
        return None
    
    def getVisibleObject(self, pos):
        """ Return the Object and Vector (Point of intersection) we see when
            looking at point x, y on our drawing canvas.
            @param pos: (x,y) Position in the window to return the color of.
        """
        minObj = None      # Closest object to View Point
        minVec = None      # Interect position of Ray from View Point to x,y
        minT = None        # Distance between View Point and minPos
        for obj in self.objects:
            vec, t = obj.intersect(self.viewPoint, Vector(pos[0], pos[1], 0))
            if (vec):
                if (not minT) or (t < minT):
                    minObj = obj
                    minVec = vec
                    minT = t
        return minObj, minVec
    
    def isShadow(self, vec, light, ignore=None):
        """ Return True if the vector location is in a shadow of the specified light.
            @param vec:     (x,y,z) Vector to check is in a shadow of the specified light.
            @param light:   Light object to use when checking for a shadow.
            @param ignore:  Any object in this scene we should ignore when checking for shadows.
        """
        for obj in self.objects:
            if ((ignore) and (obj != ignore)) or (not ignore):
                hit, t = obj.intersect(light.center, vec)
                if (hit) and (t > 0) and (t < 1):
                    return True
        return False
        
    @staticmethod
    def createFromFile(sceneFile):
        """ Create a new Scene object from a file.
            @param sceneFile:  Scene filename (without .py) to open and create Scene object from.
        """
        scenePath = Scene.locateSceneFilePath(sceneFile)
        print "Importing scene file: %s" % scenePath
        exec(file(scenePath, 'r').read())
        scene = Scene(os.path.basename(scenePath))
        for name, value in SceneParams:
            if   (name.lower() == 'resolution'):    scene.resolution = value
            elif (name.lower() == 'ambientlight'):  scene.ka = value
            elif (name.lower() == 'viewpoint'):     scene.viewPoint = value
            elif (name.lower() == 'light'):         scene.lights.append(value)
            elif (name.lower() == 'object'):        scene.objects.append(value)
            else: raise Exception('Unknown scene parameter: %s' % name)
        return scene
        
    @staticmethod
    def locateSceneFilePath(sceneFile):
        """ Will try several variations of sceneFile to find the correct one. """
        sceneDir = "%s/scenes" % os.path.dirname(os.path.dirname(__file__))
        filesToCheck = []
        filesToCheck.append(sceneFile)
        filesToCheck.append("%s.scene" % sceneFile)
        filesToCheck.append("%s/%s" % (sceneDir, sceneFile))
        filesToCheck.append("%s/%s.scene" % (sceneDir, sceneFile))
        for filePath in filesToCheck:
            if (os.path.exists(filePath)):
                return filePath
        raise Exception('Unable to locate scene file: %s' % sceneFile)
    
    