'''
Elston Almeida
Levels
ICS 3U1
'''

# Sources http://stackoverflow.com/questions/14700889/pygame-level-menu-states

import pygame
from pygame import *

class gamescene:

    if level == 0:
        level = [
            ""                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                            ",
            "                                         E  ",
            "                            PPPPPPPPPPPPPPPP",
            "                            PPPPPPPPPPPPPPPP",
            "                            PPPPPPPPPPPPPPPP",
            "               PPPPP        PPPPPPPPPPPPPPPP",
            "                            PPPPPPPPPPPPPPPP",
            "                            PPPP           P",
            "                            PPPP           P",
            "                            PPPP     PPPPPPP",
            "                      PPPPPPPPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "       PPPP                 PPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "                            PPPP     PPPPPPP",
            "PPPPP                       PPPP     PPPPPPP",
            "PPP                         PPPP     PPPPPPP",
            "PPP                         PPPP     PPPPPPP",
            "PPP                         PPPP     PPPPPPP",
            "PPP         PPPPP           PPPP     PPPPPPP",
            "PPP                                     PPPP",
            "PPP                                     PPPP",
            "PPP                                     PPPP",
            "PPP                       PPPPPPPPPPPPPPPPPP",
            "PPP                       PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",
            "PPPPPPPPPPPPPPP           PPPPPPPPPPPPPPPPPP",]


pygame.init()

# dimentions of screen
width = 1440
height = 900

# COLORS 
bg = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

# Screen
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("Level Example")

# Create sprite group
all_sprites_list = pygame.sprite.Group()

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

