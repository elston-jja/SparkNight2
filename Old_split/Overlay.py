import pygame

class Overlay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Declare base amount of lives
        self.mouseflip = False
        self.lives = 3
        # Initialize fonts
        pygame.font.init()
        # Create fontattributes in namespace
        self.font = pygame.font.SysFont("Calibri",20)
        self.options_type = pygame.font.SysFont("Calibri", 50)
        self.pause_type = pygame.font.SysFont("Calibri",80)
        # Display lives_text
        self.live_text = self.font.render("Lives: ",True,bg)
        # Surface created
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(bg)
        # Set the image of the heart
        self.hearts = pygame.image.load("ImagesAndSounds/heart.png").convert_alpha()
        self.hearts = pygame.transform.scale(self.hearts,(30,30))
        self.isPaused = False


    def update(self):
        '''
        Draw the amount of lives left
        '''
        screen.blit(self.live_text, (40,40))
        if self.lives == 3:
            #Draws three hearts
            screen.blit(self.hearts,(40, 60))
            screen.blit(self.hearts,(80, 60))
            screen.blit(self.hearts,(120, 60))
        if self.lives == 2:
            #Draws 2
            screen.blit(self.hearts,(40, 60))
            screen.blit(self.hearts,(80, 60))
        if self.lives == 1:
            #Please use your brain
            screen.blit(self.hearts,(40, 60))
        if self.lives == 0:
            # resets all values and starts from the beginning
            restart()

    def main_menu(self):
        '''
        Creates a menu loop inside game, and helps to keep events
        '''
        # Text to display
        self.screen_text = ("Press ESC to resume")
        self.music_toggle = ('Press "u" to toggle music')
        self.mouse_toggle = ('Press "y" to toggle mouse action flip')
        self.fullscreen_toggle = ('Press "i" to toggle fullscreen')
        self.quitswitch = ('Press "c" to quit ')
        # render all the types of text | has AA and color: black
        self.pause_render = self.pause_type.render(self.screen_text,True,bg)
        self.options_render = self.options_type.render(self.music_toggle, True, bg)
        self.mouse_render = self.options_type.render(self.mouse_toggle,True,bg)
        self.fullscreen_render = self.options_type.render(self.fullscreen_toggle,True,bg)
        self.quitswitch_render = self.options_type.render(self.quitswitch,True,bg)
        # Take new image when paused and load to be used
        pygame.image.save(screen,"ImagesAndSounds/current_bg.jpg")
        frame = pygame.image.load("ImagesAndSounds/current_bg.jpg")
        # Run nested loop for menu events, waiting for esc key to unlock
        inMenu = True
        while inMenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    global done
                    done = True
                    inMenu = False
                elif event.type == pygame.KEYDOWN:
                    # Unpause
                    if event.key == pygame.K_ESCAPE:
                        inMenu = False
                    # Toggle music
                    elif event.key == pygame.K_u:
                        self.isPaused = not self.isPaused
                        if self.isPaused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                            self.isPaused = False
                    # Toggle mouse flip from 2 to 0
                    elif event.key == pygame.K_y:
                        self.mouseflip = not self.mouseflip
                    # Toggle fullscreen
                    elif event.key == pygame.K_i:
                        flags=screen.get_flags()
                        if screen.get_flags() & pygame.FULLSCREEN:
                            pygame.display.set_mode([1440,870], pygame.RESIZABLE)
                        else:
                            pygame.display.set_mode([1440,870], pygame.FULLSCREEN)
                    elif event.key == pygame.K_c:
                        inMenu = False
                        done = True

            self.pause_type = pygame.font.SysFont("Calibri",80)
            self.pause_render = self.pause_type.render(self.screen_text,True,bg)
            self.options_type = pygame.font.SysFont("Calibri", 50)
            self.options_render = self.options_type.render(self.music_toggle, True, bg)
            # Draw blurred background and font on top

            screen.blit(self.blurSurf(frame,15),(0,0))
            screen.blit(self.pause_render, (450,90))
            screen.blit(self.options_render, (530, 300))
            screen.blit(self.mouse_render, (450, 400))
            screen.blit(self.fullscreen_render,(500,500))
            screen.blit(self.quitswitch_render,(590,600))
            clock.tick(60)
            pygame.display.flip()

    def intro_screen(self):
        '''
        Creates intro screen -NOT IMPLEMENTED
        '''
        try:
         intro_graphic = False
         intro = True
         while intro :
             for event.type in pygame.event_get():
                 if event.key == pygame.K_RETURN:
                     pass
                 if event.key == pygame.K_ESC:
                     pass
                 if event.key == pygame.QUIT:
                     pygame.quit()
        except:
            raise NotImplemented("Not done")


    def blurSurf(self,surface, amount):
        """
        Method used for blurring the background (Look at Source)
        -> look at source: http://www.akeric.com/blog/?p=720
        """
        #Takes screenshot of screen
        scale = 1.0/float(amount)
        surface_size = surface.get_size()
        scale_size = (int(surface_size[0]*scale), int(surface_size[1]*scale))
        #Transforms it and add blurring effect
        surface_soft1 = pygame.transform.smoothscale(surface, scale_size)
        surface_soft_final = pygame.transform.smoothscale(surface_soft1, surface_size)
        return surface_soft_final

