"""
Implementation of stonehengestate and stonehengegame.
"""
import copy
from typing import Any
from game_state import GameState
from board import Board


# todo: state before game
# todo: docstring examples!

class StonehengeState(GameState):
    """
    The state of a game at a certain point in time.
    """
    LENGTH_ONE = ["      @   @",
                  '     /   /',
                  '@ - A - B',
                  '     \\ / \\',
                  '  @ - C   @',
                  '       \\',
                  '        @']
    LENGTH_TWO = ['        @   @',
                  '       /   /',
                  '  @ - A - B   @',
                  '     / \\ / \\ /',
                  '@ - C - D - E',
                  '     \\ / \\ / \\',
                  '  @ - F - G   @',
                  '       \\   \\',
                  '        @   @']
    LENGTH_THREE = ['          @   @',
                    '         /   /',
                    '    @ - A - B   @',
                    '       / \\ / \\ /',
                    '  @ - C - D - E   @',
                    '     / \\ / \\ / \\ /',
                    '@ - F - G - H - I',
                    '     \\ / \\ / \\ / \\',
                    '  @ - J - K - L   @',
                    '       \\   \\   \\',
                    '        @   @   @']
    LENGTH_FOUR = ['            @   @',
                   '           /   /',
                   '      @ - A - B   @',
                   '         / \\ / \\ /',
                   '    @ - C - D - E   @',
                   '       / \\ / \\ / \\ /',
                   '  @ - F - G - H - I   @',
                   '     / \\ / \\ / \\ / \\ /',
                   '@ - J - K - L - M - N ',
                   '     \\ / \\ / \\ / \\ / \\',
                   '  @ - O - P - Q - R   @',
                   '       \\   \\   \\   \\',
                   '        @   @   @   @']
    LENGTH_FIVE = ['              @   @',
                   '             /   /',
                   '        @ - A - B   @',
                   '           / \\ / \\ /',
                   '      @ - C - D - E   @',
                   '         / \\ / \\ / \\ /',
                   '    @ - F - G - H - I   @',
                   '       / \\ / \\ / \\ / \\ /',
                   '  @ - J - K - L - M - N   @ ',
                   '     / \\ / \\ / \\ / \\ / \\ /',
                   '@ - O - P - Q - R - S - T',
                   '     \\ / \\ / \\ / \\ / \\ / \\',
                   '  @ - U - V - W - X - Y   @',
                   '       \\   \\   \\   \\   \\',
                   '        @   @   @   @   @']

    def __init__(self, is_p1_turn: bool, side_length: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        >>> s = StonehengeState(True, 1)
        >>> s.side_length
        1
        """
        super().__init__(is_p1_turn)
        self.side_length = side_length
        self.board = Board(side_length)

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        return self.board.__str__()

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to
        StonehengeState self.
        >>> s = StonehengeState(True, 1)
        >>> s.get_possible_moves()
        ['A', 'B', 'C']
        """
        win_condition_total = (self.side_length + 1) * 3
        one_counter = 0
        two_counter = 0
        game_is_over = False
        for key in self.board.leylines:
            if self.board.leylines[key][0] == '1':
                one_counter += 1
            elif self.board.leylines[key][0] == '2':
                two_counter += 1
        if one_counter >= win_condition_total / 2 or \
                two_counter > win_condition_total / 2:
            game_is_over = True
        if game_is_over:
            return []
        new_list = []
        possible_cells = 'ABCDEFGHIJKLMNOPQRSTUVWXY'
        for row in self.board.board:
            for char in row:
                if char in possible_cells:
                    new_list.append(char)
        return new_list

    def make_move(self, move: Any) -> "StonehengeState":
        """
        Return the StonehengeState that results from applying move to
        this StonehengeState.
        >>> s = StonehengeState(True, 2)
        >>> b = s.make_move('A')
        >>> s == b
        False
        """
        if type(move) != str:
            raise TypeError('Input should be type str!')
        new_state = copy.deepcopy(self)
        for row in new_state.board.board:
            for char in row:
                if move == char:
                    move_row = new_state.board.board.index(row)
        move_index = new_state.board.board[move_row].find(move)
        current_player = 1 if self.p1_turn else 2
        new_state.board.board[move_row] = new_state.board.\
            board[move_row][:move_index] + str(current_player) +\
            new_state.board.board[move_row][move_index+1:]
        for leyline in new_state.board.leylines:
            if move in new_state.board.leylines[leyline]:
                index = new_state.board.leylines[leyline].find(move)
                new_state.board.leylines[leyline] = new_state.board.\
                    leylines[leyline][:index] + str(current_player) \
                    + new_state.board.leylines[leyline][index+1:]
        changes = []
        for leyline in new_state.board.leylines:
            if '@' in new_state.board.leylines[leyline]:
                leyline_length = len(new_state.board.leylines[leyline]) - 1
                count = new_state.board.leylines[leyline].\
                    count(str(current_player))
                if count >= leyline_length / 2:
                    new_state.board.leylines[leyline] = str(current_player) + \
                        new_state.board.leylines[leyline][1:]
                    # append to list changes a list of list of form
                    # [['leyline changed', 'num']]
                    changes.append([leyline[:len(leyline)-1], int(leyline[-1])])
        make_move_helper(changes, new_state, current_player)
        new_state.p1_turn = not new_state.p1_turn
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        >>> s = StonehengeState(True, 1)
        >>> b = s.make_move('A')
        >>> s.__repr__() == b.__repr__()
        False
        """
        # todo: check if this newline is okay
        return "P1's Turn: {} - Board: /n{}".format(self.p1_turn,
                                                    self.board)

    def rough_outcome(self):
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        >>> s = StonehengeState(True, 5)
        >>> s.rough_outcome()
        0
        >>> b = StonehengeState(True, 1)
        >>> b.rough_outcome()
        1
        """
        current_state = copy.deepcopy(self)
        possible_moves = current_state.get_possible_moves()
        results_list = []
        # 1 state ahead
        for move in possible_moves:
            new_state = current_state.make_move(str(move))
            if new_state.get_possible_moves() == []:
                results_list.append(self.WIN)
            else:
                new_state_poss_moves = new_state.get_possible_moves()
                rough_outcome_helper(new_state, results_list,
                                     new_state_poss_moves)
        results_list_copy = results_list[:]
        if self.WIN in results_list_copy:
            return self.WIN
        elif any([x != self.LOSE for x in results_list_copy]):
            return self.DRAW
        return self.LOSE

# ==================HELPER FUNCTION=========================================


def make_move_helper(changes: list, new_state: 'StonehengeState',
                     current_player: int)->None:
    """
    A helper function for make_move, this function
    modifies the board to replace the
    appropriate leyline markers with the correct number.
    >>> s = StonehengeState(True, 1)
    >>> b = copy.deepcopy(s)
    >>> changes = [[0,0]]
    >>> make_move_helper(changes, s, 1)
    >>> s == b
    False
    """
    for item in changes:
        if item[0] == 'dld':
            cell_to_change = new_state.board.dld_indices[item[-1] - 1]
            # cell_to_change is now a list of [row, index] of
            # the cell that we need to change
            row_to_change = cell_to_change[0]
            index_to_change = int(cell_to_change[-1])
            new_state.board.board[row_to_change] = new_state.board.\
                board[row_to_change][:index_to_change]\
                + str(current_player) + new_state.board.\
                board[row_to_change][index_to_change + 1:]
        elif item[0] == 'drd':
            cell_to_change = new_state.board.drd_indices[item[-1] - 1]
            row_to_change = cell_to_change[0]
            index_to_change = int(cell_to_change[-1])
            new_state.board.board[row_to_change] = new_state.board.\
                board[row_to_change][:index_to_change] + \
                str(current_player) + \
                new_state.board.board[row_to_change][index_to_change + 1:]
        elif item[0] == 'hor':
            row_to_change = item[-1] * 2
            index_to_change = new_state.board.\
                board[row_to_change].find('@')
            new_state.board.board[row_to_change] = new_state.board.\
                board[row_to_change][:index_to_change] + \
                str(current_player) + new_state.board.\
                board[row_to_change][index_to_change + 1:]


def rough_outcome_helper(new_state: 'StonehengeState',
                         results_list: list,
                         new_state_poss_moves: list)->None:
    """
    A helper function used in rough_outcome.
    This function takes in new_state, and a new_state_poss_moves, and
    for each move in new_state_poss_moves, if the move results in the
    game to be over, append -1 to results_list, otherwise, append 0 to
    results_list.
    >>> s = StonehengeState(True, 1)
    >>> results_list = []
    >>> new_state_poss_moves = s.get_possible_moves()
    >>> rough_outcome_helper(s, results_list, new_state_poss_moves)
    >>> max(results_list)
    -1
    """
    for new_state_move in new_state_poss_moves:
        newer_state = new_state.make_move(str(new_state_move))
        if newer_state.get_possible_moves() == []:
            results_list.append(-1)
        else:
            results_list.append(0)

# ===================end helper function====================


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
