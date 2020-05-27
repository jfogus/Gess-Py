# Author:  Joshua Fogus
# Date:  5/22/20
# Description:  Creates an implementation of the Gess Game


def main():
    """ This is not meant to be run as a script. Performs simple tests. """
    b = Board()
    p = Player('b')
    b.print_board()


if __name__ == '__main__':
    main()

# Board 18 x 18
# Players x2 (b/w)
# each player 43 stones
# pieces (3x3 squares that contain stones of one color)
#  - A piece can extend outside of the board, center must be on the board
# black goes first, turns taken
# The whole piece (all stones w/in) moves as a unit
#  - If stone in center of piece
#    - piece can move any unobstructed distance
#  - If center is empty
#    - Can move <= 3 squares
#  - Regardless of center piece
#    - direction is limited by stones on the perimeter
#    - diagonal is included in directions movable
#  - Movement is halted as soon as the footprint overlaps any other stones (regardless of color)
#    - Overlapped stones of both colors are removed permanently from the game
#  - A piece may move partially beyond the board in which case any stones out of bounds are eliminated
# Footprint of a piece is its 3x3 region (not just where the stones are)
# Pieces are defined by their central square
# The goal is to eliminate the opponent's last ring
#  - A ring is a ring of eight stones around an empty center
#  - Each player starts w/ 1 ring but may make more
# Cannot make a move that breaks your own last ring
