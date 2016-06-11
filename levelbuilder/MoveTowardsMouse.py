
'''
Move Towards Mouse
'''

import pygame
import build
from math import *

class Player(pygame.sprite.Sprite):
    '''
    Class creates player objects that are used later for enemies and the main player
    '''

    def __init__(self,PlayerWidth,PlayerHeight):
        pygame.sprite.Sprite.__init__(self)

        # Width and height of image
        self.width = PlayerWidth
        self.height = PlayerHeight

        # Creates images (CREATE TWO, one for reference later)
        self.imageMaster = pygame.Surface([self.width,self.height])
        self.image = self.imageMaster

        # Fills the image with white
        self.image.fill(white)

        # Makes transparent background
        # YOU NEED THIS FOR IT TO ROTATE
        self.image.set_colorkey(red)

        # Get rect frame of image
        self.rect = self.image.get_rect()

        # angle to face mouse
        self.rect.x = 150
        self.rect.y = 150

        # Just placeholder
        self.angle = 0
        self.vely = 2
        self.velx = 2

        #Movement placeholder variables
        self.mouseMovePos = 0
        self.movedy = 0
        self.movedx = 0
        self.xvelocity = 0
        self.yvelocity = 0
        self.remainderxvelocity = 0
        self.remainderyvelocity = 0
        self.moveTimer = 0
        self.velocities = {"xvelocity":self.xvelocity,"yvelocity":self.yvelocity,"remainderxvelocity":self.remainderxvelocity,"remainderyvelocity":self.remainderyvelocity}
        self.remainderMoveTimer = 2
        self.tracexvelocity = 0
        self.traceyvelocity = 0
        self.traceremainderxvelocity = 0
        self.traceremainderyvelocity = 0
        self.moveFactor = 40
        self.collision = pygame.sprite.spritecollide(self,wall_list,False)

    def get_pos(self):
        '''
        Gets the position and angle of the mouse, and adjusts the players angle that they are viewing
        '''
        # Get mouse cords while game running
        self.pos = pygame.mouse.get_pos()

        # Get change in X and y dy/dy
        self.dy = self.pos[1] - self.rect.y -20
        self.dx = self.pos[0] - self.rect.x -20

        # Get angle from mouse and player
        self.mouse_angle = atan2(-self.dy,self.dx)
        # Var for move function
        self.mouse_angle = degrees(self.mouse_angle)
        self.angle_move = self.mouse_angle
        # Sets angle value in class
        self.angle = self.mouse_angle
        if self.angle < 0:
            self.angle += 360
        #print self.angle

    def move(self):
        '''
        '''
        #Determines how the to move the object from current pos to mouse pos, does not actually move it, just sets the velocities
        '''
        #determines how many increment to move the object by, say the difference in x was 80, this would divide that by say 40 and get 2, so each update would add 2 to posx
        moveFactor = 40
        player.moveFactor = moveFactor

        #Gets position of mouse and finds difference in x and y cords of both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

        #Divides difference of points by factor that determines how fast the character moves
        self.xvelocity = self.movedx/moveFactor
        self.yvelocity = self.movedy/moveFactor

        #Since pygame is not perfect, when dividing, there are remainders that are left, and these values store them so they can be added in between big velocity movements
        self.remainderxvelocity = (self.movedx%moveFactor)/(self.moveFactor/self.remainderMoveTimer)
        if self.movedx < 0:
            self.remainderxvelocity *= -1
        self.remainderyvelocity = (self.movedy%moveFactor)/(self.moveFactor/self.remainderMoveTimer)
        if self.movedy < 0:
            self.remainderyvelocity *= -1
        #updates all velocities in velocity dictionary
        self.updateVelocities()
        #this variable basically tells the main loop, how many times to update player pos before it reaches destination
        self.moveTimer = moveFactor

        #print self.velocities
        '''
        '''
        Determines how the to move the object from current pos to mouse pos, does not actually move it, just sets the velocities
        '''
        #determines how many increment to move the object by, say the difference in x was 80, this would divide that by say 40 and get 2, so each update would add 2 to posx
        self.collision = pygame.sprite.spritecollide(self,wall_list,False)

        #Gets position of mouse and finds difference in x and y cords of both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

        #Divides difference of points by factor that determines how fast the character moves
        self.xvelocity = self.movedx/self.moveFactor
        self.yvelocity = self.movedy/self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders that are left, and these values store them so they can be added in between big velocity movements
        self.remainderxvelocity = (self.movedx%self.moveFactor)/(self.moveFactor/self.remainderMoveTimer)
        #if self.movedx < 0:
        #    self.remainderxvelocity *= -1
        self.remainderyvelocity = (self.movedy%self.moveFactor)/(self.moveFactor/self.remainderMoveTimer)
        #if self.movedy < 0:
        #    self.remainderyvelocity *= -1
        #updates all velocities in velocity dictionary
        self.updateVelocities()
        #this variable basically tells the main loop, how many times to update player pos before it reaches destination
        self.moveTimer = self.moveFactor

    #Updates all velocities
    def updateVelocities(self, isDict = True):
        '''
        Updates all the velocity values in the entire object,
        only really done because dictionary was created with all velocity values,
        for the use of looping through values quickly
        '''
        #Updates the dictionary values so they are the same as the recently changed attribures
        if isDict:
            self.velocities['xvelocity'] =  self.xvelocity
            self.velocities['yvelocity'] =  self.yvelocity
            self.velocities['remainderxvelocity'] =  self.remainderxvelocity
            self.velocities['remainderyvelocity'] =  self.remainderyvelocity
        #Change attributes so they are like recently changed dictionary values
        else:
            self.xvelocity = self.velocities['xvelocity']
            self.yvelocity = self.velocities['yvelocity']
            self.remainderxvelocity = self.velocities['remainderxvelocity']
            self.remainderyvelocity = self.velocities['remainderyvelocity']


    # Collisions
    def check_collisions(self):

        velocities = ['xvelocity','yvelocity','remainderxvelocity','remainderyvelocity']
        #self.collision = pygame.sprite.spritecollide(self,wall_list,False)

        #if self.collision:
        #   print 'Collision'
        for values in velocities:
            velocity = 'velocity = self.%s' % values
            currentTrace = 'currentTrace = self.trace%s' % values
            traceAssign = 'self.trace%s = self.%s' % (values,values)
            changeVelocity = ('self.%s = -1*self.%s/abs(self.%s)') % (values,values,values)
            exec(currentTrace)
            exec(velocity)
            if abs(velocity) > 0 and currentTrace != velocity:
                exec(changeVelocity)
                exec(traceAssign)

        self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
        if self.exit_level:
            change_map("map0")

    def update(self):

        #self.check_collisions() #removed b/c not needed

        # Gets mouse position
        self.get_pos()

        # Gets the old center point
        self.centerpoint = self.rect.center

        # Rotate sprite
        self.image = pygame.transform.rotate(self.imageMaster ,self.angle)

        # Get rectangle frame
        self.rect = self.image.get_rect()

        # Sets the new image to the old center point
        # Makes sure the sprite does not go flying to oblivion
        self.rect.center = self.centerpoint

    def moveUpdate(self):
        '''
        Changes the x and y position of the player
        '''
        if self.moveTimer > 0:
            if self.moveTimer%2 == 0:
                self.rect.x += self.remainderxvelocity
                self.rect.y += self.remainderyvelocity
            self.rect.x += self.xvelocity
            self.rect.y += self.yvelocity

            self.collision = pygame.sprite.spritecollide(self,wall_list,False)

            if self.collision:
                if self.moveTimer%2 == 0:
                    self.rect.x -= self.remainderxvelocity
                    self.rect.y -= self.remainderyvelocity
                self.rect.x -= self.xvelocity
                self.rect.y -= self.yvelocity
                self.check_collisions()
            self.moveTimer -= 1

def change_map(map_name):

    all_sprites_list.empty()
    wall_list.empty()
    exit_list.empty()

    build.all_sprites_list.empty()
    build.exit_doors_list.empty()
    build.wall_list.empty()

    build.Level(map_name)

    all_sprites_list.add(player)

    all_sprites_list.add(build.all_sprites_list)
    wall_list.add(build.wall_list)
    exit_list.add(build.exit_doors_list)



pygame.init()



# dimensions of screen
width = 1440
height = 900

# COLORS
bg = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

# Screen
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("testing mouse and player")

draw_map = build.Level("map2")

# Create sprite group
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
exit_list = pygame.sprite.Group()

# Create object player
playerWidth = 40
playerHeight= 40
player = Player(playerWidth,playerHeight)

# Adds player to sprites list
all_sprites_list.add(player)
all_sprites_list.add(build.all_sprites_list)
wall_list.add(build.wall_list)
exit_list.add(build.exit_doors_list)

# Game time for clock functions
clock = pygame.time.Clock()

# Fill background (Makes cicle, when loop screen.fill is commented)
#screen.fill(bg)

# LOOP
done = False

while not done:
            # Quit pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_pressed = pygame.mouse.get_pressed()
            elif event.type == pygame.MOUSEBUTTONUP:
                if button_pressed[2]:
                    player.move()

        #Move player Position###

        #Defines borders which player should not be able to pass
        playerWidthBorder = playerWidth/2+5 + 30
        playerHeightBorder = playerHeight/2 + 5 + 30

        # Makes sure that the player should not be moving
        # And that the movement does not push them outside the border
        player.moveUpdate()

        # Call update function of sprites
        all_sprites_list.update()

        # fills background color
        screen.fill(bg)

        # Draw all sprites on screen
        all_sprites_list.draw(screen)

        # Set tick rate to 60
        clock.tick(60)

        # Redraw screen
        pygame.display.flip()

# Quit if loop is exited
pygame.quit()
