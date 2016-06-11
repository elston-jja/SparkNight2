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
        self.i = 0
        self.ultimate = False

    def draw_animations(self):
        if self.fireball == True:
            #pygame.gfxdraw.aacircle(screen,self.rect.centerx,self.rect.centery,(self.i-self.i/4),orange)
            pygame.gfxdraw.aacircle(screen,self.rect.centerx,self.rect.centery,(self.i+ 3),orange)
            #pygame.gfxdraw.aacircle(screen,self.rect.centerx,self.rect.centery,(self.i/2 +2),orange)
            #pygame.gfxdraw.aacircle(screen,self.rect.centerx,self.rect.centery,(self.i/3 +2),orange)
            #pygame.gfxdraw.aacircle(screen,self.rect.centerx,self.rect.centery,(self.i/4 +2),orange)
            self.i += 3
            if self.i > 80:
                self.i = 0

        if self.ultimate == True:
            self.mouse_pos()
            pygame.draw.line(screen, orange, [self.rect.centerx,self.rect.centery],[self.mouse[0],self.mouse[1]],5)
            pygame.display.flip()

    def mouse_pos(self):
        self.mouse = pygame.mouse.get_pos()

    def update(self):
        self.draw_animations()

class Attack(pygame.sprite.Sprite):
        def __init__(self,width,height,color,positionx,positiony):
            pygame.sprite.Sprite.__init__(self)
            self.width = width
            self.height = height
            self.color= color
            self.x = positionx
            self.y = positiony
            self.image = pygame.Surface([self.width,self.heigth])
            self.image.fill(self.color)
            self.rect = self.image.get_rect()

class Attack(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.x = 50
        self.y = 50
        self.sprite = pygame.image.load("/home/ea/Dropbox/cpt/levelbuilder/"+image+".png").convert()

        self.update()

    def mouse_pos(self):
        self.mouse = pygame.mouse.get_pos()

    def update(self):
        screen.blit(self.sprite,(self.x,self.y))
        self.x += self.velocity

# class Fireball(Attack):
#     def __init__(self):
#         Attack.__init__(self,20,20,blue):

pygame.init()


width = 600
height = 600
bg = (0,0,0)
white = (255,255,255)
orange = ( 255, 102, 0)
screen = pygame.display.set_mode([width,height])

pygame.display.set_caption("Testing Sprite Animation")
orb = Attack("orb")
player = Player()
all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(player)

clock = pygame.time.Clock()
isDone = False

while isDone == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isDone = True
#
    screen.fill(bg)
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    orb.update()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
