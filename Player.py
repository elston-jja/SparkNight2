import pygame
import math
from Constants import *

class Player(pygame.sprite.Sprite):

    def __init__(self, playerW, playerH, posX, posY):

        pygame.sprite.Sprite.__init__(self)

        self.width  = playerW
        self.height = playerH

        self.image = pygame.image.load("ImagesAndSounds/pickachu.png").convert()
        self.image = pygame.transform.rotate(self.image, 90)
        self.origImage = self.image

        self.image.set_colorkey(WHITE)
        self.origImage.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.mouseBlocked = False

        self.rect.x = posX
        self.rect.y = posY

        self.Bsmoothing = False
        self.smoothingLoopCap = 40
        
    def calcDisplacement(self):

        displacement = (pygame.mouse.get_pos()[0] - self.rect.centerx, pygame.mouse.get_pos()[1] - self.rect.centery)
        return displacement

    def calcRelDisplacement(self, currentPosition, finalPosition):

        return  finalPosition[0] - currentPosition[0], finalPosition[1] - currentPosition[1]
    
    def angleToMouse(self):

        disp = self.calcDisplacement()

        if (disp[0] == 0):
            disp = math.tau, disp[0], 
        angle = math.degrees(math.atan2(-disp[1],disp[0]))

        if (angle < 0):
            angle += 360

        return(angle)

    
    def handleKeys(self):
        
        click = pygame.mouse.get_pressed()

        if (click[0] == True and self.mouseBlocked == False):
            self.move()
            self.mouseBlocked = True

        if (click[0] == False):
            self.mouseBlocked = False

            
    def move(self):
        
        currPos = self.calcDisplacement()
        self.positionClicked = pygame.mouse.get_pos()
        
        self.rect.centerx += currPos[0]/self.smoothingLoopCap
        self.rect.centery += currPos[1]/self.smoothingLoopCap

        self.Bsmoothing = True
        
        
    def rotSprite(self):
        
        self.image  = pygame.transform.rotate(self.origImage, self.angleToMouse())

        
    def smoothMovement(self):

        ## Remember to call off smoothing with collisions
        
        if (self.Bsmoothing):

            currPos = self.calcRelDisplacement(self.rect, self.positionClicked)
            print (currPos)
            
            self.vx = ( currPos[0] / self.smoothingLoopCap )
            self.vy = ( currPos[1] / self.smoothingLoopCap )

            print ( self.vx, self.vy)

            self.rect.centerx += self.vx
            self.rect.centery += self.vy
            
            if (abs(currPos[1]) < 1 and abs(currPos[0]) < 1):
                self.Bsmoothing = False
                 
        
    def update(self):
        self.handleKeys()
        self.smoothMovement()
        self.rotSprite()
