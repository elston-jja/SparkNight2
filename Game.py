import pygame
from Player import *

class Game():

    def __init__(self, width, height, fullscreen, caption):

        pygame.init()

        self.screen   = pygame.display.set_mode([width,height], fullscreen)

        self.clock    = pygame.time.Clock()
        
        pygame.display.set_caption(caption)

        self.all_sprites_list = pygame.sprite.Group()
        self.player_list      = pygame.sprite.Group()
        self.enemy_list       = pygame.sprite.Group()

        #... More specific sprite lists here
        self.clock.tick(60)
        
        self.running = True

        self.background = pygame.image.load("ImagesAndSounds/background.jpg").convert()

    def isRunning(self):
        return self.running       

    def createPlayer(self, playerW, playerH, posX, posY):
        player = Player(playerW, playerH, posX, posY)
        self.player_list.add(player)
        self.all_sprites_list.add(player)

    def update(self):
        self.all_sprites_list.update()

    def render(self):
        self.screen.blit(self.background, (0,0))
        self.all_sprites_list.draw(self.screen)
        pygame.display.flip()
        
    def __del__(self):
        
        pygame.quit()
