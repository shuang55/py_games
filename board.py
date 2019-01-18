""" A board class used in playing Stonehenge"""

class Board:
    """
    A board class
    """
    LENGTH_ONE = ("      @   @",
                  '     /   /',
                  '@ - A - B',
                  '     \\ / \\',
                  '  @ - C   @',
                  '       \\',
                  '        @')
    LENGTH_TWO = ('        @   @',
                  '       /   /',
                  '  @ - A - B   @',
                  '     / \\ / \\ /',
                  '@ - C - D - E',
                  '     \\ / \\ / \\',
                  '  @ - F - G   @',
                  '       \\   \\',
                  '        @   @')
    LENGTH_THREE = ('          @   @',
                    '         /   /',
                    '    @ - A - B   @',
                    '       / \\ / \\ /',
                    '  @ - C - D - E   @',
                    '     / \\ / \\ / \\ /',
                    '@ - F - G - H - I',
                    '     \\ / \\ / \\ / \\',
                    '  @ - J - K - L   @',
                    '       \\   \\   \\',
                    '        @   @   @')
    LENGTH_FOUR = ('            @   @',
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
                   '        @   @   @   @',)
    LENGTH_FIVE = ('              @   @',
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
                   '        @   @   @   @   @')

    LEYLINES_LENGTH_ONE = (('dld1', '@A'), ('dld2', '@BC'),
                           ('drd1', '@AC'), ('drd2', '@B'))

    def __init__(self, side_length: int)-> None:
        """
        Initialize a stonehenge board
        """
        self.side_length = side_length
        if side_length == 1:
            self.board = list(self.LENGTH_ONE)
        elif side_length == 2:
            self.board = list(self.LENGTH_TWO)
        elif side_length == 3:
            self.board = list(self.LENGTH_THREE)
        elif side_length == 4:
            self.board = list(self.LENGTH_FOUR)
        elif side_length == 5:
            self.board = list(self.LENGTH_FIVE)
        self.dld_indices = [][:]
        self.dld_indices.append([0, self.board[0].find('@')])
        self.dld_indices.append([0, self.board[0].rfind('@')])
        # construct the indices of the (down left) diagonal leylines markers
        # now, dld_indices is a list of list of the form
        # [row, the indices of the leyline markers]
        # of form [index_dld1, index_dld2 , ... , index_dld6]
        if self.side_length >= 2:
            self.dld_indices.append([2, self.board[2].rfind('@')])
        if self.side_length >= 3:
            self.dld_indices.append([4, self.board[4].rfind('@')])
        if self.side_length >= 4:
            self.dld_indices.append([6, self.board[6].rfind('@')])
        if self.side_length >= 5:
            self.dld_indices.append([8, self.board[8].rfind('@')])
        # construct the indices of the (down right) diagonal leylines markers
        self.drd_indices = [][:]
        number_leylines = self.side_length + 1
        starting_index = 0
        for i in range(number_leylines):
            if i == self.side_length:
                self.drd_indices.append([-3, self.board[-3].rfind('@')])
            else:
                self.drd_indices.append([-1, self.board[-1].
                                         find('@', starting_index)])
                starting_index = self.board[-1].find('@', starting_index) + 1
        ####
        n = self.side_length
        if n == 1:
            leylines_dict = dict(self.LEYLINES_LENGTH_ONE)
        elif n == 2:
            leylines_dict = {'dld1': '@AC', 'dld2': '@BDF', 'dld3': '@EG',
                             'drd1': '@CF', 'drd2': '@ADG',
                             'drd3': '@BE'}.copy()
        elif n == 3:
            leylines_dict = {'dld1': '@ACF', 'dld2': '@BDGJ', 'dld3': '@EHK',
                             'dld4': '@IL', 'drd1': '@FJ', 'drd2': '@CGK',
                             'drd3': '@ADHL', 'drd4': '@BEI'}.copy()
        elif n == 4:
            leylines_dict = {'dld1': '@ACFJ', 'dld2': '@BDGKO', 'dld3': '@EHLP',
                             'dld4': '@IMQ', 'dld5': '@NR',
                             'drd1': '@JO', 'drd2': '@FKP',
                             'drd3': '@CGLQ', 'drd4': '@ADHMR',
                             'drd5': '@BEIN'}.copy()
        elif n == 5:
            leylines_dict = {'dld1': '@ACFJO', 'dld2': '@BDGKPU',
                             'dld3': '@EHLQV',
                             'dld4': '@IMRW', 'dld5': '@NSX', 'dld6': '@TY',
                             'drd1': '@OU', 'drd2': '@JPV', 'drd3': '@FKQW',
                             'drd4': '@CGLRX', 'drd5': '@ADHMSY',
                             'drd6': '@BEINT'}.copy()
        i = 2
        while i < len(self.board) - 2:
            name = 'hor' + str(int(i / 2))
            row_chars = ''
            for char in self.board[i]:
                if char not in ' -\\/':
                    row_chars += char
            leylines_dict[name] = row_chars.rstrip('@')
            i += 2
        self.leylines = leylines_dict
        ####

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        return "\n".join([x for x in self.board])

    def construct_leylines(self)-> dict:
        # todo: should i keep this
        """Construct the leylines for Board self"""
        pass

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
