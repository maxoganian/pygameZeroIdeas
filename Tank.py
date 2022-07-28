import math
import time

from pgzero.actor import Actor

def deg2rad(deg):
    return deg * (math.pi/180.0)

class Obj(Actor):

    """
    Common class for all objects that move on the screen
    """
    def __init__(self, image, pos):
        Actor.__init__(self, image, pos)

        self.speed = 0.0 # pixels / draw

        #self.updateVelocity()

    def updateVelocity(self):
        "determine velocity vector"
        self.vx = math.cos(deg2rad(self.angle)) * self.speed  
        self.vy = -math.sin(deg2rad(self.angle)) * self.speed

    def update(self):
        "update our position according to the velocity vector"
        self.updateVelocity()

        self.x += self.vx
        self.y += self.vy

class Bullet(Obj):

    def __init__(self, image, pos, tankId):
        Obj.__init__(self, image, pos)

        self.tankId = tankId
        self.speed = 3.0

class Rock(Obj):

    def __init__(self, image, pos):
        Obj.__init__(self, image, pos)

        self.speed = 10.0
        self.age = 0
        self.oldAge = 25

    def update(self):
        Obj.update(self)
        self.age += 1

    def isOld(self):
        return self.age > self.oldAge

class Tank(Obj):

    def __init__(self, image, pos, screenWidth, screenHeight, id):
        Obj.__init__(self, image, pos)

        self.id = id
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight


        self.speed = 0.0
        self.angle = 0
        self.updateGunPosition()

        self.lastTimeShot = None # secs
        self.secondsPerShot = 1 # secs

    def updateGunPosition(self):
        "This is where the bullets fire from"    

        bulletOffset = 10
        offset = (self.width / 2) + bulletOffset
        offsetX = math.cos(deg2rad(self.angle)) * offset  
        offsetY = -math.sin(deg2rad(self.angle)) * offset

        self.gunX = self.x + offsetX
        self.gunY = self.y + offsetY

    def moveForward(self):
        self.speed = 1.0
        self.updateGunPosition()

    def moveBackward(self):
        self.speed = -1.0
        self.updateGunPosition()

    def stop(self):
        self.speed = 0    

    def rotateCW(self):
        self.angle -= 1
        self.updateGunPosition()

    def rotateCCW(self):
        self.angle += 1
        self.updateGunPosition()

    def bounceOff(self, obj):
        "We have collided with an object and need to bounce off it"

        pos = (obj.x, obj.y)
        angleToObj = self.angle_to(pos)

        # displace our position by the vector to this angle
        offset = 10.
        offsetX = math.cos(deg2rad(angleToObj)) * offset  
        offsetY = -math.sin(deg2rad(angleToObj)) * offset       

        self.x -= offsetX
        self.y -= offsetY

    def canShoot(self):
        if self.lastTimeShot is None:
            # first shot!
            self.lastTimeShot = time.time()
            return True
        else:
            if time.time() - self.lastTimeShot > self.secondsPerShot:
                self.lastTimeShot = time.time()
                return True

    def update(self):
        Obj.update(self)

        # keep tank on screen
        if self.x < 0:
            self.x = 1
        if self.x > self.screenWidth:
            self.x = self.screenWidth - 1
        if self.y < 0:
            self.y = 1
        if self.y > self.screenHeight:
            self.y = self.screenHeight - 1    