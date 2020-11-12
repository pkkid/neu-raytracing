#!/usr/bin/python2.4
"""
Represents a 3D Scene.
Created by M.Shepanski
"""

import color
import os
import pygametools
import time
import texture
from pygame.surface import Surface
from vector import Vector

# World Objects
from light import Light
from plane import Plane
from sphere import Sphere


class Scene:
    """ Represents a 3D Scene. """
    
    def __init__(self, name=None):
        self.resolution = (600, 400)              # Resolution of the drawing canvas
        self.viewPoint = Vector(300, 200, 1000)   # View Point (location of out eye)
        self.logging = False                      # Set True to enable logging
        # Items in the Scene 
        self.lights  = []                         # List of lights in our scene
        self.objects = []                         # List of objects in our scene
        self.ka = 0.0                             # Ambient light coefficient
        self.ni = 1.0                             # Index of Refraction for the Scene (Air)
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
        
    def log(self, msg):
        """ Log a message to the screen. """
        if (self.logging):
            print msg
    
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
            @param viewPoint:  Current viewpoint we're looking at this object from.
        """
        try:
            rayPoint = Vector(pos[0], pos[1], 0)
            obj, vec = self.getVisibleObject(self.viewPoint, rayPoint)
            if (obj):
                # Update coordinate information
                objName = obj.__class__.__name__
                simpVec = tuple(map(int, vec.val()))
                self.coordinfo[pos] = "%s: %s" % (objName, simpVec)
                # Get the color for the specified point
                return obj.getColorFromRay(self, vec, self.viewPoint)
            return None
        except:
            print "Error getting color for point: %s" % str(pos)
            raise
    
    def getVisibleObject(self, viewPoint, rayPoint, ignore=None):
        """ Return the Object and Vector (Point of intersection) we see when
            looking at point x, y on our drawing canvas.
            @param viewPoint:  Current viewpoint we're looking at this object from.
            @param rayPoint:   (x,y,z) Of a point on the ray from the viewPoint
            @param ignore:  Any object in this scene we should ignore when checking for shadows.
        """
        minObj = None      # Closest object to View Point
        minVec = None      # Interect position of Ray from View Point to x,y
        minT = None        # Distance between View Point and minPos
        for obj in self.objects:
            if ((ignore) and (obj != ignore)) or (not ignore):
                vec, t = obj.intersect(viewPoint, rayPoint)[0]
                if (vec) and ((not minT) or (t < minT)) and (t > 0):
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
                hit, t = obj.intersect(light.center, vec)[0]
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
    
    