import Enemy

class BossEnemy(Enemy):

    def __init__(self,spawnx,spawny):
        '''
        Explanation of attributes in Parent class
        '''
        Player.__init__(self,spawnx,spawny)
        self.health = 300
        #self.image = ""
        self.enemey_collide = pygame.sprite.spritecollide(self, enemy_list, False)
        self.player_collide = pygame.sprite.spritecollide(self, player_list, False)
        self.attack_collide = pygame.sprite.spritecollide(self, attack_sprites_list, False)
        self.imageMasterSprite = pygame.image.load("ImagesAndSounds/pickachu.png").convert()
        self.imageMasterSprite = pygame.transform.scale(self.imageMasterSprite, (80,80))
        #self.imageMasterSprite = pygame.transform.rotate(self.imageMasterSprite, 180)
        self.imageSprite = self.imageMasterSprite
        self.imageSprite.set_colorkey(white)
        self.isBoss = True

    def get_pos(self):
        #Done to overide the rotation of boss, as boss rotations make it too dangerous
        pass

    def attack_Q(self):
        '''
        Creates the Q electricity ball attack, and projects
        it to wherever the mouse was
        '''
        orb = ElectricityOrb(True)
        attack_sprites_list.add(orb)
        all_sprites_list.add(orb)

    def update(self):
        self.angle_move = 0
        self.attack_Q()
        Player.update(self)
