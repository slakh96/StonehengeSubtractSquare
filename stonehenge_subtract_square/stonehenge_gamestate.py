"""Document for the gamestate of the stonehenge game."""

from typing import List
from game_state import GameState

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


class StonehengeGamestate(GameState):
    """A class to keep track of the Stonehenge gamestate."""

    def __init__(self, p1_turn: bool, size: int = None,
                 letter_values: List = None, ley_lines: List = None) -> None:
        """Initializes the game's state. Overwrites the initializer from the
        superclass.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> x1.letter_values
        [['A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'H', 'I'], ['J', 'K', 'L']]
        >>> x1.num_ley_lines
        12
        >>> x1.size
        3"""
        self.p1_turn = p1_turn
        if not size:
            self.size = int(input("Enter a board size from 1 - 5: "))
        else:
            self.size = size
        if not letter_values:  # **if we are starting a new game**
            self.letter_values = self.generate_game_spaces()
            self.ley_lines = self.generate_ley_lines()
        else:
            self.letter_values = letter_values
            self.ley_lines = ley_lines
        self.num_ley_lines = 3 * self.size + 3
        assert len(self.ley_lines) == self.num_ley_lines, "Error! Length of" \
                                                          "self.ley_lines !=" \
                                                          "self. num_ley_lines!"

    def generate_game_spaces(self) -> List[list]:
        """Generates the game board based on the size.
        >>> x1 = StonehengeGamestate(True, 2)
        >>> x1.generate_game_spaces()
        [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
        """

        index, counter, row_count, board_list = 0, 0, 2, []
        while row_count <= self.size + 1:
            row_temp_list = []
            while counter < row_count:
                counter += 1
                row_temp_list.append(ALPHABET[index])
                index += 1
            board_list.append(row_temp_list)
            row_count += 1
            counter = 0
        row_temp_list = []
        while counter < row_count - 2:
            counter += 1
            row_temp_list.append(ALPHABET[index])
            index += 1
        board_list.append(row_temp_list)
        # print(board_list)
        return board_list

    def generate_ley_lines(self) -> List[List]:
        """Generates ley_lines based on the game board size initialized.
        >>> x1 = StonehengeGamestate(True, 2)
        >>> y1 = x1.generate_ley_lines()
        >>> ['@', ['A', 'B']] in y1
        True
        >>> x2 = StonehengeGamestate(True, 3)
        >>> y2 = x2.generate_ley_lines()
        >>> ['@', ['E', 'H', 'K']] in y2
        True
        """
        ley_lines_list = []
        # Step 1: Generate the horizontal ley-lines
        horizontal_lines = self.generate_horizontal_ley_lines()
        for lst in horizontal_lines:
            ley_lines_list.append(lst)
        # Step 2: Special case of first row diagonal lists - 2 of them
        special_lines = self.generate_special_ley_lines()
        for lst in special_lines:
            ley_lines_list.append(lst)
        # Step 3: Generate the remaining diagonal ley lines.
        standard_lines = self.generate_standard_diagonal()
        for lst in standard_lines:
            ley_lines_list.append(lst)

        return ley_lines_list

    def generate_standard_diagonal(self) -> List[list]:
        """Generates the diagonal ley lines, other than the ones stemming from
        a and b which go along the borders of the game board.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> y = x1.generate_standard_diagonal()
        >>> ['@', ['A', 'D', 'H', 'L']] in y
        True
        >>> ['@', ['B', 'D', 'G', 'J']] in y
        True
        >>> x2 = StonehengeGamestate(True, 2)
        >>> y = x2.generate_standard_diagonal()
        >>> ['@', ['E', 'G']] in y
        True
        """
        # 1 variables: For the right standard diagonals.
        # 2 variables: For the left standard diagonals.
        ley_lines_list = []
        i = 0
        for sublist in self.letter_values[:-1]:
            temp_list1, temp_list2 = [], []
            temp_index1 = 0 - len(sublist)  # takes the first value.
            temp_index2 = len(sublist) - 1  # takes the end index from sublist
            for sublist2 in self.letter_values[i:]:  # starts from the
                # current sublist and goes until the end.
                if sublist2 == self.letter_values[-1]:
                    temp_list1.append(sublist2[temp_index1 + 1])
                    temp_list2.append(sublist2[temp_index2 - 1])
                else:
                    temp_list1.append(sublist2[temp_index1])
                    temp_list2.append(sublist2[temp_index2])
            ley_lines_list.append(["@", temp_list1])
            ley_lines_list.append(["@", temp_list2])
            i += 1

        return ley_lines_list

    def generate_horizontal_ley_lines(self) -> List[list]:
        """Helper function for the generate ley lines - this function
        generates the horizontal ley lines for us.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> y = x1.generate_horizontal_ley_lines()
        >>> ['@', ['A', 'B']] in y
        True
        >>> x2 = StonehengeGamestate(True, 2)
        >>> x2.generate_horizontal_ley_lines()
        [['@', ['A', 'B']], ['@', ['C', 'D', 'E']], ['@', ['F', 'G']]]"""
        ley_lines_list = []
        for sublist in self.letter_values:
            new_ley_line = ['@', sublist]
            ley_lines_list.append(new_ley_line)
        return ley_lines_list

    def generate_special_ley_lines(self) -> List[list]:
        """Generates the special ley-lines: i.e. the ones which stem from the
        top 2 elements and consist of the elements at the right and left borders
        of the board, except for the bottom-most element.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> x1.generate_special_ley_lines()
        [['@', ['A', 'C', 'F']], ['@', ['B', 'E', 'I']]]
        >>> x2 = StonehengeGamestate(True, 2)
        >>> x2.generate_special_ley_lines()
        [['@', ['A', 'C']], ['@', ['B', 'E']]]
        """
        temp_list, temp_list2, ley_lines_list = [], [], []
        for sublist in self.letter_values:
            temp_list.append(sublist[0])
            # print(temp_list)
            temp_list2.append(sublist[-1])
            # print(temp_list2)
        temp_list = temp_list[:-1]
        temp_list2 = temp_list2[:-1]
        new_ley_line = ["@", temp_list]
        ley_lines_list.append(new_ley_line)
        new_ley_line = ["@", temp_list2]
        ley_lines_list.append(new_ley_line)
        return ley_lines_list

    def __str__(self) -> str:
        """Return the string representation of this game state.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> y1 = x1.__str__()
        >>> isinstance(y1, str)
        True"""
        if self.size == 1:
            return r"""\\
                   {}   {}
                  /   /
             {} - {} - {}
                  \ / \
               {} - {}   {}
                    \
                     {}""".format(self.ley_lines[2][0], self.ley_lines[5][0],
                                  self.ley_lines[0][0], self.ley_lines[0][1][0],
                                  self.ley_lines[0][1][1], self.ley_lines[1][0],
                                  self.ley_lines[1][1][0], self.ley_lines[3][0],
                                  self.ley_lines[4][0])
        elif self.size == 2:
            return r"""\\
                        {}   {}
                       /   /
                  {} - {} - {}   {}
                     / \ / \ /
                {} - {} - {} - {}
                     \ / \ / \
                  {} - {} - {}   {}
                       \   \
                        {}   {}""".format(self.ley_lines[3][0],
                                          self.ley_lines[6][0],
                                          self.ley_lines[0][0],
                                          self.ley_lines[0][1][0],
                                          self.ley_lines[0][1][1],
                                          self.ley_lines[8][0],
                                          self.ley_lines[1][0],
                                          self.ley_lines[1][1][0],
                                          self.ley_lines[1][1][1],
                                          self.ley_lines[1][1][2],
                                          self.ley_lines[2][0],
                                          self.ley_lines[2][1][0],
                                          self.ley_lines[2][1][1],
                                          self.ley_lines[4][0],
                                          self.ley_lines[7][0],
                                          self.ley_lines[5][0])
        elif self.size == 3:
            return r"""\\
                           {}  {}
                          /  /
                     {} - {} - {}   {}
                        / \ / \ /
                   {} - {} - {} - {}   {}
                      / \ / \ / \ /
                 {} - {} - {} - {} - {}
                      \ / \ / \ / \
                   {} - {} - {} - {}   {}
                        \   \   \
                         {}   {}   {}
                """.format(self.ley_lines[4][0], self.ley_lines[7][0],
                           self.ley_lines[0][0], self.ley_lines[0][1][0],
                           self.ley_lines[0][1][1], self.ley_lines[9][0],
                           self.ley_lines[1][0], self.ley_lines[1][1][0],
                           self.ley_lines[1][1][1], self.ley_lines[1][1][2],
                           self.ley_lines[11][0], self.ley_lines[2][0],
                           self.ley_lines[2][1][0], self.ley_lines[2][1][1],
                           self.ley_lines[2][1][2], self.ley_lines[2][1][3],
                           self.ley_lines[3][0], self.ley_lines[3][1][0],
                           self.ley_lines[3][1][1], self.ley_lines[3][1][2],
                           self.ley_lines[5][0], self.ley_lines[10][0],
                           self.ley_lines[8][0], self.ley_lines[6][0])
        elif self.size == 4:

            return r"""\\
                       {}  {}
                      /  /
                 {} - {} - {}   {}
                    / \ / \ /
               {} - {} - {} - {}   {}
                  / \ / \ / \ /
             {} - {} - {} - {} - {}   {}
                / \ / \ / \ / \ /
           {} - {} - {} - {} - {} - {}
                \ / \ / \ / \ / \
             {} - {} - {} - {} - {}   {}
                  \   \   \   \
                   {}   {}   {}   {}
        """.format(self.ley_lines[5][0], self.ley_lines[8][0],
                   self.ley_lines[0][0], self.ley_lines[0][1][0],
                   self.ley_lines[0][1][1], self.ley_lines[10][0],
                   self.ley_lines[1][0], self.ley_lines[1][1][0],
                   self.ley_lines[1][1][1], self.ley_lines[1][1][2],
                   self.ley_lines[12][0], self.ley_lines[2][0],
                   self.ley_lines[2][1][0], self.ley_lines[2][1][1],
                   self.ley_lines[2][1][2], self.ley_lines[2][1][3],
                   self.ley_lines[14][0], self.ley_lines[3][0],
                   self.ley_lines[3][1][0], self.ley_lines[3][1][1],
                   self.ley_lines[3][1][2], self.ley_lines[3][1][3],
                   self.ley_lines[3][1][4], self.ley_lines[4][0],
                   self.ley_lines[4][1][0],
                   self.ley_lines[4][1][1], self.ley_lines[4][1][2],
                   self.ley_lines[4][1][3], self.ley_lines[6][0],
                   self.ley_lines[13][0], self.ley_lines[11][0],
                   self.ley_lines[9][0], self.ley_lines[7][0])
        elif self.size == 5:
            return r"""\\
                       {}  {}
                      /  /
                 {} - {} - {}   {}
                    / \ / \ /
               {} - {} - {} - {}   {}
                  / \ / \ / \ /
             {} - {} - {} - {} - {}   {}
                / \ / \ / \ / \ /
           {} - {} - {} - {} - {} - {}   {}
              / \ / \ / \ / \ / \ /
         {} - {} - {} - {} - {} - {} - {}
              \ / \ / \ / \ / \ / \
           {} - {} - {} - {} - {} - {}   {}
                \   \   \   \   \
                 {}   {}   {}   {}   {}
         """.format(self.ley_lines[6][0], self.ley_lines[9][0],
                    self.ley_lines[0][0], self.ley_lines[0][1][0],
                    self.ley_lines[0][1][1], self.ley_lines[11][0],
                    self.ley_lines[1][0], self.ley_lines[1][1][0],
                    self.ley_lines[1][1][1], self.ley_lines[1][1][2],
                    self.ley_lines[13][0], self.ley_lines[2][0],
                    self.ley_lines[2][1][0], self.ley_lines[2][1][1],
                    self.ley_lines[2][1][2], self.ley_lines[2][1][3],
                    self.ley_lines[15][0], self.ley_lines[3][0],
                    self.ley_lines[3][1][0], self.ley_lines[3][1][1],
                    self.ley_lines[3][1][2], self.ley_lines[3][1][3],
                    self.ley_lines[3][1][4], self.ley_lines[17][0],
                    self.ley_lines[4][0], self.ley_lines[4][1][0],
                    self.ley_lines[4][1][1], self.ley_lines[4][1][2],
                    self.ley_lines[4][1][3], self.ley_lines[4][1][4],
                    self.ley_lines[4][1][5], self.ley_lines[5][0],
                    self.ley_lines[5][1][0], self.ley_lines[5][1][1],
                    self.ley_lines[5][1][2], self.ley_lines[5][1][3],
                    self.ley_lines[5][1][4], self.ley_lines[7][0],
                    self.ley_lines[16][0], self.ley_lines[14][0],
                    self.ley_lines[12][0], self.ley_lines[10][0],
                    self.ley_lines[8][0])
        return "BOARD SIZE NOT FROM 1-5: CANNOT OUTPUT STR REPRESENTATION."

    def __repr__(self) -> str:
        """Returns a string representation of this game state. Shows each
        individual ley line instead of the visual game board. Also provides
        additional information such as the size and whose turn it is.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> y1 = x1.__str__()
        >>> isinstance(y1, str)
        True"""

        ley_output = "\n"
        for ley_line in self.ley_lines:
            ley_output += str(ley_line)
            ley_output += '\n'
        return " __repr__ ! Size: {}. {}'s turn. {} Ley lines: {}" \
            .format(self.size, self.get_current_player_name(),
                    self.num_ley_lines, ley_output)

    def get_possible_moves(self) -> List[str]:
        """Returns a list of all the possible moves available. Possible moves
        include any space that is not yet taken by a player.
        >>> x3 = StonehengeGamestate(True, 3)
        >>> x3.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        >>> x2 = StonehengeGamestate(True, 2)
        >>> x2.ley_lines = [['@', [1, 'B']], ['@', ['C', 'D', 'E']], \
        ['@', ['F', 'G']], ['@', [1, 'C']], ['@', ['B', 'E']], \
        ['@', [1, 'D', 'G']], ['@', ['B', 'D', 'F']], ['@', ['C', 'F']], \
        ['@', ['E', 'G']]]
        >>> x2.get_possible_moves()
        ['B', 'C', 'D', 'E', 'F', 'G']
        """

        possible_moves = []
        # Check if game is over first.
        count1, count2 = 0, 0
        for i in range(len(self.ley_lines)):
            if self.ley_lines[i][0] == '1':
                count1 += 1
            elif self.ley_lines[i][0] == '2':
                count2 += 1
        if (count1 >= len(self.ley_lines) / 2 or count2 >=
                len(self.ley_lines) / 2):
            return []
        # If the game is not over already
        for ley_line in self.ley_lines:
            for item in ley_line[1]:
                if item in ALPHABET and item not in possible_moves:
                    possible_moves.append(item)
        return possible_moves

    def make_move(self, move: str) -> 'StonehengeGamestate':
        """Makes a move and builds a new gamestate based on what the move would
        do to the old gamestate.
        >>> x1 = StonehengeGamestate(True, 1)
        >>> xnew = x1.make_move("A")
        >>> xnew.p1_turn
        False
        >>> "A" in xnew.letter_values[0]
        False
        >>> xnew.size
        1
        >>> len(xnew.ley_lines)
        6
        >>> "A" in x1.letter_values[0]
        True
        """
        # Must first change the ley-lines and then change the letter_values.
        temp_ley_lines, to_append = [], []
        for ley_line in self.ley_lines:  # e.g ["@", [A, B]]
            to_append.append(ley_line[0])
            to_append.append(ley_line[1][:])
            temp_ley_lines.append(to_append)
            to_append = []
        temp_letter_values = []
        for letter_row in self.letter_values:  # e.g. ['A', 'B']
            to_append = []
            for i in range(len(letter_row)):
                to_append.append(letter_row[i])
            temp_letter_values.append(to_append)

        if self.p1_turn:
            change_to = "1"
        else:
            change_to = "2"

        # Step 1: Change the ley-lines.
        temp_ley_lines = change_ley_lines(temp_ley_lines, move, change_to)

        # Step 2: Change the letter_values.
        for i in range(len(temp_letter_values)):
            for x in range(len(temp_letter_values[i])):
                if temp_letter_values[i][x] == move:
                    temp_letter_values[i][x] = change_to
        # Step 3: Change who is playing.
        if change_to == '1':  # if player 1 was just playing
            temp_is_p1_turn = False
        else:
            temp_is_p1_turn = True

        # Step 4: Form and return the new game state.
        new_game_state = StonehengeGamestate(temp_is_p1_turn, self.size,
                                             temp_letter_values, temp_ley_lines)
        return new_game_state

    def rough_outcome(self) -> float:
        """Return a estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self. Thus, return whether the player
        can immediatley win with this move, will lose(other player can
        immediately win if the current player does this move), or neither will
        happen within this move from current player & then move from opposite
        player.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> x1.rough_outcome()
        0"""

        possible_moves = self.get_possible_moves()
        temp_state = self
        if possible_moves == []:  # If no possible moves, the player cannot not
            # lose.
            return -1
        else:
            states_after_move_list = []
            for move in temp_state.get_possible_moves():
                new_state = temp_state.make_move(move)
                states_after_move_list.append(new_state)
            if any(gstate.get_possible_moves() == [] for gstate in
                   states_after_move_list):  # If current player can make a move
                # that leaves the other player with no moves to do...then
                # the current player wins.
                return 1
            else:
                if all_states_over(states_after_move_list):
                    return -1
                return 0
        # if the player cannot win or lose within 1 turn.

    def __eq__(self, other: "StonehengeGamestate") -> bool:
        """Return whether this state and another Stonehenge game state are
        equal. States are said to be equal if they have the same size and
        the same ley-lines. It does not matter whether
        or not it is p1's turn or p2's turn.
        >>> x1 = StonehengeGamestate(True, 3)
        >>> x2 = StonehengeGamestate(True, 3)
        >>> x1 == x2
        True
        >>> x3 = x1.make_move("A")
        >>> x2 == x3
        False"""
        return self.ley_lines == other.ley_lines and self.size == other.size


def all_states_over(states_list: List[GameState]) -> bool:
    """Given a list of states, checks if all the states can be over within one
     move."""
    # list_states_if_over = []
    for state in states_list:
        for move in state.get_possible_moves():
            if state.make_move(move).get_possible_moves() != []:
                return False
    return True


def change_ley_lines(ley_lines: List, move: str,
                     change_to: str) -> List:
    """Changes the ley line by substituting the values in the move with the
    player number. Helper function for make_move.
    >>> x1 = StonehengeGamestate(True, 1)
    >>> y1 = change_ley_lines(x1.ley_lines, "A", "1")
    >>> y1 == [['1', ['1', 'B']], ['@', ['C']], ['1', ['1']], ['@', ['B']], \
    ['1', ['1', 'C']], ['@', ['B', 'C']]]
    True
    """
    temp_ley_lines = []
    for ley_line in ley_lines:
        temp_ley_lines.append(ley_line[:])
    # Step 1: Mark the spots with the player's number.
    for i in range(len(temp_ley_lines)):
        for x in range(len(temp_ley_lines[i][1])):
            if temp_ley_lines[i][1][x] == move:
                temp_ley_lines[i][1][x] = change_to

    # Step 2: Attribute the ley-lines to the player if applicable.
    for i in range(len(temp_ley_lines)):
        if temp_ley_lines[i][0] == "@":
            temp_ley_lines[i] = \
                attribute_ley_line(temp_ley_lines[i], change_to)

    return temp_ley_lines


def attribute_ley_line(ley_line: List, change_to: str) -> List:
    """Attributes the ley line to a player if applicable. Helper function
    for chenge_ley_lines.
    >>> x1 = StonehengeGamestate(True, 1)
    >>> attribute_ley_line(['@', ['1', 'B']], "1")
    ['1', ['1', 'B']]
    >>> x2 = StonehengeGamestate(True, 3)
    >>> attribute_ley_line(['1', ['1', '2']], "2")
    ['1', ['1', '2']]"""
    count_taken1, count_taken2 = 0, 0
    for i in range(len(ley_line[1])):
        if ley_line[1][i] == "1":
            count_taken1 += 1
        elif ley_line[1][i] == "2":
            count_taken2 += 1
    if (count_taken1 >= len(ley_line[1]) / 2 or count_taken2 >=
            len(ley_line[1]) / 2) and ley_line[0] == "@":
        ley_line[0] = change_to
    return ley_line


if __name__ == '__main__':
    from doctest import testmod
    testmod()
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
    # x1 = StonehengeGamestate(True, 1)
    # y1 = x1.make_move("A")
    # x2 = StonehengeGamestate(True, 2)
    # x3 = StonehengeGamestate(True, 3)
    # x4 = StonehengeGamestate(False, 4)
    # x5 = StonehengeGamestate(False, 5)
