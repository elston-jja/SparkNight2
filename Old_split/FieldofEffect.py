import pygame

class FieldofEffect(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        # Initial width, height, and field size
        self.height = 2
        self.width = 2
        self.field_level = 2
        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(bg)
        # Number of times to loop animation
        self.loop_animation = 1

    def draw(self):
        '''
        Draw radiating circles as attack for player
        '''
        # Increase Field level
        self.field_level += 2

        # Draw Surface
        self.image = pygame.Surface([self.width,self.height])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(bg)
        #self.image.fill(red)

        # set center points to player
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery

        # draw circle
        pygame.draw.circle(screen,red,player.rect.center,self.field_level,1)

        # When circle radius(field size) is max, reset the field size
        # reset the width and the height of the image and count to 1 less loop
        if self.field_level > 80:
            self.field_level = 2
            self.loop_animation -= 1
            self.width = 2
            self.height = 2
        # When increase the width and the height by 4 (of surface)
        self.width += 4
        self.height += 4

        # Makes sure the object is removed durring a level change or
        # removes an enemy when hit
        self.check_collisions()

        # When done looping, remove itself from the drawn classes
        if self.loop_animation < 0:
            attack_sprites_list.remove(self)
            all_sprites_list.remove(self)

    def check_collisions(self):
        '''
        Removes the attack, when a new level has been loaded
        '''
        self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
        if self.exit_level:
            all_sprites_list.remove(self)
            attack_sprites_list.remove(self)

    def update(self):
        self.draw()
