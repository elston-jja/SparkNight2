
'''
Move Towards Mouse
'''

import pygame
from math import *
from pygame.locals import *
from map_list import maps

class Player(pygame.sprite.Sprite):

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
        self.collision = pygame.sprite.spritecollide(self, wall_list, False)
        self.obstacle = wall_list

        #Adds pickachu image
        self.pickachu_Master = pygame.image.load("pickachu.png").convert()
        self.pickachu_Master = pygame.transform.rotate(self.pickachu_Master, 90)
        self.pickachu_Master = pygame.transform.scale(self.pickachu_Master, (35,35))
        self.pickachu = self.pickachu_Master
        self.pickachu.set_colorkey(white)

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
        self.collision = pygame.sprite.spritecollide(self, self.obstacle, False)

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
            self.collision = pygame.sprite.spritecollide(
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
            elif self.collision:
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
        #print 'it worked in the function?'

    #def attack_R(self):
#        laser = Laser()
#        attack_sprites_list.add(laser)
#        all_sprites_list.add(laser)

    def attack_W(self):
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
        self.pickachu = pygame.transform.rotate(self.pickachu_Master, self.angle)
        # Get rectangle frame
        self.rect = self.image.get_rect()
        # Sets the new image to the old center point
        # Makes sure the sprite does not go flying to oblivion
        self.rect.center = self.centerpoint

        screen.blit(self.pickachu, (self.rect.x, self.rect.y))


class Enemy(Player):

    def __init__(self,spawnx,spawny):
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, 30, 30)
        self.rect.x = spawnx
        self.rect.y = spawny
        self.health = 3
        #self.image = ""
        self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
        self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
        self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, False)

    def move(self):
        '''
        Updates the velocities of the player after detecting a mouse click
        '''
        #determines how many increment to move the object by, say the
        #difference in x was 80, this would divide that by say 40 and get 2,
        # so each update would add 2 to posx
        self.collision = pygame.sprite.spritecollide(self, self.obstacle, False)

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
            self.collision = pygame.sprite.spritecollide(
                self, wall_list, False
            )
            enemy_list.remove(self)
            self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
            self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, True)
            self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
            #print self.player_collide
            #If collision was at exit block, loads new map

            if self.collision or self.enemey_collide:
                if self.moveTimer % 2 == 0:
                    self.rect.x -= self.remainderxvelocity
                    self.rect.y -= self.remainderyvelocity
                self.rect.x -= self.xvelocity
                self.rect.y -= self.yvelocity
                #and set velocity to opposite direction equal to 1
                self.changeVelocityAfterCollision()

            if self.attack_collide:
                self.health -= 1

            if self.player_collide:
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


class ElectricityOrb(Player):

    def __init__(self):

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
        self.collision = pygame.sprite.spritecollide(self, wall_list, False)
        self.orb_image = pygame.image.load("better_orb.png").convert()
        self.orbExplision_image = pygame.image.load("orb_explosion_large.png").convert()
        self.orb_image.set_colorkey(bg)
        self.orbExplision_image.set_colorkey(bg)
        self.obstacle = wall_list
        self.exploded = False
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
            if self.collision and self.moveTimer == 14:
                isDoubleCollision = True
            else:
                isDoubleCollision = False
            self.collision = pygame.sprite.spritecollide(self,wall_list,False)
            self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
            self.collisionTrace = None
            #self.enemy_collision = pygame.sprite.spritecollide(self,enemy_list,False)
            #If collision was at exit block, loads new map


            if (self.exit_level or self.collision and not isDoubleCollision): #or self.enemy_collision:
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
        self.exit_level = pygame.sprite.spritecollide(self,exit_list,False)
        #If collision was at exit block, loads new map
        if self.exit_level:
            all_sprites_list.remove(self)
            attack_sprites_list.remove(self)

    def update(self):
        self.draw()

class Level:

    def __init__(self,level):
        # State the initial level number
        # Value not needed except for verbosity
        self.level = level
        # Default x y starting block cordinates
        x = 0
        y = 0
        # Creates object called "list of maps" and I can call all maps
        # From the lists in the maps_list file
        list_of_maps = maps()
        # Get the level from maps_list and load it into the interpreter
        # Change the current level to the list varible in the maps_list file
        exec_var = "self.current_level = list_of_maps." + str(self.level)
        exec (exec_var)
        # Get the lines/rows from each variable in the list
        for line_row in self.current_level:
            # Check each character in the row
            for char in line_row:
                # if the character is a 'w' then add a wall block (30,30)
                if char == "w":
                    wall = Wall(x,y,grey)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                # If the character is an 'e' then add an wall block
                # That when collided can cause to exit
                # As it is added to the exitdoor list (change var is need be)
                if char == "e":
                    exit_ = Wall(x,y,red)
                    wall_list.add(exit_)
                    exit_list.add(exit_)
                    all_sprites_list.add(exit_)
                elif char == "y":
                    wall = Wall(x,y,yellow)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                elif char == "g":
                    wall = Wall(x,y,green)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                elif char == "p":
                    wall = Wall(x,y,purple)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                elif char == "y":
                    wall = Wall(x,y,yellow)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                elif char == "P":
                    player.rect.x = x
                    player.rect.y = y
                elif char == "E":
                    enemy = Enemy(x,y)
                    enemy_list.add(enemy)
                    all_sprites_list.add(enemy)
                    # When drawing each block
                    # (Character in row)
                    # Move 30px to the right
                x+= 30
                # When moving down to next row change the Y by 30
                # Reset th X
            y+=30
            x = 0

class Wall(pygame.sprite.Sprite):

    def __init__(self,x,y,color):

        # Base sprite class with collisions
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30])
        self.rect = self.image.get_rect()
        self.color = color
        self.image.fill(color)
        if self.color == grey:
            self.image.set_colorkey(color)
            self.block = pygame.image.load("wall.png").convert()
            self.block = pygame.transform.scale(self.block,(30,30))
        elif self.color == red:
            self.image.set_colorkey(color)
            self.block = pygame.image.load("exit.png").convert_alpha()
            self.block = pygame.transform.scale(self.block,(30,30))
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        #screen.blit(self.block,(90,90))

    def update(self):
        if self.color == grey:
            screen.blit(self.block,(self.x,self.y))
        if self.color == red:
            screen.blit(self.block,(self.x,self.y))

class Overlay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 3
        pygame.font.init()
        self.font = pygame.font.SysFont("Calibri",20)
        self.live_text = self.font.render("Lives: ",True,bg)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(bg)
        self.hearts = pygame.image.load("heart.png").convert_alpha()
        self.hearts = pygame.transform.scale(self.hearts,(30,30))

    def update(self):
        screen.blit(self.live_text, (40,40))
        if self.lives == 3:
            screen.blit(self.hearts,(40, 60))
            screen.blit(self.hearts,(80, 60))
            screen.blit(self.hearts,(120, 60))
        if self.lives == 2:
            screen.blit(self.hearts,(40, 60))
            screen.blit(self.hearts,(80, 60))
        if self.lives == 1:
            screen.blit(self.hearts,(40, 60))
        if self.lives == 0:
            restart()

    def main_menu(self):
        self.screen_text = "Press ESC to resume"
        self.music_toggle = ('Press "u" to toggle music') #"Press "x" to do function"
        pygame.image.save(screen,"current_bg.jpg")
        frame = pygame.image.load("current_bg.jpg")
        inMenu = True
        while inMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    global done
                    done = True
                    inMenu = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        inMenu = False
                    elif event.key == pygame.K_u:
                        print " STOP MUSIC "
                        
            self.pause_type = pygame.font.SysFont("Calibri",80)
            self.pause_render = self.pause_type.render(self.screen_text,True,bg)
            self.options_type = pygame.font.SysFont("Calibri", 50)
            self.options_render = self.options_type.render(self.music_toggle, True, bg)
            screen.blit(self.blurSurf(frame,15),(0,0))
            screen.blit(self.pause_render, (450,90))
            screen.blit(self.options_render, (530, 300))
            clock.tick(60)
            pygame.display.flip()




    def blurSurf(self,surface, amt):
        """
        Blur the given surface by the given 'amount'.  Only values 1 and greater
        are valid.  Value 1 = no blur.
        """
        scale = 1.0/float(amt)
        surf_size = surface.get_size()
        scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf

def change_map(map_name):
    '''
    Builds new map when exit encountred, and creates new walls
    '''
    all_sprites_list.empty()
    wall_list.empty()
    exit_list.empty()
    attack_sprites_list.empty()
    exit_doors_list.empty()
    Level(map_name)
    all_sprites_list.add(player, overlay, all_sprites_list)
    wall_list.add(wall_list)

pygame.init()

# dimensions of screen
width = 1440
height = 870

# COLORS
bg = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
#bg = (0,0,0)
grey = (211,211,211)
white = (255,255,255)
#red = (220,100,100)
#green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
purple = (128,0,128)
yellowInBlackGuy = (241,203,121)


# Screen
screen = pygame.display.set_mode([width, height]) #,flags^FULLSCREEN,bits)
pygame.display.set_caption("Sparknight 2: The Sparkening")

lives_left = 3

# Create sprite group
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
exit_list = pygame.sprite.Group()
exit_doors_list = pygame.sprite.Group()
attack_sprites_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
overlay = Overlay()
enemy_list = pygame.sprite.Group()
blur_group = pygame.sprite.Group()



playerWidth = 30
playerHeight = 30
#Move player Position###
#Defines borders which player should not be able to pass
playerWidthBorder = playerWidth / 2 + 5 + 30
playerHeightBorder = playerHeight / 2 + 5 + 30
player = Player(playerWidth, playerHeight)
#enemy = Enemy(1200,600)

#Draws level
draw_map = Level("map1")

# Adds player to sprites list

all_sprites_list.add(player)
player_list.add(player)
all_sprites_list.add(overlay)
wall_list.add(wall_list)
blur_group.add(overlay)


obstacles_for_attacks = wall_list


def restart():
    global lives_left, all_sprites_list,wall_list,exit_list,exit_doors_list,player_list,overlay,enemy_list,player,draw_map
    lives_left = 3
    # Create sprite group
    all_sprites_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()
    exit_list = pygame.sprite.Group()
    exit_doors_list = pygame.sprite.Group()
    attack_sprites_list = pygame.sprite.Group()
    player_list = pygame.sprite.Group()
    overlay = Overlay()
    enemy_list = pygame.sprite.Group()

    player = Player(playerWidth, playerHeight)
    #enemy = Enemy(1200,600)

    #Draws level
    draw_map = Level("map1")
    

    # Adds player to sprites list

    all_sprites_list.add(player)
    player_list.add(player)

    all_sprites_list.add(overlay)

    wall_list.add(wall_list)

    obstacles_for_attacks = wall_list


#Music file for background Music
pygame.mixer.music.load('MerryChristmasMr_Lawrence.mp3')
# Game time for clock functions
clock = pygame.time.Clock()

# Fill background (Makes cicle, when loop screen.fill is commented)
#screen.fill(bg)

background = pygame.image.load("background2.jpg").convert()
background = pygame.transform.scale(background,(1440,900))
pygame.mixer.music.play(-1, 1.0)
# LOOP
done = False

#Hello elston

while not done:
            # Quit pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create object player
                button_pressed = pygame.mouse.get_pressed()
                #print button_pressed
            elif event.type == pygame.MOUSEBUTTONUP:
                if button_pressed[2]:
                    player.move()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.attack_Q()
                #if event.key == pygame.K_r:
                #    player.attack_R()
                elif event.key == pygame.K_w:
                    player.attack_W()
                elif event.key == pygame.K_c:
                    done = True
                elif event.key == pygame.K_ESCAPE:
                    overlay.main_menu()


        # Makes sure that the player should not be moving
        # And that the movement does not push them outside the border


        # fills background color
        screen.fill(bg)
        screen.blit(background,(0,0))
        # Call update function of sprites
        all_sprites_list.update()

        # Draw all sprites on screen
        all_sprites_list.draw(screen)

        wall_list.update()

        # Set tick rate to 60
        clock.tick(60)
        #toggle_fullscreen()
        # Redraw screen

        pygame.display.flip()

# Quit if loop is exited
pygame.mixer.music.stop()
pygame.quit()
