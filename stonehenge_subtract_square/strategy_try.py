"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, Union, List
from game import Game
from game_state import GameState
from tree import Tree
from stacks_and_sacks import Stack


ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def recursive_minimax(game: Game) -> Union[List, int]:
    """
    Returns a move for the game input through using recursion to look at
    all possible moves and determining the best one for the user to choose.
    >>> from stonehenge_game import StonehengeGame
    >>> from stonehenge_gamestate import StonehengeGamestate
    >>> x1 = StonehengeGamestate(True, 2)
    >>> g1 = StonehengeGame(True, x1)
    >>> recursive_minimax(g1)
    'A'
    >>> x1 = StonehengeGamestate(True, 2)
    >>> x1 = x1.make_move('A')
    >>> x1 = x1.make_move('F')
    >>> x1 = x1.make_move('D')
    >>> g1 = StonehengeGame(True, x1)
    >>> recursive_minimax(g1)
    'E'
    """
    lst_w_max = []
    original_moves = game.current_state.get_possible_moves()
    print("Original moves: ")
    print(original_moves)
    player_name = game.current_state.get_current_player_name()
    lst = recursive_minimax_helper(game.current_state, player_name)
    for element in lst:
        print(element)
    # print(len(lst))
    for i in range(len(lst)):
        lst_w_max.append(find_max_state(lst[i]))
    assert len(lst_w_max) == len(original_moves), "More numbers than moves!"
    print(lst_w_max)
    move_to_make_value = max(lst_w_max)
    # print(move_to_make_value)
    i = 0
    while i < len(lst_w_max) and lst_w_max[i] != move_to_make_value:
        i += 1
    print(i)
    return original_moves[i]


def get_average(lst: List[float]) -> float:
    """Returns the average of a set of values in a list.
    >>> avg1 = [3.5, 4.5]
    >>> get_average(avg1)
    4.5"""
    # return sum(lst) / len(lst)
    return max(lst)


def make_level_1_list(lst: Union[List[object], object]) -> List:
    """Return the average of each of the elements in the input list.
    >>> lst1 = [1, 2, [3, 4], 5, [6]]
    >>> make_level_1_list(lst1)
    [1, 2, 3, 4, 5, 6]"""
    if isinstance(lst, List) and any(isinstance(i, list) for i in lst):
        return sum([make_level_1_list(lst[i]) for i in range(len(lst))], [])
    elif isinstance(lst, List):
        return lst
    return [lst]


def recursive_minimax_helper(state: GameState, original_player: str)\
        -> Union[List, int]:
    """   Returns a move for the game input through using recursion to look at
    all possible moves and determining the best one for the user to choose.
    Helper to recursive_minimax.
    >>> from stonehenge_game import StonehengeGame
    >>> from stonehenge_gamestate import StonehengeGamestate
    >>> x1 = StonehengeGamestate(True, 2)
    >>> g1 = StonehengeGame(True, x1)
    >>> y = recursive_minimax_helper(x1, 'p1')
    >>> isinstance(y, List)
    True"""

    if state.get_possible_moves() == []:
        # if state.get_current_player_name() == original_player:
        #     return -1
        # return 1
        return -1

    return [recursive_minimax_helper(state.make_move(move), original_player)
            for move in state.get_possible_moves()]


def iterative_minimax(game: Any) -> Any:
    """ Finds the best possible moves without using recursion, instead using
    loops, tree structures, and stacks to determine the best possible moves
    from all of the possible moves to be made.
    >>> from stonehenge_game import StonehengeGame
    >>> from stonehenge_gamestate import StonehengeGamestate
    >>> x1 = StonehengeGamestate(True, 2)
    >>> g1 = StonehengeGame(True, x1)
    >>> iterative_minimax(g1)
    'A'"""
    shadow_game = game
    original_moves = game.current_state.get_possible_moves()
    current_state = game.current_state
    stored_states = []
    stack1 = Stack()
    stack1.add(Tree(current_state))
    i = 0

    while not stack1.is_empty():
        temp_tree = stack1.remove()
        if temp_tree.children == []:  # If no children currently
            for move in temp_tree.value.get_possible_moves():
                new_state = temp_tree.value.make_move(move)
                temp_tree.children.append(Tree(new_state))  # Type of children
                # is a tree, so it has a score also

        else:  # If there are children, get the max of their scores * - 1.
            to_max = []
            for subtree in temp_tree.children:
                to_max.append(subtree.score * -1)
            temp_tree.score = max(to_max)
            stored_states.append([temp_tree.value, temp_tree.score,
                                  temp_tree.part_of])

        if temp_tree.children == []:  # If still no children, i.e. no moves
            # to make...
            shadow_game.current_state = temp_tree.value
            if shadow_game.is_winner(temp_tree.value.get_current_player_name()):
                temp_tree.score = 1
            elif shadow_game.is_winner('p1'):
                temp_tree.score = -1
            elif shadow_game.is_winner('p2'):
                temp_tree.score = -1
            else:
                temp_tree.score = 0
            stored_states.append([temp_tree.value,
                                  temp_tree.score, temp_tree.part_of])
        elif temp_tree.score == 5:  # IF temp tree has children (so the state is
            # not at its end, and also the score has yet to be determined.
            stack1.add(temp_tree)
            for child in temp_tree.children:
                # print("child:")
                # print(child)
                child.part_of = True if i == 0 else False
                stack1.add(child)

        i += 1

    desired_state = find_desired_state(stored_states)
    move = find_which_move(original_moves, current_state, desired_state)
    return move


def find_which_move(original_moves: List, current_state: GameState,
                    desired_state: GameState) -> object:
    """Finds the move that outputs the desired game state.
    >>> from stonehenge_gamestate import StonehengeGamestate
    >>> x1 = StonehengeGamestate(True, 2)
    >>> x2 = x1.make_move('A')
    >>> find_which_move(x1.get_possible_moves(), x1, x2)
    'A'"""
    move = None
    for move in original_moves:  # for move in original_moves
        if str(current_state.make_move(move)) == str(desired_state):
            return move
    return move


def find_desired_state(stored_states: List) -> GameState:
    """Finds the desired state from all of the intermediate states of the game,
    which are stored in the list parameter. No doctest given since this relies
    on other methods."""
    current_state_children = []
    desired_state: GameState
    for item in stored_states:
        if len(item) == 3 and item[2]:
            current_state_children.append(item)
    first_state = stored_states[-1]
    for item in current_state_children:  # looks for the state that we want
        # to achieve.

        if item[1] == -1 * first_state[1]:
            desired_state = item[0]  # Desired state now has type gamestate
    return desired_state


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def find_max_state(lst: Union[List, int]) -> int:
    """Finds max state
    >>> lst = [1, 2, [3, 4, [5, 6], 7], 8]
    >>> find_max_state(lst)
    8
    """
    if isinstance(lst, List) and not any(isinstance(x, List) for x in lst):
        return max(lst)
    elif isinstance(lst, List):
        return max([find_max_state(obj) for obj in lst])
    else:
        return lst


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
    # x2 = StonehengeGamestate(True, 2)
    # ya = x2.make_move("C")
    # yb = ya.make_move("F")
    # yc = yb.make_move("D")
    # yd = yc.make_move("B")  # now it is p1's turn after this move is done.
    # g1 = StonehengeGame(True, yd)
    # # iterative_minimax(g1)
    # x2a = StonehengeGamestate(False, 2)
    # ye = x2a.make_move("C")
    # yf = ye.make_move("F")
    # yg = yf.make_move("D")
    # yh = yg.make_move("B")
    # g2a = StonehengeGame(True, yh)
    # s1 = StonehengeGamestate(True, 1)
    # g2 = StonehengeGame(True, s1)
    # s1 = SubtractSquareGame(True)
    # # s2 = SubtractSquareState(True, 5)
