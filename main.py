
'''
Move Towards Mouse
'''

import pygame
from pygame import examples
from pygame.examples import aliens
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
        #Timer placeholder for how many seconds movement takes the finer movement
        self.remainderMoveTimer = 2
        #Tracer values for all velocities
        self.tracexvelocity = 0
        self.traceyvelocity = 0
        self.traceremainderxvelocity = 0
        self.traceremainderyvelocity = 0
        #Dont know what this guy does, but probabley sets what the moveTimr can do
        self.moveFactor = 40
        #Boolean value that determines if a wall was hit
        self.collision = pygame.sprite.spritecollide(self,wall_list,False)
        self.obstacle = wall_list

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


    def move(self):
        '''
        Updates the velocities of the player after detecting a mouse click
        '''
        #determines how many increment to move the object by, say the difference in x was 80, this would divide that by say 40 and get 2, so each update would add 2 to posx
        self.collision = pygame.sprite.spritecollide(self,self.obstacle,False)

        #Gets position of mouse and finds difference in x and y cords of both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

        #Divides difference of points by factor that determines how fast the character moves
        self.xvelocity = self.movedx/self.moveFactor
        self.yvelocity = self.movedy/self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders that are left, and these values store them so they can be added in between big velocity movements
        self.remainderxvelocity = (self.movedx%self.moveFactor)/(self.moveFactor/self.remainderMoveTimer)
        self.remainderyvelocity = (self.movedy%self.moveFactor)/(self.moveFactor/self.remainderMoveTimer)

        #this variable basically tells the main loop, how many times to update player pos before it reaches destination
        self.moveTimer = self.moveFactor


    def changeVelocityAfterCollision(self):
        '''
        Sets the velocities of players to ad absolute of 1 after a collision
        '''
        #All of the name velocities that we need to use in the next few commands for string insertion
        velocities = ['xvelocity','yvelocity','remainderxvelocity','remainderyvelocity']

        #Each loop changes a velocity after a collision only if the velocity is not the same as it was before
        for values in velocities:
            #All these variables are strings that will be executed as commands
            velocity = 'velocity = self.%s' % values
            currentTrace = 'currentTrace = self.trace%s' % values
            traceAssign = 'self.trace%s = self.%s' % (values,values)
            changeVelocity = ('self.%s = -1*self.%s/abs(self.%s)') % (values,values,values)
            #assigns variable currentTrace a trace velocity (previous velocity) value
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
            if self.moveTimer%2 == 0:
                self.rect.x += self.remainderxvelocity
                self.rect.y += self.remainderyvelocity
            #Updates position eith velocity
            self.rect.x += self.xvelocity
            self.rect.y += self.yvelocity
            #Checks to see if a collision occured after the move
            self.collision = pygame.sprite.spritecollide(self,wall_list,False)
            self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
            #If collision was at exit block, loads new map
            if self.exit_level:
                change_map("map0")
            #if not exit block, but normal wall cancel last movement
            elif self.collision:
                if self.moveTimer%2 == 0:
                    self.rect.x -= self.remainderxvelocity
                    self.rect.y -= self.remainderyvelocity
                self.rect.x -= self.xvelocity
                self.rect.y -= self.yvelocity
                #and set velocity to opposite direction equal to 1
                self.changeVelocityAfterCollision()

            self.moveTimer -= 1

    def attack_Q(self):
        '''
        Creates the Q electricity ball attack, and projects it to wherever the mouse was
        '''
        orb = ElectricityOrb()
        attack_sprites_list.add(orb)
        all_sprites_list.add(orb)
        #print 'it worked in the function?'

    def attack_R(self):
        laser = Laser()
        attack_sprites_list.add(laser)
        all_sprites_list.add(laser)

    def update(self):
        '''
        Updates all of the movement attributes of the player each loop of the main loop
        '''
        #Movement Update
        self.moveUpdate()
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



class ElectricityOrb(Player):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        # Width and height of image
        self.width = 10
        self.height = 10
        # Creates images (CREATE TWO, one for reference later)
        self.imageMaster = pygame.Surface([self.width,self.height])
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

        #Timer placeholder for how many seconds movement takes the finer movement
        self.remainderMoveTimer = 2
        #Tracer values for all velocities
        self.tracexvelocity = 0
        self.traceyvelocity = 0
        self.traceremainderxvelocity = 0
        self.traceremainderyvelocity = 0
        #Dont know what this guy does, but probabley sets what the moveTimr can do
        self.moveFactor = 40
        #Boolean value that determines if a wall was hit
        self.collision = pygame.sprite.spritecollide(self,wall_list,False)
        self.orb_image = pygame.image.load("orb.png").convert()
        self.orb_image.set_colorkey(bg)
        self.obstacle = wall_list
        self.move()

    def get_pos(self):
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
            self.collision = pygame.sprite.spritecollide(self,wall_list,False)
            self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
            #If collision was at exit block, loads new map
            if self.exit_level or self.collision:
                all_sprites_list.remove(self)

    def move(self):
        '''
        Updates the velocities of the player after detecting a mouse click
        '''
        #determines how many increment to move the object by, say the difference in x was 80, this would divide that by say 40 and get 2, so each update would add 2 to posx

        #Gets position of mouse and finds difference in x and y cords of both points
        self.mouseMovePos = pygame.mouse.get_pos()
        self.movedx = self.mouseMovePos[0] - self.rect.center[0]
        self.movedy = self.mouseMovePos[1] - self.rect.center[1]

        #Divides difference of points by factor that determines how fast the character moves
        self.xvelocity = self.movedx/self.moveFactor
        self.yvelocity = self.movedy/self.moveFactor

        #Since pygame is not perfect, when dividing, there are remainders that are left, and these values store them so they can be added in between big velocity movements
        self.remainderxvelocity = (self.movedx%self.moveFactor)/(self.moveFactor/self.remainderMoveTimer)
        self.remainderyvelocity = (self.movedy%self.moveFactor)/(self.moveFactor/self.remainderMoveTimer)

        #this variable basically tells the main loop, how many times to update player pos before it reaches destination
        self.moveTimer = self.moveFactor

    def update(self):
        Player.update(self)
        screen.blit(self.orb_image,(self.rect.x,self.rect.y))


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass
        #pass
        # Get mouse position again

        #self.image.set_colorkey(red)
    def get_pos(self):
        self.mousex = pygame.mouse.get_pos()[0]
        self.mousey = pygame.mouse.get_pos()[1]
        self.currentx = player.rect.centerx
        self.currenty = player.rect.centery
        self.dx = self.mousex - self.currentx
        self.dy = self.mousey - self.currenty
        self.mouse_angle = atan2(-self.dy,self.dx)
        self.mouse_angle = degrees(self.mouse_angle)

    def get_master(self):
        self.masterimage = pygame.Surface([self.dx,40])
        self.image = self.masterimage
        self.rect = self.image.get_rect()
        self.image.set_colorkey(white)
        self.image.fill(red)
        self.top = self.rect.top

    def set_pos(self):
        self.rect.x = player.rect.centerx
        self.rect.y = player.rect.centery

    def debug(self):
        print " Current dx and dy values \n"
        print "\t" + str(self.dx)
        print "\t" + str(self.dy)
        print "\nCurrent X and Y values for image"
        print "\t" + str(self.rect.x)
        print "\t" + str(self.rect.y)
        #self.image.set_colorkey(white)
        #self.image.fill(red)

    def update(self):
        self.get_pos()
        self.get_master()
        self.image = pygame.transform.rotate(self.masterimage, self.mouse_angle)
        self.rect = self.image.get_rect()
        self.rect.top = self.top
        self.set_pos()
        self.debug()

def change_map(map_name):
    '''
    Builds new map when exit encountred, and creates new walls
    '''
    all_sprites_list.empty()
    wall_list.empty()
    exit_list.empty()
    attack_sprites_list.empty()

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
attack_sprites_list = pygame.sprite.Group()
#enemy_list = pygame.sprite.Group()


# Create object player
playerWidth = 40
playerHeight= 40
player = Player(playerWidth,playerHeight)

# Adds player to sprites list
all_sprites_list.add(player)
all_sprites_list.add(build.all_sprites_list)
wall_list.add(build.wall_list)
exit_list.add(build.exit_doors_list)
obstacles_for_attacks = wall_list

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
                #print button_pressed
            elif event.type == pygame.MOUSEBUTTONUP:
                if button_pressed[2]:
                    player.move()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.attack_Q()
                if event.key == pygame.K_r:
                    player.attack_R()


        #Move player Position###

        #Defines borders which player should not be able to pass
        playerWidthBorder = playerWidth/2+5 + 30
        playerHeightBorder = playerHeight/2 + 5 + 30

        # Makes sure that the player should not be moving
        # And that the movement does not push them outside the border

        # fills background color
        screen.fill(bg)

        # Call update function of sprites
        all_sprites_list.update()

        # Draw all sprites on screen
        all_sprites_list.draw(screen)
        """try:
            for values in attack_sprites_list:
                values.draw()
        except:
            pass"""
        # Set tick rate to 60
        clock.tick(60)

        # Redraw screen
        pygame.display.flip()

# Quit if loop is exited
pygame.quit()
