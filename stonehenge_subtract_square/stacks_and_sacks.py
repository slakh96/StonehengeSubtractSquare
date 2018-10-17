"""stack: init, add remove, isempty
Sack: init, add remove, isempty"""
from random import randint
from tree import Tree

# NOTE: THIS FILE IS TAKEN FROM THE LAB HANDOUT, FROM CLASS. As was posted by
# an instructor on Piazza, we are permitted to use these files when citing them.


class Container:
    """A class to represent the types of containers such as Stack and Sack."""

    def __init__(self) -> None:
        """Initializes an empty stack.
        >>> c1 = Container()
        >>> c1.contents
        []
        """
        self.contents = []

    # def __str__(self) -> str:
    #     """REturns str rep."""
    #     to_return = []
    #     return self.contents

    def add(self, to_add: object) -> None:
        """Adds an item to the top of the stack. In a stack, cannot add
        things to the middle or the bottom.
        >>> c1 = Container()
        >>> c1.add(3)
        >>> c1.contents
        [3]
        """
        self.contents.append(to_add)

    def remove(self) -> object:
        """Removes and returns an object."""

        raise NotImplementedError("You must define this specifically for your"
                                  "container subclass!")

    def is_empty(self) -> bool:
        """Checks whether or not this Stack is empty.
        >>> c1 = Container()
        >>> c1.is_empty()
        True
        >>> c1.add(3)
        >>> c1.add(4)
        >>> c1.is_empty()
        False
        """
        return self.contents == []


class Stack(Container):
    """A class to represnt the object stack in List format, where the items
    are added and removed from the top. Init, is_empty, and add are inherited
    from the superclass Container."""

    def remove(self) -> Tree:
        """Removes the top item of the stack and returns it.
        >>> s1 = Stack()
        >>> s1.add(3)
        >>> s1.add(4)
        >>> s1.remove()
        4
        """
        if not Stack.is_empty(self):
            return self.contents.pop()
        else:
            raise AttributeError("Empty Stack, cannot remove!")


class Sack(Container):
    """A class to represent a sack."""

    def remove(self) -> object:
        """Removes a random object from the sack and returns this object.
        >>> s1 = Sack()
        >>> s1.add(3)
        >>> s1.is_empty()
        False
        >>> s1.remove()
        3
        >>> s1.is_empty()
        True"""

        if not Sack.is_empty(self):
            rand = randint(0, len(self.contents) - 1)
            return self.contents.pop(rand)
        else:
            raise Exception("You cannot remove from an empty Sack!")


if __name__ == '__main__':
    from doctest import testmod
    testmod()
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
