import Player

class ElectricityOrb(Player):

    def __init__(self, isBoss = False):
        '''
        attributes explained in Player class
        '''
        pygame.sprite.Sprite.__init__(self)
        # Width and height of image
        self.width = 30
        self.height = 30
        # Creates images (CREATE TWO, one for reference later)
        self.imageMaster = pygame.Surface([self.width, self.height])
        self.image = self.imageMaster
        # Fills the image with white
        #self.image.fill(white)
        self.image.fill(bg)
        # Makes transparent background
        # YOU NEED THIS FOR IT TO ROTATE
        self.image.set_colorkey(bg)
        #self.image.set_colorkey(red)
        # Get rect frame of image
        self.rect = self.image.get_rect()
        # angle to face mouse
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        # Just placeholder
        self.angle = 0
        self.vely = 2
        self.velx = 2
        #Movement placeholder positions
        self.mouseMovePos = 0
        self.movedy = 0
        self.movedx = 0
        #movement placeholder velocities
        self.xvelocity = 0
        self.yvelocity = 0
        self.remainderxvelocity = 0
        self.remainderyvelocity = 0
        #Timer placeholder for how many seconds movement takes
        self.moveTimer = 0

        #Timer placeholder for how many seconds movement takes the
        # finer movement
        self.remainderMoveTimer = 2
        #Tracer values for all velocities
        self.tracexvelocity = 0
        self.traceyvelocity = 0
        self.traceremainderxvelocity = 0
        self.traceremainderyvelocity = 0
        #Dont know what this guy does, but probabley sets what
        # the moveTimr can do
        self.moveFactor = 40
        #Boolean value that determines if a wall was hit
        self.wallCollision = pygame.sprite.spritecollide(self, wall_list, False)
        self.orb_image = pygame.image.load("ImagesAndSounds/better_orb.png").convert()
        self.orbExplision_image = pygame.image.load("ImagesAndSounds/orb_explosion_large.png").convert()
        self.orb_image.set_colorkey(bg)
        self.orbExplision_image.set_colorkey(bg)
        self.obstacle = wall_list
        #Determines which image to load for the orb
        self.exploded = False
        self.isBoss = isBoss
        self.move()

    """def move(self):
            Player.move(self)"""

    def get_pos(self):
        #Stops rotation of orbs, as it messes with collisions
        pass

    def moveUpdate(self):
        '''
        Keeps the electrriy ball moving to where the player clicked it to until collision
        '''
        #Checks to see if the move timer is over
        if self.moveTimer > 0:
            #lets the remainder update every 2 loops
            if self.moveTimer%2 == 0:
                self.rect.x += self.remainderxvelocity
                self.rect.y += self.remainderyvelocity
            #Updates position eith velocity
            self.rect.x += self.xvelocity
            self.rect.y += self.yvelocity
            #Checks to see if a collision occured after the move
            if self.wallCollision and self.moveTimer == 14:
                isDoubleCollision = True
            else:
                isDoubleCollision = False
            self.wallCollision = pygame.sprite.spritecollide(self,wall_list,False)
            self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
            self.wallCollisionTrace = None
            #self.enemy_collision = pygame.sprite.spritecollide(self,enemy_list,False)
            #If collision was at exit block, loads new map


            if (self.exit_level or self.wallCollision and not isDoubleCollision): #or self.enemy_collision:
                self.moveTimer = 15
                self.exploded = True
                #print "it's colliding"
                self.changeVelocityAfterCollision()
            if self.moveTimer <= 10:
                self.exploded = True
            self.moveTimer -= 1
            #print 'Its subtracting'
        else:
            all_sprites_list.remove(self)

    def move(self):
        '''
        Updates the velocities of the player after detecting a mouse click
        '''
        #determines how many increment to move the object by, say the difference
        #in x was 80, this would divide that by say 40 and get 2,
        #so each update would add 2 to posx

        #Gets position of mouse and finds difference in x and y cords
        #of both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

        # Divides difference of points by factor that determines
        # how fast the character moves
        self.xvelocity = self.movedx / self.moveFactor
        self.yvelocity = self.movedy / self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders
        # that are left, and these values store them so they can be added
        # in between big velocity movements
        self.remainderxvelocity = (self.movedx % self.moveFactor) /\
         (self.moveFactor / self.remainderMoveTimer)
        self.remainderyvelocity = (self.movedy % self.moveFactor) /\
         (self.moveFactor / self.remainderMoveTimer)

        #this variable basically tells the main loop, how many times
        # to update player pos before it reaches destination
        self.moveTimer = self.moveFactor + 40

    def update(self):
        #Movement Update
        self.moveUpdate()
        # Gets mouse position
        self.get_pos()
        # Gets the old center point
        self.centerpoint = self.rect.center
        # Rotate sprite
        #self.image = pygame.transform.rotate(self.imageMaster, self.angle)
        # Get rectangle frame
        self.rect = self.image.get_rect()
        # Sets the new image to the old center point
        # Makes sure the sprite does not go flying to oblivion
        self.rect.center = self.centerpoint

        if self.exploded:
            self.orbDrawImage = self.orbExplision_image
            #print 'Allah Akbar'
        else:
            self.orbDrawImage = self.orb_image

        screen.blit(self.orbDrawImage, (self.rect.x, self.rect.y))
