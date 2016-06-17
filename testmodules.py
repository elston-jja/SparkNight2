import unittest
from main import *

class TestPosition(unittest.TestCase):

    def testsize(self):
        player = Player(30,30)
        player.rect.x = 150
        self.assertEqual(self.get_rect.x, 150)

if __name__ == '__main__':
    unittest.main()
