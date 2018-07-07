import pygame

class Wall(pygame.sprite.Sprite):

    def __init__(self,x,y,color):

        # Base sprite class with collisions
        pygame.sprite.Sprite.__init__(self)
        # Create the width and height of surface
        self.image = pygame.Surface([30,30])
        self.rect = self.image.get_rect()
        self.color = color
        # Set the colors
        self.image.fill(color)
        self.image.set_colorkey(color)
        # Check to see what color and draw
        # an image accordingly
        self.checkBlockSprite()
        # Set the image to be drawn at given x and y cords
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def checkBlockSprite(self):
        '''
        Checks to see what was the color code of the block
        this enables the program to know what type of block to draw
        using different color codes
        '''
        if self.color == grey:
            self.block = pygame.image.load("ImagesAndSounds/wall.png").convert()
            self.block = pygame.transform.scale(self.block,(30,30))
        else:
            self.block = pygame.image.load("ImagesAndSounds/exit.png").convert_alpha()
            self.block = pygame.transform.scale(self.block,(30,30))

    def update(self):
        screen.blit(self.block,(self.x,self.y))
