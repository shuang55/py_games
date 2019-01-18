"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
import copy
from typing import Union
from typing import Any
from tree_api import Tree
from stack_api import Stack

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Implement a recursive version of the minimax strategy.


def recursive_minimax_strategy(game: Any)-> Any:
    """A recursive minimax strategy
    """
    current_state = game.current_state
    result_list = []
    poss_moves = current_state.get_possible_moves()
    for i in range(len(poss_moves)):
        # this is the recursive step (since
        # recursive_minimax_helper is recursive)
        resultant_state_score = \
            recursive_minimax_helper(game,
                                     current_state.make_move(
                                         game.str_to_move(str(poss_moves[i]))))
        result_list.append(-1 * resultant_state_score)
    best_move = max(result_list)
    best_move_index = result_list.index(best_move)
    return poss_moves[best_move_index]


def recursive_minimax_helper(game: Any, state: Any)->int:
    """Return the score of state, recursively.
    This is the recursive step in recursive_minimax_strategy
    """
    old_state = game.current_state
    game.current_state = state
    current_player = state.get_current_player_name()
    if game.is_over(state):
        if game.is_winner('p1'):
            winner_name = 'p1'
        elif game.is_winner('p2'):
            winner_name = 'p2'
        else:
            game.current_state = old_state
            return 0
        game.current_state = old_state
        return 1 if winner_name == current_player else -1
    else:
        game.current_state = old_state
        return max([-1 *
                    recursive_minimax_helper(
                        game, state.make_move(game.str_to_move(str(x))))
                    for x in state.get_possible_moves()])


# TODO: Implement an iterative version of the minimax strategy.
def iterative_minimax_strategy(game: Any)-> Any:
    """An iterative implementation of minimax strategy """
    initial_root = Tree(game)
    stack_of_tree_games = Stack()
    stack_of_tree_games.add(initial_root)
    # in a loop, do the following (until the stack is empty):
    while not stack_of_tree_games.is_empty():
        # get item at the top of the stack_of_games
        top = stack_of_tree_games.remove()
        # if the state of the item is over, set the Tree's score
        # the score is -1 for a loss, 0 for a draw, and 1 for a win
        if top.value.is_over(top.value.current_state):
            set_tree_score(top)
        # elif we haven't looked at this node (it has no children)
        elif top.children == []:
            # create new items, which are the result of
            # applying each possible move to the current state.
            # we store these children in a list for now w/ a helper function
            create_children(top)
            stack_of_tree_games.add(top)
            for child in top.children:
                stack_of_tree_games.add(child)
        else:
            # we've looked at this state before top.children is not None
            children_score = [(-1 * x.score) for x in top.children]
            top.score = max(children_score)
    best_score = initial_root.score
    for child in initial_root.children:
        if (-1 * child.score) == best_score:
            correct_resultant = child
            break
    return correct_resultant.move


# ===========start helper functions=======================


def set_tree_score(tree: Union[Tree, object])->None:
    """
    Set tree's score to be 1 for 1 win, 0 for a tie, and
    -1 for a loss. This is a helper function for
    iterative_minimax_strategy
    precondition: tree.value is a Game
    """
    game = tree.value
    current_player = game.current_state.get_current_player_name()
    if game.is_winner('p1'):
        winner = 'p1'
    elif game.is_winner('p2'):
        winner = 'p2'
    else:
        winner = 'tie'

    if winner == 'tie':
        tree.score = 0
    else:
        tree.score = 1 if current_player == winner\
            else -1


def create_children(tree: Union[Tree, object])->None:
    """A helper function for iterative_minimax_strategy
    This function takes in a tree (with a game as value
    and makes its children
    the possible states that can result from making a move
    on the game.
    precondition: tree.value is a game
    """
    game = tree.value
    state = game.current_state
    poss_moves = state.get_possible_moves()
    for move in poss_moves:
        tree_child = copy.deepcopy(tree.value)
        tree_child.current_state = state.make_move(game.str_to_move(str(move)))
        t = Tree(tree_child)
        t.move = move
        tree.children.append(t)


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
