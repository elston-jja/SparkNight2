'''
Always Face Mouse
'''

import pygame, random, math
from pygame import *

# Goal is to make a level generator

class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.width = 40
		self.height = 40
		self.image = pygame.Surface([self.width,self.height])
		self.image.fill(red)
		self.image.set_colorkey(red)
                pygame.draw.rect(self.image,white,[0,0,self.width,self.height])
                self.rect = self.image.get_rect()
                self.angle = 0

        def update(self):
                self.rotate = 

pygame.init()

width = 300
height = 300

bg = (0,0,0)
white = (255,255,255)
red = (255,0,0)

screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("testing mouse and player")

all_sprites_list = pygame.sprite.Group()

player = Player()

all_sprites_list.add(player)

clock = pygame.time.Clock()

done = False

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        screen.fill(bg)

        

        pos = pygame.mouse.get_pos()

        #print (pos)

        Player.angle, mouse_angle = 360-math.atan2(pos[1]-300,pos[0]-300)*180/math.pi

        all_sprites_list.update()

        all_sprites_list.draw(screen)

        clock.tick(60)

        pygame.display.flip()

pygame.quit()
