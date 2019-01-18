"""An implementation of stonehenge."""
from game import Game
from stonehengestate import StonehengeState


class StonehengeGame(Game):
    """
    Class for a Stonehengegame to be played with two players.
    Note: Docstring examples are omitted since they require
    user input
    """

    def __init__(self, p1_starts):
        """
        Initialize this Game, using p1_starts to find who the first player is.

        :param p1_starts: A boolean representing whether Player 1 is the first
                          to make a move.
        :type p1_starts: bool
        """
        # todo: do you have to enforce the side_length 1-5 rule here?
        side_length = int(input("Enter the side length of the board: "))
        self.current_state = StonehengeState(p1_starts, side_length)

    def get_instructions(self):
        """
        Return the instructions for this Game.
        """
        instructions = "Players take turns claiming cells (in the " + \
                       "diagram: circles" + \
                       " labelled with a capital letter). When a player " + \
                       "captures at least half of the cells in a ley-line " + \
                       "(in the diagram: hexagons with a line " + \
                       "connecting it to cells)" + \
                       ",then the player captures that ley-line. " + \
                       "The first player to " + \
                       "capture at least half of the ley-lines " + \
                       "is the winner." + \
                       "A ley-line, once claimed, cannot be taken" + \
                       " by the other player."
        return instructions

    def is_over(self, state: 'StonehengeState') -> bool:
        """
        Return whether or not this game is over.
        """
        win_condition_total = (state.side_length + 1) * 3
        one_counter = 0
        two_counter = 0
        for key in state.board.leylines:
            if state.board.leylines[key][0] == '1':
                one_counter += 1
            elif state.board.leylines[key][0] == '2':
                two_counter += 1
        return one_counter >= win_condition_total / 2 or \
            two_counter >= win_condition_total / 2

    def is_winner(self, player):
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        :param player: The player to check.
        :type player: str
        :return: Whether player has won or not.
        :rtype: bool
        """
        win_condition_total = (self.current_state.side_length + 1) * 3
        one_counter = 0
        two_counter = 0
        for key in self.current_state.board.leylines:
            if self.current_state.board.leylines[key][0] == '1':
                one_counter += 1
            elif self.current_state.board.leylines[key][0] == '2':
                two_counter += 1
        if player == 'p1':
            return one_counter >= win_condition_total / 2
        return two_counter >= win_condition_total / 2

    def str_to_move(self, string):
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.

        :param string:
        :type string:
        :return:
        :rtype:
        """
        if not isinstance(string, str):
            return 'not a valid move!'
        return string


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
