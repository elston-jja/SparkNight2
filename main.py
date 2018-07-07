#!/usr/bin/python

import pygame
from Game import Game
from Constants import *

game  = Game(WIDTH, HEIGHT, 0, "test")

game.createPlayer(PLAYER_W, PLAYER_H, 150, 150)


while( game.isRunning() ):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    game.update()
    game.render()
    
