"""Document for the stonehenge game."""

from game import Game
from stonehenge_gamestate import StonehengeGamestate
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class StonehengeGame(Game):
    """A class to keep track of the Stonhenge Game."""
    def __init__(self, p1_starts: bool,
                 current_state: 'StonehengeGamestate' = None) -> None:
        """Initializes the stonehenge game.
        >>> x1 = StonehengeGamestate(True, 2)
        >>> g1 = StonehengeGame(True, x1)
        >>> g1.current_state.size
        2"""
        self.p1_starts = p1_starts
        if not current_state:
            self.current_state = StonehengeGamestate(self.p1_starts)
        else:
            self.current_state = current_state

    def get_instructions(self) -> str:
        """Returns the instructions for the stonehenge game.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> g1 = StonehengeGame(True, x1)
        >>> in1 = g1.get_instructions()
        >>> isinstance(in1, str)
        True"""

        return "INSTRUCTIONS: This game is about capturing ley-lines," \
               "(represented by @) " \
               "in other words, lines of letters from the board. Players" \
               "take turns claiming spots (represented by letters) from the " \
               "board. The first player to capture at least 50% of the " \
               "letters in a line captures that ley-line permanently." \
               "Once a player has captured 50% of the ley-lines of the " \
               "board, they win the game."

    def is_over(self, state: 'StonehengeGamestate') -> bool:
        """Returns whether or not the game is over by checking whether or not
        either player has captured at least half of the ley-lines.
        >>> x1 = StonehengeGamestate(True, 1)
        >>> g1 = StonehengeGame(True, x1)
        >>> g1.is_over(x1)
        False
        >>> x1.ley_lines = [['1', ['1', 'B']], ['@', ['C']], ['1', ['1']], \
        ['@', ['B']], ['1', ['1', 'C']], ['@', ['B', 'C']]]
        >>> g1.is_over(x1)
        True
        """
        count1, count2 = 0, 0
        for i in range(len(state.ley_lines)):
            if state.ley_lines[i][0] == '1':
                count1 += 1
            elif state.ley_lines[i][0] == '2':
                count2 += 1
        return count1 >= len(state.ley_lines) / 2 or count2 >= \
            len(state.ley_lines) / 2

    def is_winner(self, player: str) -> bool:
        """Checks if the proposed player is the winner.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> g1 = StonehengeGame(True, x1)
        >>> x1.ley_lines = [['1', ['1', 'B']], ['@', ['C']], ['1', ['1']], \
        ['@', ['B']], ['1', ['1', 'C']], ['@', ['B', 'C']]]
        >>> g1.is_winner('p1')
        True
        >>> g1.is_winner('p2')
        False"""

        # Check which player has captured at least 50% of the leylines.
        count1, count2 = 0, 0
        for i in range(len(self.current_state.ley_lines)):
            if self.current_state.ley_lines[i][0] == '1':
                count1 += 1
            elif self.current_state.ley_lines[i][0] == '2':
                count2 += 1
        if count1 > count2:
            winner = 'p1'
        elif count1 < count2:
            winner = 'p2'
        else:
            winner = 'Tie!'
        return player == winner

    def str_to_move(self, string: str) -> str:
        """Returns the formatted move to make. In this case, just returns the
        move itself since the required move is just a string.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> g1 = StonehengeGame(True, x1)
        >>> g1.str_to_move("A")
        'A'
        """

        return string

    def __eq__(self, other: 'StonehengeGame') -> bool:
        """Returns whether two Stonehenge games are equal by comparing their
        current states. It does not consider whether player one started or not.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> g1 = StonehengeGame(True, x1)
        >>> x2 = x1.make_move("A")
        >>> g2 = StonehengeGame(True, x2)
        >>> g1 == g2
        False
        >>> x3 = StonehengeGamestate(False, 3)
        >>> g3 = StonehengeGame(False, x3)
        >>> g3 == g1
        True
        """
        return self.current_state == other.current_state


if __name__ == '__main__':
    from doctest import testmod
    testmod()
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
