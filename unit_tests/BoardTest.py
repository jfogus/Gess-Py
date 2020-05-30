# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Unit tests for the Board of a Gess game


from Gess import Board, Player, IllegalMove
import unittest


class BoardTest(unittest.TestCase):
    def test_get_squares(self):
        """ Tests that a board is initially set up properly. """
        b = Board()

        expected_board = [
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "b", "", "b", "", "b", "b", "b", "b", "b", "b", "b", "b", "", "b", "", "b", "", ""],
            ["", "b", "b", "b", "", "b", "", "b", "b", "b", "b", "", "b", "", "b", "", "b", "b", "b", ""],
            ["", "", "b", "", "b", "", "b", "b", "b", "b", "b", "b", "b", "b", "", "b", "", "b", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "b", "", "", "b", "", "", "b", "", "", "b", "", "", "b", "", "", "b", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "w", "", "", "w", "", "", "w", "", "", "w", "", "", "w", "", "", "w", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["", "", "w", "", "w", "", "w", "w", "w", "w", "w", "w", "w", "w", "", "w", "", "w", "", ""],
            ["", "w", "w", "w", "", "w", "", "w", "w", "w", "w", "", "w", "", "w", "", "w", "w", "w", ""],
            ["", "", "w", "", "w", "", "w", "w", "w", "w", "w", "w", "w", "w", "", "w", "", "w", "", ""],
            ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        ]

        self.assertListEqual(expected_board, b.get_squares())

    def test_get_delta1(self):
        """ Tests that a positive delta can be returned properly. """
        b = Board()

        origin = (2, 2)
        target = (3, 3)

        self.assertTupleEqual((1, 1), b.get_delta(origin, target))

    def test_get_delta2(self):
        """ Tests that a negative delta can be returned properly. """
        b = Board()

        origin = (2, 2)
        target = (1, 1)

        self.assertTupleEqual((-1, -1), b.get_delta(origin, target))

    def test_place_piece1(self):
        """ Test placing a piece with two arguments. """
        b = Board()

        origin = {
            (3, 1): "", (3, 2): "b", (3, 3): "",
            (2, 1): "b", (2, 2): "b", (2, 3): "b",
            (1, 1): "", (1, 2): "b", (1, 3): ""
        }
        target = {
            (11, 1): "", (11, 2): "", (11, 3): "",
            (10, 1): "", (10, 2): "", (10, 3): "",
            (9, 1): "", (9, 2): "", (9, 3): ""
        }
        expected_piece = {
            (11, 1): "", (11, 2): "b", (11, 3): "",
            (10, 1): "b", (10, 2): "b", (10, 3): "b",
            (9, 1): "", (9, 2): "b", (9, 3): ""
        }

        b.place_piece(origin, target)

        self.assertDictEqual(expected_piece, b.get_piece((10, 2)))

    def test_place_piece2(self):
        """ Test placing a piece with one argument. """
        b = Board()

        target = {
            (11, 1): "", (11, 2): "b", (11, 3): "",
            (10, 1): "b", (10, 2): "b", (10, 3): "b",
            (9, 1): "", (9, 2): "b", (9, 3): ""
        }
        expected_piece = {
            (11, 1): "", (11, 2): "b", (11, 3): "",
            (10, 1): "b", (10, 2): "b", (10, 3): "b",
            (9, 1): "", (9, 2): "b", (9, 3): ""
        }

        b. place_piece(target)

        self.assertDictEqual(expected_piece, b.get_piece((10, 2)))

    def test_in_gutter1(self):
        """ Test if handles a square not in the gutter. """
        b = Board()

        self.assertFalse(b.in_gutter((5, 7)))

    def test_in_gutter2(self):
        """ Test if in column a. """
        b = Board()

        self.assertTrue(b.in_gutter((5, 0)))

    def test_in_gutter3(self):
        """ Test if in column t. """
        b = Board()

        self.assertTrue(b.in_gutter((5, 19)))

    def test_in_gutter4(self):
        """ Test if in row 0. """
        b = Board()

        self.assertTrue(b.in_gutter((0, 5)))

    def test_in_gutter5(self):
        """ Test if in row 20. """
        b = Board()

        self.assertTrue(b.in_gutter((19, 5)))

    def test_to_indices(self):
        """ Tests if a letter/number combination can be converted. """
        b = Board()

        self.assertTupleEqual((2, 2), b.to_indices("c3"))

    def test_get_piece(self):
        """ Tests retrieving a piece. """
        b = Board()

        expected_piece = {
            (3, 1): "", (3, 2): "b", (3, 3): "",
            (2, 1): "b", (2, 2): "b", (2, 3): "b",
            (1, 1): "", (1, 2): "b", (1, 3): ""
        }

        self.assertDictEqual(expected_piece, b.get_piece((2, 2)))

    def test_clear_gutter1(self):
        """ Tests that column a is cleared. """
        b = Board()

        target = {
            (5, 0): "b", (5, 1): "b", (5, 2): "b",
            (4, 0): "b", (4, 1): "b", (4, 2): "b",
            (3, 0): "b", (3, 1): "b", (3, 2): "b"
        }

        b.place_piece(target)
        b.clear_gutter()

        expected_piece = {
            (5, 0): "", (5, 1): "b", (5, 2): "b",
            (4, 0): "", (4, 1): "b", (4, 2): "b",
            (3, 0): "", (3, 1): "b", (3, 2): "b"
        }

        self.assertDictEqual(expected_piece, b.get_piece((4, 1)))

    def test_clear_gutter2(self):
        """ Tests that column t is cleared. """
        b = Board()

        target = {
            (5, 17): "", (5, 18): "b", (5, 19): "b",
            (4, 17): "", (4, 18): "b", (4, 19): "b",
            (3, 17): "", (3, 18): "b", (3, 19): "b"
        }

        b.place_piece(target)
        b.clear_gutter()

        expected_piece = {
            (5, 17): "", (5, 18): "b", (5, 19): "",
            (4, 17): "", (4, 18): "b", (4, 19): "",
            (3, 17): "", (3, 18): "b", (3, 19): ""
        }

        self.assertDictEqual(expected_piece, b.get_piece((4, 18)))

    def test_clear_gutter3(self):
        """ Tests that row 1 is cleared. """
        b = Board()

        target = {
            (2, 5): "", (2, 6): "b", (2, 7): "b",
            (1, 5): "", (1, 6): "b", (1, 7): "b",
            (0, 5): "b", (0, 6): "b", (0, 7): "b"
        }

        b.place_piece(target)
        b.clear_gutter()

        expected_piece = {
            (2, 5): "", (2, 6): "b", (2, 7): "b",
            (1, 5): "", (1, 6): "b", (1, 7): "b",
            (0, 5): "", (0, 6): "", (0, 7): ""
        }

        self.assertDictEqual(expected_piece, b.get_piece((1, 6)))

    def test_clear_gutter4(self):
        """ Tests that row 20 is cleared. """
        b = Board()

        target = {
            (19, 5): "b", (19, 6): "b", (19, 7): "b",
            (18, 5): "", (18, 6): "b", (18, 7): "b",
            (17, 5): "b", (17, 6): "b", (17, 7): ""
        }

        b.place_piece(target)
        b.clear_gutter()

        expected_piece = {
            (19, 5): "", (19, 6): "", (19, 7): "",
            (18, 5): "", (18, 6): "b", (18, 7): "b",
            (17, 5): "b", (17, 6): "b", (17, 7): ""
        }

        self.assertDictEqual(expected_piece, b.get_piece((18, 6)))

    def test_is_player_piece1(self):
        """ Tests if a black piece can be identified for the black player. """
        b = Board()
        p = Player('b')

        piece = b.get_piece((2, 2))

        self.assertTrue(b.is_player_piece(p, piece))

    def test_is_player_piece2(self):
        """ Tests if a white piece can be identified for the white player. """
        b = Board()
        p = Player('w')

        piece = b.get_piece((17, 2))

        self.assertTrue(b.is_player_piece(p, piece))

    def test_is_player_piece3(self):
        """ Tests if a black piece is not returned for the white player. """
        b = Board()
        p = Player('w')

        piece = b.get_piece((2, 2))

        self.assertFalse(b.is_player_piece(p, piece))

    def test_is_player_piece4(self):
        """ Tests if a white piece is not returned for the black player. """
        b = Board()
        p = Player('b')

        piece = b.get_piece((17, 2))

        self.assertFalse(b.is_player_piece(p, piece))

    def test_is_player_piece5(self):
        """ Tests if an empty piece is handled properly for a white player. """
        b = Board()
        p = Player('w')

        piece = b.get_piece((10, 10))

        self.assertFalse(b.is_player_piece(p, piece))

    def test_is_player_piece6(self):
        """ Tests if an empty piece is handled properly for a black player. """
        b = Board()
        p = Player('b')

        piece = b.get_piece((10, 10))

        self.assertFalse(b.is_player_piece(p, piece))

    def test_is_player_piece7(self):
        """ Tests if a contended piece is handled properly for a white player. """
        b = Board()
        p = Player('b')

        target = {
            (5, 1): "", (5, 2): "w", (5, 3): "w",
            (4, 1): "w", (4, 2): "w", (4, 3): "w",
            (3, 1): "w", (3, 2): "w", (3, 3): "w"
        }

        b.place_piece(target)
        piece = b.get_piece((2, 2))

        self.assertFalse(b.is_player_piece(p, piece))

    def test_is_player_piece8(self):
        """ Tets if a contended piece is handled properly for a black player. """
        b = Board()
        p = Player('w')

        target = {
            (5, 1): "", (5, 2): "w", (5, 3): "w",
            (4, 1): "w", (4, 2): "w", (4, 3): "w",
            (3, 1): "w", (3, 2): "w", (3, 3): "w"
        }

        b.place_piece(target)
        piece = b.get_piece((2, 2))

        self.assertFalse(b.is_player_piece(p, piece))

    def test_is_legal_direction1(self):
        """ Tests if NW is a legal direction. """
        b = Board()

        piece = b.get_piece((2, 3))
        delta = (1, -1)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction2(self):
        """ Tests if N is a legal direction. """
        b = Board()

        piece = b.get_piece((2, 2))
        delta = (1, 0)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction3(self):
        """ Tests if NE is a legal direction."""
        b = Board()

        piece = b.get_piece((2, 3))
        delta = (1, 1)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction4(self):
        """ Tests if W is a legal direction. """
        b = Board()

        piece = b.get_piece((2, 2))
        delta = (0, -1)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction5(self):
        """ Tests if E is a legal direction. """
        b = Board()

        piece = b.get_piece((2, 2))
        delta = (0, 1)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction6(self):
        """ Tests if SW is a legal direction. """
        b = Board()

        piece = b.get_piece((2, 3))
        delta = (-1, -1)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction7(self):
        """ Tests if S is a legal direction. """
        b = Board()

        piece = b.get_piece((2, 2))
        delta = (-1, 0)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction8(self):
        """ Tests if SE is a legal direction. """
        b = Board()

        piece = b.get_piece((2, 3))
        delta = (-1, 1)

        self.assertTrue(b.is_legal_direction(piece, delta))

    def test_is_legal_direction9(self):
        """ Tests if generally illegal direction is handled properly. """
        b = Board()

        piece = b.get_piece((2, 3))
        delta = (1, 8)

        self.assertFalse(b.is_legal_direction(piece, delta))

    def test_is_legal_direction10(self):
        """ Tests if illegal direction for the piece is handled properly."""
        b = Board()

        piece = b.get_piece((2, 3))
        delta = (1, 0)

        self.assertFalse(b.is_legal_direction(piece, delta))

    def test_is_legal_distance1(self):
        """ Tests a legal distance due to directional stone. """
        b = Board()

        piece = b.get_piece((5, 2))
        delta = (3, 0)

        self.assertTrue(b.is_legal_distance(piece, delta))

    def test_is_legal_distance2(self):
        """ Tests an illegal distance due to no central stone. """
        b = Board()

        piece = b.get_piece((5, 2))
        delta = (4, 0)

        self.assertFalse(b.is_legal_distance(piece, delta))

    def test_is_legal_distance3(self):
        """ Tests a legal distance due to central stone. """
        b = Board()

        piece = b.get_piece((6, 2))
        delta = (5, 0)

        self.assertTrue(b.is_legal_distance(piece, delta))

    def test_is_legal_distance4(self):
        """ Tests illegal distance due to collision with opposing piece. """
        b = Board()

        piece = b.get_piece((6, 2))
        delta = (8, 0)

        self.assertFalse(b.is_legal_distance(piece, delta))

    def test_is_legal_distance5(self):
        """ Tests illegal distance due to collision with allied piece. """
        b = Board()

        piece = b.get_piece((2, 2))
        delta = (0, 3)

        self.assertFalse(b.is_legal_distance(piece, delta))

    def test_is_legal_distance6(self):
        """ Tests legal distance with capture. """
        b = Board()

        piece = b.get_piece((6, 2))
        delta = (6, 0)

        self.assertTrue(b.is_legal_distance(piece, delta))

    def test_check_for_rings1(self):
        """ Tests the default rings are properly identified. """
        b = Board()

        expected_rings = {
            (2, 11): 'b',
            (17, 11): 'w'
        }

        self.assertDictEqual(expected_rings, b.check_for_rings())

    def test_check_for_rings2(self):
        """ Tests that white rings will be added. """
        b = Board()

        target = {
            (18, 3): "", (18, 4): "w", (18, 5): "w",
            (17, 3): "w", (17, 4): "w", (17, 5): "w",
            (16, 3): "", (16, 4): "w", (16, 5): "w"
        }

        b.place_piece(target)

        expected_rings = {
            (17, 6): 'w',
            (2, 11): 'b',
            (17, 11): 'w'
        }

        self.assertDictEqual(expected_rings, b.check_for_rings())

    def test_check_for_rings3(self):
        """ Test that black rings will be added. """
        b = Board()

        target = {
            (3, 3): "", (3, 4): "b", (3, 5): "b",
            (2, 3): "b", (2, 4): "b", (2, 5): "b",
            (1, 3): "", (1, 4): "b", (1, 5): "b"
        }

        b.place_piece(target)

        expected_rings = {
            (2, 6): 'b',
            (2, 11): 'b',
            (17, 11): 'w'
        }

        self.assertDictEqual(expected_rings, b.check_for_rings())

    def test_check_for_rings4(self):
        """ Test that mixed color rings are not identified. """
        b = Board()

        target = {
            (3, 3): "", (3, 4): "w", (3, 5): "w",
            (2, 3): "w", (2, 4): "w", (2, 5): "w",
            (1, 3): "", (1, 4): "w", (1, 5): "w"
        }

        b.place_piece(target)

        expected_rings = {
            (2, 11): 'b',
            (17, 11): 'w'
        }

        self.assertDictEqual(expected_rings, b.check_for_rings())

    def test_move_piece1(self):
        """ Test a move from the the gutter. """
        b = Board()
        p = Player('b')

        error = False
        try:
            b.move_piece(p, 'a2', 'b2')
        except IllegalMove:
            error = True

        self.assertTrue(error)

    def test_move_piece2(self):
        """ Test a move to the gutter. """
        b = Board()
        p = Player('b')

        error = False
        try:
            b.move_piece(p, 'c3', 'c1')
        except IllegalMove:
            error = True

        self.assertTrue(error)

    def test_move_piece3(self):
        """ Test a move of the wrong color piece. """
        b = Board()
        p = Player('b')

        error = False
        try:
            b.move_piece(p, 'c17', 'c16')
        except IllegalMove:
            error = True

        self.assertTrue(error)

    def test_move_piece4(self):
        """ Test a move in an illegal direction. """
        b = Board()
        p = Player('b')

        error = False
        try:
            b.move_piece(p, 'd3', 'd4')
        except IllegalMove:
            error = True

        self.assertTrue(error)

    def test_move_piece5(self):
        """ Test a move of an illegal distance. """
        b = Board()
        p = Player('b')

        error = False
        try:
            b.move_piece(p, 'c6', 'c12')
        except IllegalMove:
            error = True

        self.assertTrue(error)

    def test_move_piece6(self):
        """ Test a legal move. """
        b = Board()
        p = Player('b')

        expected_piece = {
            (4, 1): "", (4, 2): "b", (4, 3): "",
            (3, 1): "b", (3, 2): "b", (3, 3): "b",
            (2, 1): "", (2, 2): "b", (2, 3): ""
        }

        b.move_piece(p, 'c3', 'c4')

        self.assertDictEqual(expected_piece, b.get_piece((3, 2)))

    def test_remove_piece(self):
        """ Tests that a piece is removed. """
        b = Board()

        square = b.to_indices('j3')
        piece = b.get_piece(square)
        b.remove_piece(piece)

        expected_piece = {
            (3, 8): "", (3, 9): "", (3, 10): "",
            (2, 8): "", (2, 9): "", (2, 10): "",
            (1, 8): "", (1, 9): "", (1, 10): ""
        }

        self.assertDictEqual(expected_piece, b.get_piece(square))

def main():
    unittest.main()


if __name__ == "__main__":
    main()