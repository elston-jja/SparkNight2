'''
Testing file for main function of Spark Night game
@author: Elston Almeida and Lance Pereira
@date: June 17, 2016
@course: ICS3U1
'''

import unittest
from main import *

class Testmain(unittest.TestCase):
    pygame.init()
    screen = pygame.display.set_mode([width, height],pygame.FULLSCREEN)
    pygame.display.set_caption("Sparknight 2: The Sparkening")
    player = Player(30,30)
    player.xvelocity = 1
    player.yvelocity = -1
    player.remainderxvelocity = 1
    player.remainderyvelocity = -1

    player.rect.x = 1
    player.rect.y = 1

    def test_move(self):
        player.move()
        self.assertEqual([player.rect.x,player.rect.y],[145,145])

    def test_changeVelocityAfterCollision(self):
        player.xvelocity = 5
        player.yvelocity = -10
        player.remainderxvelocity = 4
        player.remainderyvelocity = -3
        player.changeVelocityAfterCollision()
        self.assertEqual(player.xvelocity,-1)
        self.assertEqual(player.yvelocity,1)
        self.assertEqual(player.remainderxvelocity,-1)
        self.assertEqual(player.remainderyvelocity,1)

if __name__ == '__main__':
    unittest.main()
