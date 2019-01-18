""" Stack class, to
be used in iterative_minimax_strategy.
This code was taken from winter 2018 csc148
lecture notes.
"""


class Stack:
    """ Last-in, first-out (LIFO) stack.
    Again, all of this code is taken from
    csc148 winter 2018 lecture notes.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.

        >>> s = Stack()
        """
        # code is taken from lecture notes
        self._contains = []

    def add(self, obj: object) -> None:
        """ Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(5)
        """
        self._contains.append(obj)

    def remove(self) -> object:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not emp.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contains.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(5)
        >>> s.is_empty()
        False
        """
        return len(self._contains) == 0


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
