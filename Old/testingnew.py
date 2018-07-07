import pygame
from pygame import *


class Universal(pygame.sprite.Sprite):
    ''' Universal spirte class'''

    def __init__(self, width, height, initialx, initialy, alpha):

        pygame.sprite.Sprite.__init__(self)

        self.height = height
        self.width = width

        self.image = Surface([self.width,self.height])

        self.rect = self.image.get_rect()

        self.image.set_colorkey(alpha)
        self.image.fill((0,0,0))
        
        self.rect.centerx = initialx
        self.rect.centery = initialy


class Player(Universal):

    def __init__(self):

        Universal.__init__(self, 30, 30, 200, 200, (255,255,255))

    def update(self):
        pass

    def move(self):
        pass

class Square(Universal):

    def __init__(self):

        Universal.__init__(self,30,30,200,230,(0,0,0))
        
        self.image.fill((255,160,122))

    def update(self):
        pass
        
                            
all_sprites_list = pygame.sprite.Group()

player = Player()
square = Square()

all_sprites_list.add(player,square)

pygame.init()
        
dimentions = (400,400)

screen = display.set_mode(dimentions)

clock = time.Clock()
screen.fill((255,255,255))



done = False

while not done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RIGHT:
                player.rect.centerx += 4
            if event.key == pygame.K_UP:
                player.rect.centery -= 4
                    
            if event.key == pygame.K_LEFT:
                player.rect.centerx -= 4
            if event.key == pygame.K_DOWN:
                player.rect.centery += 4



    all_sprites_list.draw(screen)
    all_sprites_list.update()
    print player.rect.centerx
    
    display.flip()

    clock.tick(60)
