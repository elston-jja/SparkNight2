
class Level:
    '''
    Checks the level and display it accoringly
    '''
    def __init__(self,level):
        # State the initial level number
        # Value not needed except for verbosity
        self.level = level
        # Default x y starting block cordinates
        self.x = 0
        self.y = 0
        # Creates object called "list of maps" and I can call all maps
        # From the lists in the maps_list file
        list_of_maps = maps()
        # Get the level from maps_list and load it into the interpreter
        # Change the current level to the list varible in the maps_list file
        exec_var = "self.current_level = list_of_maps." + str(self.level)
        exec (exec_var)
        # Get the lines/rows from each variable in the list
        self.make_level()

    def make_level(self):

        for line_row in self.current_level:
            # Check each character in the row
            for char in line_row:
                # if the character is a 'w' then add a wall block (30,30)
                if char == "w":
                    wall = Wall(self.x,self.y,grey)
                    wall_list.add(wall)
                    all_sprites_list.add(wall)
                # If the character is an 'e' then add an wall block
                # That when collided can cause to exit
                # As it is added to the exitdoor list (change var is need be)
                if char == "e":
                    exit_ = Wall(self.x,self.y,red)
                    wall_list.add(exit_)
                    exit_list.add(exit_)
                    all_sprites_list.add(exit_)
                elif char == "P":
                    player.rect.x = self.x
                    player.rect.y = self.y
                elif char == "E":
                    enemy = Enemy(self.x,self.y)
                    enemy_list.add(enemy)
                    all_sprites_list.add(enemy)
                    # When drawing each block
                    # (Character in row)
                    # Move 30px to the right
                elif char == "B":
                    boss_enemy = BossEnemy(self.x,self.y)
                    enemy_list.add(boss_enemy)
                    all_sprites_list.add(boss_enemy)
                self.x+= 30
                # When moving down to next row change the Y by 30
                # Reset th X
            self.y+=30
            self.x = 0

