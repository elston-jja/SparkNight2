import pygame
from Constants import *

class Player(pygame.sprite.Sprite):

    def __init__(self, playerW, playerH, posX, posY):

        pygame.sprite.Sprite.__init__(self)

        self.width  = playerW
        self.height = playerH

        self.image = pygame.image.load("ImagesAndSounds/pickachu.png").convert()

        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.rect.x = posX
        self.rect.y = posY
        
        
    def update(self):
        pass
