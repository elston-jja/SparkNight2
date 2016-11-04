import pygame


class universal(pygame.sprote.Sprite):

    def __init__(self,width,height, initialx, initialy, alpha):

        pygame.sprite.Sprite.__init__(self)

        if width or height:

            self.image = pygame.Surface([width,height])

        if alpha:
            self.image.set_colorkey(alpha)


        self.rect = pygame.image.get_rect()

        self.rect.x = initialx

        self.rect.y = initialy
