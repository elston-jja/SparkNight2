import pygame
import math
from Constants import *

class Player(pygame.sprite.Sprite):

    def __init__(self, playerW, playerH, posX, posY):

        pygame.sprite.Sprite.__init__(self)

        self.width  = playerW
        self.height = playerH

        self.image = pygame.image.load("ImagesAndSounds/pickachu.png").convert()
        self.origImage = self.image

        self.image.set_colorkey(WHITE)
        self.origImage.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.rect.x = posX
        self.rect.y = posY

        self.vx = 0
        self.vy = 0

        self.ax = 3
        self.ay = 3
        

    def calcDisplacement(self):

        displacement = pygame.mouse.get_pos()[0] - self.rect.centerx, pygame.mouse.get_pos()[1] - self.rect.centery
        return displacement
        
    def angleToMouse(self):

        disp = self.calcDisplacement()
        if (disp[1] == 0):
            disp = disp[0], math.tau
        angle = math.atan(disp[0]/disp[1])
        return math.degrees(angle)

    def move(self):
        
        currPos = self.calcDisplacement()
        
        
        
    
    def rotSprite(self):
        
        self.image  = pygame.transform.rotate(self.origImage, self.angleToMouse())
        self.rect   = self.image.get_rect()
           
    def update(self):
        
        self.rotSprite()
        
