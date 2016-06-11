import pygame
from pygame import *
from pygame import gfxdraw

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 250
        self.fireball = False
        self.ultimate = False
        
    def draw_animations(self):
        if self.fireball == True:
            for i in xrange(1,80,1):
                pygame.gfxdraw.aacircle(screen,self.rect.centerx,self.rect.centery,i,orange)
                pygame.time.wait(1)
                pygame.display.flip()

        if self.ultimate == True:
            pygame.draw.aaline(screen, orange, self.rect)
            

    def mouse_pos(self):
        self.mouse = pygame.mouse.get_pos()
            
    def update(self):
        self.draw_animation()

pygame.init()

width = 600
height = 600
bg = (0,0,0)
white = (255,255,255)
orange = ( 255, 102, 0)
screen = pygame.display.set_mode([width,height])

pygame.display.set_caption("Testing Sprite Animation")

player = Player()
all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(player)

clock = pygame.time.Clock()
isDone = False

while isDone == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDone = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player.fireball = True
                print "Fireball"
            if event.key == pygame.K_r:
                player.ultimate = True
                print "Fireball"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                player.fireball = False
                print "Fireball ending"
            if event.key == pygame.K_r:
                player.ultimate = False
                print "Ultimate ending"
    screen.fill(bg)
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
