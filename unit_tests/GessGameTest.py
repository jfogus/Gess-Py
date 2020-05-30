# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Unit tests for the GessGame class of the Gess Game

from Gess import GessGame, IllegalMove
import unittest


class GessGameTest(unittest.TestCase):
    def test_get_game_state(self):
        """ Tests returning the game state. """
        g = GessGame()

        self.assertEqual('UNFINISHED', g.get_game_state())

    def test_get_active_player(self):
        """ Tests returning the active player. """
        g = GessGame()

        self.assertEqual('b', g.get_active_player().get_stone())

    def test_resign_game(self):
        """ Tests resigning the game as the active player. """
        g = GessGame()

        g.resign_game()

        self.assertEqual('WHITE_WON', g.get_game_state())

    def test_make_move1(self):
        """ Tests trying to make a move after the game is finished. """
        g = GessGame()

        g.make_move('f6', 'f9')    # black move
        g.make_move('l15', 'l12')  # white move
        g.make_move('f9', 'f12')   # black move
        g.make_move('l12', 'l9')   # white move
        g.make_move('f12', 'f13')  # black move
        g.make_move('l9', 'l8')    # white move
        g.make_move('f15', 'f14')  # black move
        g.make_move('l8', 'l5')    # white move

        response = g.make_move('f14', 'f13')

        self.assertFalse(response)

    def test_make_move2(self):
        """ Tests handling an illegal move. """
        g = GessGame()

        self.assertFalse(g.make_move('c6', 'd7'))

    def test_make_move3(self):
        """ Tests destroying the last ring as the active player. """
        g = GessGame()

        self.assertFalse(g.make_move('j3', 'j5'))

    def test_make_move4(self):
        """ Tests completing a successful move. """
        g = GessGame()

        self.assertFalse(g.make_move('c7', 'c8'))

    def test_make_move5(self):
        """ Tests making a black move to the NW. """
        g = GessGame()

        self.assertTrue(g.make_move('m6', 'l7'))

    def test_make_move6(self):
        """ Tests making a black move to the N. """
        g = GessGame()

        self.assertTrue(g.make_move('l6', 'l7'))

    def test_make_move7(self):
        """ Tests making a black move to the NE. """
        g = GessGame()

        self.assertTrue(g.make_move('k6', 'l7'))

    def test_make_move8(self):
        """ Tests making a black move to the W. """
        g = GessGame()

        self.assertTrue(g.make_move('m7', 'l7'))

    def test_make_move9(self):
        """ Tests making a black move to the E. """
        g = GessGame()

        self.assertTrue(g.make_move('k7', 'l7'))

    def test_make_move10(self):
        """ Tests making a black move to the SW. """
        g = GessGame()

        self.assertTrue(g.make_move('m8', 'l7'))

    def test_make_move11(self):
        """ Tests making a black move to the S. """
        g = GessGame()

        self.assertTrue(g.make_move('l8', 'l7'))

    def test_make_move12(self):
        """ Tests making a black move to the SE. """
        g = GessGame()

        self.assertTrue(g.make_move('k8', 'l7'))

    def test_make_move13(self):
        """ Tests making a white move to the NW. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('d13', 'c14'))

    def test_make_move14(self):
        """ Tests making a white move to the N. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('c13', 'c14'))

    def test_make_move15(self):
        """ Tests making a white move to the NE. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('b13', 'c14'))

    def test_make_move16(self):
        """ Tests making a white move to the W. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('d14', 'c14'))

    def test_make_move17(self):
        """ Tests making a white move to the E. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('b14', 'c14'))

    def test_make_move18(self):
        """ Tests making a white move to the SW. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('d15', 'c14'))

    def test_make_move19(self):
        """ Tests making a white move to the S. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('c15', 'c14'))

    def test_make_move20(self):
        """ Tests making a white move to the SE. """
        g = GessGame()

        g.make_move('k8', 'l7')
        self.assertTrue(g.make_move('b15', 'c14'))

    def test_update_rings1(self):
        """ Test adding a new ring for white. """
        g = GessGame()

        target = {
            (18, 3): "", (18, 4): "w", (18, 5): "w",
            (17, 3): "w", (17, 4): "w", (17, 5): "w",
            (16, 3): "", (16, 4): "w", (16, 5): "w"
        }

        g._board.place_piece(target)
        g.update_rings()

        self.assertListEqual([(17, 6), (17, 11)], g._players[1].get_rings())

    def test_update_rings2(self):
        """ Test adding a new ring for black. """
        g = GessGame()

        target = {
            (3, 3): "", (3, 4): "b", (3, 5): "b",
            (2, 3): "b", (2, 4): "b", (2, 5): "b",
            (1, 3): "", (1, 4): "b", (1, 5): "b"
        }

        g._board.place_piece(target)
        g.update_rings()

        self.assertListEqual([(2, 6), (2, 11)], g._players[0].get_rings())


    def test_update_rings3(self):
        """ Test removing a ring for white. """
        g = GessGame()

        target = {
            (18, 8): "", (18, 9): "w", (18, 10): "",
            (17, 8): "w", (17, 9): "w", (17, 10): "",
            (16, 8): "", (16, 9): "w", (16, 10): ""
        }

        g._board.place_piece(target)
        g.update_rings()

        self.assertListEqual([], g._players[1].get_rings())

    def test_update_rings4(self):
        """ Test removing a ring for black. """
        g = GessGame()

        target = {
            (3, 8): "", (3, 9): "b", (3, 10): "",
            (2, 8): "b", (2, 9): "b", (2, 10): "",
            (1, 8): "", (1, 9): "b", (1, 10): ""
        }

        g._board.place_piece(target)
        error = False
        try:
            g.update_rings()
        except IllegalMove:
            error = True

        self.assertTrue(error)

    def test_switch_turn1(self):
        """ Test switching the turn to the white player. """
        g = GessGame()

        g.switch_turn()

        self.assertEqual(g._players[1], g.get_active_player())

    def test_switch_turn2(self):
        """ Test switching the turn back to the black player. """
        g = GessGame()

        g.switch_turn()
        g.switch_turn()

        self.assertEqual(g._players[0], g.get_active_player())

    def test_check_win_condition1(self):
        """ Tests that a win condition is properly updated for white. """
        g = GessGame()
        g._players[1].set_rings([])

        g.check_win_condition()

        self.assertEqual('BLACK_WON', g.get_game_state())

    def test_check_win_condition2(self):
        """ Tests that a win condition is properly updated for black. """
        g = GessGame()
        g._players[0].set_rings([])

        g.check_win_condition()

        self.assertEqual('WHITE_WON', g.get_game_state())

    def test_check_win_condition3(self):
        """ Tests a natural win for the black player. """
        g = GessGame()

        g.make_move('l6', 'l9')    # black move
        g.make_move('c15', 'c12')  # white move
        g.make_move('l9', 'l12')   # black move
        g.make_move('c12', 'c9')   # white move
        g.make_move('l12', 'l13')  # black move
        g.make_move('c9', 'c8')    # white move
        g.make_move('l13', 'l16')  # black move

        self.assertEqual('BLACK_WON', g.get_game_state())

    def test_check_win_condition4(self):
        """ Tests a natural win for the white player. """
        g = GessGame()

        g.make_move('f6', 'f9')    # black move
        g.make_move('l15', 'l12')  # white move
        g.make_move('f9', 'f12')   # black move
        g.make_move('l12', 'l9')   # white move
        g.make_move('f12', 'f13')  # black move
        g.make_move('l9', 'l8')    # white move
        g.make_move('f15', 'f14')  # black move
        g.make_move('l8', 'l5')    # white move

        self.assertEqual('WHITE_WON', g.get_game_state())


def main():
    """ Runs unit tests for the GessGame class. """
    unittest.main()


if __name__ == "__main__":
    main()