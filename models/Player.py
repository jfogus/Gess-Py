# Author:  Joshua Fogus
# Date:  5/27/20
# Description:  Creates a player for the Gess Game which maintains its color, stones, and rings.


class Player:
    """ Represents a player of the Gess game. Has no knowledge of any other classes.
        Maintains, updates, and provides information on its own list of rings, its
        stone marker, and its own color. Has one parameters, a stone, in the form
        of a character, either 'w' or 'b' """

    def __init__(self, stone):
        self._stone = stone
        self._color = ""
        self._rings = []

        # Sets the initial rings and color for each player
        if stone == "b":
            self._rings.append((17, 11))
            self._color = "BLACK"
        elif stone == "w":
            self._rings.append((2, 11))
            self._color = "WHITE"

    # TODO: Add stone tracking to the player.

    def get_stone(self):
        """ Has no parameters. Returns the player's stone as a string: 'w' or 'b' """
        return self._stone

    def get_color(self):
        """ Has no parameters. Returns the player's color as a string:
            "WHITE" or "BLACK" """
        return self._color

    def get_rings(self):
        """ Has no parameters. Returns a list of tuples indicating the locations of
            the centers of the player's rings in (row, col) format. """
        return self._rings

    def set_rings(self, rings):
        """ Receives a list of tuples indicating the locations of the centers of
            the player's rings in (row, col) format. Entirely replaces the previous
            list of rings with the new list of rings.  Returns nothing. """
        self._rings = rings

    def has_rings(self):
        """ Has no parameters. Returns True if the player has at least one ring,
            otherwise returns False. """
        if len(self._rings) > 0:
            return True

        return False


def main():
    """ This is not meant to be run as a script. Performs a simple test. """
    p = Player('b')
    print("Player rings:", p.get_rings())


if __name__ == "__main__":
    main()
