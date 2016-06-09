#!/usr/bin/python2

import pygame, random, math, sys
from pygame import *
from pygame import gfxdraw

class Game:
    def __init__(self):

        # Set the varibales for the game
        self.score = 0
        self.lives = 3

        # keeps Two font sizes
        self.font = pygame.font.SysFont("Arial", 12)
        self.losefont = pygame.font.SysFont("Arial", 30)

        # End Variable
        self.end = False
        
    def update(self):

        # Lets the user keep track of score and lives
        score_text = self.font.render("Score: " + str(self.score),2,white)
        screen.blit(score_text, (7,6))
        lives_text = self.font.render("Lives: " + str(self.lives),2,white)
        screen.blit(lives_text, (80,6))

        # What to do when the user does not have any lives
        if self.lives <= 0:
            self.lose()

    def lose(self):
        screen.fill(lose)
        lose_text = self.losefont.render("YOU LOSE",9,black)
        screen.blit(lose_text, (220,150))
        self.image = pygame.Surface([200,90])
        self.end = True
        
class Ball(pygame.sprite.Sprite):
    
    def __init__(self,rad):

        # Keeps the class as a sprite
        pygame.sprite.Sprite.__init__(self)
        
        # State velocity and initial position
        self.velocity = [6,6]
        self.angle = 120
        self.walls = None
        self.brick = None

        # Verbose values
        self.vel_x = self.velocity[0]
        self.vel_y = self.velocity[1]
        
        # State the surface to draw
        self.width = 14
        self.height = 18
        self.image = pygame.Surface([self.width,self.height])
        
        # Background fill
        self.image.fill(red)
        # Transparent the background
        self.image.set_colorkey(red)
        
        # Draw shiny ball with outline
        pygame.gfxdraw.filled_circle(self.image,6,8,5,black)
        pygame.gfxdraw.filled_circle(self.image,4,6,1,white)
        pygame.gfxdraw.circle(self.image,6,8,6,white)

        # Get the rectangle frame for image
        self.rect = self.image.get_rect()
        print self.rect

        # Initial X and Y values
        self.rect.x = 302
        self.rect.y = 615

    def reset_pos(self):

        # Should be same as initial
        self.rect.x = 302
        self.rect.y = 615
        # Reset the paddle
        player.reset_pos()
        
    def check_boundaries(self):

        # Should be done in one line of code
        # For python2 remove the comment below
        if self.rect.y > screen.get_height()+50:
           self.reset_pos()
           brickbreaker.lives -= 1
        elif self.rect.y < 0 + 24:
           self.vel_y = self.vel_y * -1
        if self.rect.x > screen.get_width() - 24:
           self.vel_x = self.vel_x * -1
        elif self.rect.x < 0 + 24:
           self.vel_x = self.vel_x * -1

    def bounce(self):

        # FIX (needs to work with angles)
        self.vel_y = (self.vel_y * -1) #*  1.2
        #self.vel_x = (self.vel_x * -1) #*  1.2

    def check_collisions(self):

        # check if the ball hits the paddle
        if player.rect.x < self.rect.x < player.rect.x + 65:
            if player.rect.y < self.rect.y < player.rect.y + 15:
                # calls bounce method from ball
		print player.rect
		print self.rect
                self.bounce()

# ------#------------------------------------------------------------------------------------
        # CATCH COLLISIONS 
        collision = pygame.sprite.spritecollide(self,self.brick,True)
        for c in collision:
            brickbreaker.score += 1
            ball.bounce()
            print(brickbreaker.score)
        #
# ------#------------------------------------------------------------------------------------
    def update(self):

        #pass
        # Checks position & bounds
        self.check_boundaries()
        self.check_collisions()

        # Adds Velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
   
                     
class Paddle(pygame.sprite.Sprite):

    def __init__(self):
        # DEFAULT
        pygame.sprite.Sprite.__init__(self)

        # Static Variables
        width = 65
        height = 15
        
        self.image = pygame.Surface([width,height])
        self.image.fill(red)
        #self.image.set_colorkey(red)
        
        # Draw Paddle
        pygame.draw.rect(self.image,paddle,[0,0,width,height])
        pygame.draw.rect(self.image,black,[0,0,width,height+1],3)
        pygame.draw.rect(self.image,white,[0,0,width,height-10])
        pygame.draw.rect(self.image,white,[0,0,width,height-12])

        # Get rectangle frame
        self.rect = self.image.get_rect()

        # Set Cords
        self.rect.x = 270
        self.rect.y = 627
        self.x = self.rect.x
        self.y = self.rect.y

        self.offscreen = False

    def move(self,direction):

        # Set how fast the paddle moves left of right
        # Can be int or float
        self.paddle_speed = 9.0

        # Move the paddle to the other side
        # of the screen when hiting borders

        if self.offscreen:
            if self.rect.x > screen.get_width() + 25:
                self.rect.x = 0
            elif self.rect.x < -65:
                self.rect.x = screen.get_width()

        else:
            if self.rect.x > screen.get_width()-100:
                  self.rect.x = screen.get_width()-100
            elif self.rect.x < +35:
                self.rect.x = 35
        # Move paddle left or right
        if (direction == "left"): 
            self.rect.x += -self.paddle_speed
        elif(direction == "right"):
            self.rect.x += self.paddle_speed

    def reset_pos(self):

        # Set the proper Codinates when reset
        self.rect.x = 270
        self.rect.y = 627

    def update(self):
        pass
        
class Wall(pygame.sprite.Sprite):

    def __init__(self,x,y,width,height,color,outline):
        
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        pygame.draw.rect(self.image,color,[0,0,width,height])
        # For bricks only
        if outline:
            pygame.draw.rect(self.image,black,[0,0,width,height], outline)
            
        self.rect = self.image.get_rect()
        # Where to position walls and bricks
        self.rect.x = x
        self.rect.y = y

# ------------------------------------------------
# GAME
# ------------------------------------------------

# initialize pygame
pygame.init()
pygame.font.init()

# define colors
black  = (0,0,0)
white  = (255,255,255)
red    = (255,0,0)
green  = (0,255,0)
blue   = (0,0,255)
bg     = (5,53,113)
border = (28,121,121)
b_brick= (204,102,0)
lose   = (204,195,183)
paddle = (163,163,163)

# set dimentions for window
width = 600
#height = 400
height = 700


# create window
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("Brickbreaker")

# Assign lists to sprite groups
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
brick_list = pygame.sprite.Group()

#-----------------------------------
# Creating walls
#-----------------------------------

# Width of wall
w_wall = 24

wall1 = Wall(0,0,w_wall,900,border,0)
wall_list.add(wall1)
all_sprites_list.add(wall1)

wall2 = Wall(600 - w_wall,0,w_wall,900,border,0)
wall_list.add(wall2)
all_sprites_list.add(wall2)

wall3 = Wall(0,0,600,w_wall,border,0)
wall_list.add(wall3)
all_sprites_list.add(wall3)

#wall4 = Wall(0,400 - w_wall,600,w_wall)
#wall_list.add(wall4)
#all_sprites_list.add(wall4)

#-----------------------------------
# Creating Bricks
#-----------------------------------

for b in range(0,500,50):
    # Create wall (X, Y, Width, Height, Color ,Outline)
    brick = Wall(50+b,40,50,20,b_brick,2)
    all_sprites_list.add(brick)
    brick_list.add(brick)
    brick = Wall(50+b,80,50,20,b_brick,2)
    all_sprites_list.add(brick)
    brick_list.add(brick)
    brick = Wall(50+b,120,50,20,b_brick,2)
    all_sprites_list.add(brick)
    brick_list.add(brick)
    brick = Wall(50+b,160,50,20,b_brick,2)
    all_sprites_list.add(brick)
    brick_list.add(brick)

# ----------------------------------
# Create objetcs
brickbreaker = Game()
ball = Ball(5)
player = Paddle()
ball.walls = wall_list
ball.brick = brick_list

# Add objects to groups
all_sprites_list.add(player,ball)

# Set game timer
clock = pygame.time.Clock()

# Move values Defaults
left  = False
right = False

# set loop
done  = False

# ------------------------------------------

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print (pygame.mouse.get_pos())

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            elif event.key == pygame.K_RIGHT:
                right = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            elif event.key == pygame.K_RIGHT:
                right = False
                # Allow paddle to move and reset from left to right
            elif event.key == pygame.K_i:
                player.offscreen = not player.offscreen
                
            

    if left:
        player.move("left")
    if right:
        player.move("right")
    if brickbreaker.end:
        from time import sleep
        sleep(3.0)
        done = True
                
    screen.fill(bg)

    all_sprites_list.update()
    
    all_sprites_list.draw(screen)

    brickbreaker.update()

    clock.tick(60)
    
    pygame.display.flip()

pygame.quit()
