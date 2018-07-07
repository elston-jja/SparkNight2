import Player

class Enemy(Player):

    def __init__(self,spawnx,spawny):
        '''
        Explenations of attributes in Player Class
        '''
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, 30, 30)
        self.rect.x = spawnx
        self.rect.y = spawny
        self.health = 3
        self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
        self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
        self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, False)
        self.imageMasterSprite = pygame.image.load("ImagesAndSounds/Wizard_Male.png").convert()
        self.imageMasterSprite = pygame.transform.scale(self.imageMasterSprite, (30,30))
        self.imageMasterSprite = pygame.transform.rotate(self.imageMasterSprite, 180)
        self.imageSprite = self.imageMasterSprite
        self.imageSprite.set_colorkey(white)
        self.isBoss = False

    def move(self):
        '''
        Updates the velocities of the enemy by, checking where the player is and drawing hypotonus to it
        '''
        #determines how many increment to move the object by, say the
        #difference in x was 80, this would divide that by say 40 and get 2,
        # so each update would add 2 to posx
        self.wallCollision = pygame.sprite.spritecollide(self, self.obstacle, False)

        #Gets position of mouse and finds difference in x and y cords of
        #both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = player.rect.centerx - self.rect.center[0]
        self.movedy = player.rect.centery - self.rect.center[1]

        #Divides difference of points by factor that determines how fast the
        #character moves
        self.xvelocity = self.movedx / self.moveFactor
        self.yvelocity = self.movedy / self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders
        #that are left, and these values store them so they can be
        # added in between big velocity movements
        self.remainderxvelocity = (self.movedx % self.moveFactor) /\
        (self.moveFactor / self.remainderMoveTimer)
        self.remainderyvelocity = (self.movedy % self.moveFactor) /\
         (self.moveFactor / self.remainderMoveTimer)

        #this variable basically tells the main loop, how many times to
        #update player pos before it reaches destination
        self.moveTimer = self.moveFactor

    def moveUpdate(self):
        '''
        Changes the x and y position of the enemy
        '''
        #Checks to see if the move timer is over
        if self.moveTimer > 0:
            #lets the remainder update every 2 loops
            if self.moveTimer % 2 == 0:
                self.rect.x += self.remainderxvelocity
                self.rect.y += self.remainderyvelocity
            #Updates position eith velocity
            self.rect.x += self.xvelocity
            self.rect.y += self.yvelocity
            #Checks to see if a collision occured after the move
            self.wallCollision = pygame.sprite.spritecollide(
                self, wall_list, False
            )
            enemy_list.remove(self)
            self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
            self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, True)
            self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
            #print self.player_collide
            #If collision was at exit block, loads new map

            if self.wallCollision or self.enemey_collide:
                if self.moveTimer % 2 == 0:
                    self.rect.x -= self.remainderxvelocity
                    self.rect.y -= self.remainderyvelocity
                self.rect.x -= self.xvelocity
                self.rect.y -= self.yvelocity
                #and set velocity to opposite direction equal to 1
                self.changeVelocityAfterCollision()

            if self.attack_collide:
                self.health -= 1

            if self.player_collide and not self.isBoss:
                #print 'What up my boi'
                overlay.lives -= 1
                all_sprites_list.remove(self)
            else:
                enemy_list.add(self)

            self.moveTimer -= 1

    def update(self):
        self.move()

        if self.health <= 0:
            all_sprites_list.remove(self)

        Player.update(self)
