import pygame

class Player(pygame.sprite.Sprite, object):

    '''
    Class creates player objects that are used later for enemies
    and the main player
    '''

    def __init__(self, PlayerWidth, PlayerHeight):
        pygame.sprite.Sprite.__init__(self)
        # Width and height of image
        self.width = PlayerWidth
        self.height = PlayerHeight
        # Creates images (CREATE TWO, one for reference later)
        self.imageMaster = pygame.Surface([self.width, self.height], pygame.FULLSCREEN)
        self.image = self.imageMaster
        # Fills the image with white
        self.image.fill(white)
        # Makes transparent background
        # YOU NEED THIS FOR IT TO ROTATE
        self.image.set_colorkey(white)
        # Get rect frame of image
        self.rect = self.image.get_rect()
        # angle to face mouse
        self.rect.x = 150
        self.rect.y = 150
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
        #Timer placeholder for how many seconds movement
        #takes the finer movement
        self.remainderMoveTimer = 2
        #Tracer values for all velocities
        self.tracexvelocity = 0
        self.traceyvelocity = 0
        self.traceremainderxvelocity = 0
        self.traceremainderyvelocity = 0
        #Dont know what this guy does, but probabley sets
        #what the moveTimr can do
        self.moveFactor = 40
        self.map_number = 0
        #Boolean value that determines if a wall was hit
        self.wallCollision = pygame.sprite.spritecollide(self, wall_list, False)
        self.obstacle = wall_list

        #Adds pickachu image
        self.imageMasterSprite = pygame.image.load("ImagesAndSounds/pickachu.png").convert()
        self.imageMasterSprite = pygame.transform.rotate(self.imageMasterSprite, 90)
        self.imageMasterSprite = pygame.transform.scale(self.imageMasterSprite, (35,35))
        self.imageSprite = self.imageMasterSprite
        self.imageSprite.set_colorkey(white)

    def get_pos(self):
        '''
        Gets the position and angle of the mouse, and adjusts the
        players angle that they are viewing
        '''
        # Get mouse cords while game running
        self.pos = pygame.mouse.get_pos()

        # Get change in X and y dy/dy
        self.dy = self.pos[1] - self.rect.centery
        self.dx = self.pos[0] - self.rect.centerx

        # Get angle from mouse and player
        self.mouse_angle = atan2(- self.dy, self.dx)

        # Var for move function
        self.mouse_angle = degrees(self.mouse_angle)
        #Possibley does nothing
        self.angle_move = self.mouse_angle

        # Sets angle value in class
        self.angle = self.mouse_angle
        if self.angle < 0:
            self.angle += 360

    def move(self):
        '''
        Updates the velocities of the player after detecting a mouse click
        '''
        #determines how many increment to move the object by, say the
        #difference in x was 80, this would divide that by say 40 and get 2,
        # so each update would add 2 to posx
        self.wallCollision = pygame.sprite.spritecollide(self, self.obstacle, False)

        #Gets position of mouse and finds difference in x and y cords of
        #both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

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

    def changeVelocityAfterCollision(self):
        '''
        Sets the velocities of players to ad absolute of 1 after a collision
        '''
        #All of the name velocities that we need to use in the next few
        #commands for string insertion
        velocities = [
            'xvelocity', 'yvelocity', 'remainderxvelocity', 'remainderyvelocity'
            ]

        #Each loop changes a velocity after a collision only if the
        #velocity is not the same as it was before
        for values in velocities:
            #All these variables are strings that will be executed as commands
            velocity = 'velocity = self.%s' % values
            currentTrace = 'currentTrace = self.trace%s' % values
            traceAssign = 'self.trace%s = self.%s' % (values, values)
            changeVelocity = ('self.%s = -1*self.%s/abs(self.%s)') %\
             (values, values, values)
            #assigns variable currentTrace a trace velocity
            #(previous velocity) value
            exec(currentTrace)
            #Assigns velocity the current velocity value
            exec(velocity)
            if abs(velocity) > 0 and currentTrace != velocity:
                #Changes the velocity to an absolute 1
                exec(changeVelocity)
                #sets the trace to current
                exec(traceAssign)

    def moveUpdate(self):
        '''
        Changes the x and y position of the player
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
            self.exit_level = pygame.sprite.spritecollide(
                self, exit_list, False
            )
            #If collision was at exit block, loads new map
            if self.exit_level:
                self.map_number += 1
                self.map_number = self.map_number
                change_map("map" + str(self.map_number))
            #if not exit block, but normal wall cancel last movement
            elif self.wallCollision:
                if self.moveTimer % 2 == 0:
                    self.rect.x -= self.remainderxvelocity
                    self.rect.y -= self.remainderyvelocity
                self.rect.x -= self.xvelocity
                self.rect.y -= self.yvelocity
                #and set velocity to opposite direction equal to 1
                self.changeVelocityAfterCollision()

            self.moveTimer -= 1

    def attack_Q(self):
        '''
        Creates the Q electricity ball attack, and projects
        it to wherever the mouse was
        '''
        orb = ElectricityOrb()
        attack_sprites_list.add(orb)
        all_sprites_list.add(orb)

    def attack_W(self):
        '''
        Calls the field of effect attack based on the loation of the player
        '''
        area_of_effect = FieldofEffect()
        attack_sprites_list.add(area_of_effect)
        all_sprites_list.add(area_of_effect)

    def update(self):
        '''
        Updates all of the movement attributes of the player
        each loop of the main loop
        '''

        #Movement Update
        self.moveUpdate()
        # Gets mouse position
        self.get_pos()
        # Gets the old center point
        self.centerpoint = self.rect.center
        # Rotate sprite
        self.image = pygame.transform.rotate(self.imageMaster, self.angle)
        self.imageSprite = pygame.transform.rotate(self.imageMasterSprite, self.angle)
        # Get rectangle frame
        self.rect = self.image.get_rect()
        # Sets the new image to the old center point
        # Makes sure the sprite does not go flying to oblivion
        self.rect.center = self.centerpoint

        screen.blit(self.imageSprite, (self.rect.x, self.rect.y))
