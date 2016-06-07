'''
Elston Almeida
Levels
ICS 3U1
'''

# Sources http://stackoverflow.com/questions/14700889/pygame-level-menu-states

import pygame
from pygame import *
from map1 import maps

class gamescene():

    def __init__(self):
        level = 0
        self.wall_list = pygame.sprite.Group()
        x = 0
        y = 0
        list_of_maps = maps()
        level = list_of_maps.map_0
        for row in level:
            for col in row:
                if col == "P":
                    p = Wall(x,y)
                    self.wall_list.add(p)
                    all_sprites_list.add(p)
                if col == "E":
                    e = Wall(x,y)
                    self.wall_list.add(e)
                    all_sprites_list.add(e)
                x+= 32
            y+=32
            x = 0
                        
class Wall(pygame.sprite.Sprite):

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([30,30])
        self.image.convert()
        self.rect = self.image.get_rect()
        
        self.image.fill(red)
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        pass
    


pygame.init()

# dimentions of screen
#width = 1440
#height = 900

width = 1440
height = 900

# COLORS 
bg = (0,0,0)
white = (255,255,255)
red = (220,100,100)
green = (0,255,0)


# Screen
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("Level Example")

# Create sprite group
all_sprites_list = pygame.sprite.Group()

manager = gamescene()

# Create object player
#player = Player()

# Adds player to sprites list
#all_sprites_list.add(player)

# Game time for clock functions
clock = pygame.time.Clock()

# Fill background (Makes cicle, when loop screen.fill is commented)
#screen.fill(bg)

# LOOP
done = False

while not done:
            # Quit pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Call update function of sprites
        all_sprites_list.update()

        # fills background color
        screen.fill(bg)
        
        # Draw all sprites on screen
        all_sprites_list.draw(screen)

        # Set tick rate to 60
        clock.tick(60)

        # Redraw screen
        pygame.display.flip()

# Quit if loop is exited
pygame.quit()

