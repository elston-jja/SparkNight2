'''
Elston Almeida
Levels
ICS 3U1
'''

# Sources http://stackoverflow.com/questions/14700889/pygame-level-menu-states

import pygame
from pygame import *
from map_list import maps

class Level:

    def __init__(self):
        # State the initial level number
        # Value not needed except for verbosity
        self.level = 1
        # Default x y starting block cordinates
        x = 0
        y = 0
        # Creates object called "list of maps" and I can call all maps
        # From the lists in the maps_list file
        list_of_maps = maps()
        # Get the level from maps_list and load it into the interpreter
        # Change the current level to the list varible in the maps_list file
        self.current_level = list_of_maps.map_1
        # Get the lines/rows from each variable in the list
        for line_row in self.current_level:
            # Check each character in the row
            for char in line_row:
                # if the character is a 'w' then add a wall block (30,30)
                if char == "w":
                    wall = Wall(x,y)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                # If the character is an 'e' then add an wall block
                # That when collided can cause to exit
                # As it is added to the exitdoor list (change var is need be)
                if char == "e":
                    exit_ = Wall(x,y)
                    wall_list.add(exit_)
                    exit_doors_list.add(exit_)
                    all_sprites_list.add(exit_)
                    # When drawing each block
                    # (Character in row)
                    # Move 30px to the right
                x+= 30
                # When moving down to next row change the Y by 30
                # Reset the X
            y+=30
            x = 0
                        
class Wall(pygame.sprite.Sprite):

    def __init__(self,x,y):

        # Base sprite class with collisions
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
exit_doors_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

draw_current_level = Level()

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

