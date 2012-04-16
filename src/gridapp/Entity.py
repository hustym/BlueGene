# coding: utf-8
#!/usr/bin/python

import GlobalTimer

class Entity(object):
    def __init__(self):
        self.databaseID = 0
        self.id = id(self)
        self.isDestroyed = False

        self.allClients = []
        self.canBeSeen = True
        self.client = None
        self.hasWitness = False
        self.isWitnessed = False
        self.otherClients = []
        self.position = 0, 0
        self.spaceID = 0
        self.topSpeed = 0.0
        self.global_timer = GlobalTimer.global_timer

    #base

    def addTimer(self, initial_offset, repeat_offset=0, user_data=0):
        return self.global_timer.addTimer(initial_offset, self.onTimer, repeat_offset, user_data)

    def delTimer(self, id):
        self.global_timer.delTimer(id)

    def onTimer(self, timer_id, user_data):
        pass

    def destroy(self):
        pass

    def writeToDB(self, callback):
        pass

    def onWriteToDB(self):
        pass


    # cell
    def accelerateAlongPath(self, waypoints, acceleration, maxSpeed, facing, userData):
        pass

    def accelerateToEntity( self, destinationEntity, acceleration, maxSpeed, range, facing, userData ):
        pass

    def accelerateToPoint( self, destination, acceleration, maxSpeed, facing, userData ):
        pass

    def addProximity( self, range, userData ):
        pass

    def cancel( self, controllerID ):
        pass

    def debug( self ):
        pass

    def entitiesInRange( self, range, entityType=None, position=None ):
        pass

    def getStopPoint( self, destination, ignoreFirstStopPoint, maxDistance, girth, stopDist, nearPortalDist ):
        pass

    def moveToEntity( self, destEntityID, velocity, range, userData, faceMovement, moveVertically ):
        pass

    def moveToPoint( self, destination, velocity, userData, faceMovement, moveVertically ):
        pass

    def navigate( self, destination, velocity, faceMovement, maxDistance, girth, closeEnough, userData ):
        pass

    def navigateFollow( self, destEntity, angle, distance, velocity, maxDistance, maxSearchDistance, faceMovement, girth, userData ):
        pass

    def navigateStep( self, destination, velocity, maxMoveDistance, maxDistance, faceMovement, girth, userData ):
        pass

    def setAoIRadius( self, radius, hyst=5 ):
        pass

    def teleport( self, nearbyMBRef, position, direction ):
        pass

    def onDestroy( self ):
        pass

    def onEnterTrap( self, entity, range, controllerID ):
        pass

    def onEnteredAoI( self, entity ):
        pass

    def onLeaveTrap( self, entity, range, controllerID ):
        pass

    def onLoseControlledBy( self, id ):
        pass

    def onMove( self, controllerID, userData ):
        pass

    def onMoveFailure( self, controllerID, userData ):
        pass

    def onNavigate( self, controllerID, userData ):
        pass

    def onNavigateFailed( self, controllerID, userData ):
        pass

    def onStartSeeing( self, entity, userData ):
        pass

    def onStopSeeing( self, entity, userData ):
        pass

    def onTeleportFailure( self ):
        pass

    def onWitnessed( self, isWitnessed ):
        pass


