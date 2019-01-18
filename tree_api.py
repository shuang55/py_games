""" A barebones Tree class, with only __init__, to
be used in iterative_minimax_strategy.
This code was taken from winter 2018 csc148
lecture notes.
"""


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    Again, most of this code is taken from winter 2018
    csc148 lecture notes.
    === Attributes ===
    @param object value: value of root node
    @param list[Tree|None] children: child nodes
    """
    def __init__(self, value=None, children=None):
        """
        Create Tree self with content value and 0 or more children
        @param Tree self: this tree
        @param object value: value contained in this tree
        @param list[Tree|None] children: possibly-empty list of children
        @rtype: None
        """
        # this code is taken from lecture notes
        self.value = value
        # copy children if not None
        # NEVER have a mutable default parameter...
        self.children = children[:] if children is not None else []
        self.score = None
        self.move = None


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
