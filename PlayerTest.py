# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Tests the Player class of the GessGame file.


from GessGame import Player
import unittest


class PlayerTest(unittest.TestCase):
    def test_get_stone_white(self):
        """ Tests making a white player. """
        p = Player('w')

        self.assertEqual('w', p.get_stone())

    def test_get_stone_black(self):
        """ Tests making a black player. """
        p = Player('b')

        self.assertEqual('b', p.get_stone())

    def test_get_color_white(self):
        """ Tests to get the long form color of a white player. """
        p = Player('w')

        self.assertEqual('WHITE', p.get_color())

    def test_get_color_black(self):
        """ Tests to get the long form color of a black player. """
        p = Player('b')

        self.assertEqual('BLACK', p.get_color())

    def test_get_rings1(self):
        """ Tests if the default ring will be returned for white. """
        p = Player('w')

        self.assertListEqual([(17, 11)], p.get_rings())

    def test_get_rings2(self):
        """ Tests if the default ring will be returned for black. """
        p = Player('b')

        self.assertListEqual([(2, 11)], p.get_rings())

    def test_has_rings1(self):
        """ Test confirming a player has rings. """
        p = Player('b')

        self.assertTrue(p.has_rings())

    def test_set_rings1(self):
        """ Test if a players ring can be changed. """
        p = Player('b')

        p.set_rings([(15, 17)])

        self.assertListEqual([(15, 17)], p.get_rings())

    def test_set_rings2(self):
        """ Test if a player can have multiple rings. """
        p = Player('w')

        p.set_rings([(14, 19), (12, 2)])

        self.assertListEqual([(14, 19), (12, 2)], p.get_rings())

    def test_set_rings3(self):
        """ Test if a players rings can be emptied. """
        p = Player('b')

        p.set_rings([])

        self.assertListEqual([], p.get_rings())

    def test_has_rings2(self):
        """ Test if a player has no rings. """
        p = Player('w')

        p.set_rings([])

        self.assertFalse(p.has_rings())

    def test_has_rings3(self):
        """ Test if a player has multiple rings. """
        p = Player('b')

        p.set_rings([(14, 19), (12, 2)])

        self.assertTrue(p.has_rings())


def main():
    """ Performs unit tests of the Player class for a Gess Game. """
    unittest.main()


if __name__ == "__main__":
    main()