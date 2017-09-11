"""
# Copyright Caleb D'Souza, 2017
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""
# Import requaired classes
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree


def build_tree(formula):
    """
    (str) -> FormulaTree
    If given a valid String representing a formula returns a FormulaTree
    representation of the given string formula, else given an invalid String
    formula returns None.
    REQ: A valid string
    REQ: len(formula) > -1
    >>> formula = '((-y*x)*-x)'
    >>> build_tree(formula)
    AndTree(AndTree(NotTree(Leaf('y')), Leaf('x')), NotTree(Leaf('x')))
    >>> formula = '((y*w)'
    >>> build_tree(formula)

    >>> formula = '( )'
    >>> build_tree(formula)

    >>> formula = '(a*)'
    >>> build_tree(formula)

    >>> formula = '(((a*b)'
    >>> build_tree(formula)

    >>> formula ='----(a*-b)'
    >>> build_tree(formula)
    NotTree(NotTree(NotTree(NotTree(AndTree(Leaf('a'), NotTree(Leaf('b')))))))
    >>> formula = '(F*s)'
    >>> build_tree(formula)

    >>> formula = ' '
    >>> build_tree(formula)

    >>> formula = '(-(y*(-x+z))'
    >>> build_tree(formula)

    >>> formula = '((a+b)*(c+d))'
    >>> build_tree(formula)
    AndTree(OrTree(Leaf('a'), Leaf('b')), OrTree(Leaf('c'), Leaf('d')))
    """
    # Store the operator version of the Not connective
    NOT_OPERATOR = "-"
    # Store the operator version of the Or connective
    OR_OPERATOR = "+"
    # Store the operator version of the And connective
    AND_OPERATOR = "*"
    # Determine the length of the given formula
    formula_lenght = len(formula)

    # Check if an empty string is given as a formual
    if(formula_lenght != 0):
        # Determine the first character in the given formula string
        first_character = formula[0]

        # Check if first character is a lower case alphabet or a Not operator
        if(formula_lenght == 1 and first_character.islower()):
            # If the first character is a lower case alphabet then build Leaf
            # and add it to the resultant Tree being built
            built_tree = Leaf(formula[0])

        elif(formula[0] == NOT_OPERATOR):
            # If the first character is a not operator;
            # Then first build the build the tree of the child for the Not node
            child_of_not_tree = build_tree(formula[1:])
            # Then build the NotTree node and add the built node to the
            # resultant Tree being built
            built_tree = NotTree(child_of_not_tree)

        else:
            # Then the first character is a Or or And operator
            # Therefore check if the given formula is a vaild And or Or formula
            if(formula_lenght > 2 and first_character == '(' and
               formula[-1] == ')'):
                # Keep a counter to track the position of each character in
                # the given formula while interating throught the given
                # formula string
                current_position = 1
                # Keep a tarck of the number of brakets in the given formula
                # string
                bracket_equilibrium_count = 0
                # Store the an operator that is in the current set of brackets
                current_operator_position = None

                # Go though each characher until an ANd or Or operator is found
                while(current_position < len(formula) and
                      not current_operator_position):

                    # Check if the current character for this formula is an
                    # open bracket
                    if(formula[current_position] == '('):
                        # Then oour bracket count is positivly out of
                        # equilibrium
                        bracket_equilibrium_count += 1

                    # Check if the current character for this formula is
                    # closed braket
                    elif(formula[current_position] == ')'):
                        # Then oour bracket count is negatively out of
                        # equilibrium
                        bracket_equilibrium_count -= 1

                    # Check if the braket count is in equilibrium and the
                    # current position is a either a And or Or opperator
                    if(bracket_equilibrium_count == 0 and
                       (formula[current_position] == OR_OPERATOR or
                        formula[current_position] == AND_OPERATOR)
                       ):
                        # Then keep track of the poition of the found
                        # Or or And operator
                        current_operator_position = current_position

                    # Move to the next position in the given formula string
                    current_position += 1

                # Check if an Or or And operator was found
                if(current_operator_position is not None):
                    # Build the left child tree of the found operator
                    left_tree = build_tree(formula[1:current_position-1])
                    # Build the right child tree of the foudn operator
                    right_tree = build_tree(
                        formula[current_position:formula_lenght-1])

                    # Check if the right and left child trees were valid and
                    # build
                    if(right_tree is not None and left_tree is not None):
                        # Determine wheather the found operator was an Or or
                        # And operator
                        if(formula[current_position-1] == OR_OPERATOR):
                            # Build the resultant OrTree node and add it to
                            # the resultant FormulaTree being built
                            built_tree = OrTree(left_tree, right_tree)

                        else:
                            # build the resultant AndTree node and add it to
                            # The resultant FOrmulaTree being built
                            built_tree = AndTree(left_tree, right_tree)
                    else:
                        # Then either the left or right child node were not
                        # built then the given formula string is not valid
                        built_tree = None

                else:
                    # Then an Or or And operator was not found then the given
                    # formula string is not valid
                    built_tree = None

            else:
                # Then the primary requirements for a basic Or or And operator
                # formula string where not met then the given formula is not
                # valid
                built_tree = None

    else:
        # Then an empty string was given as a formula string and therefore,
        # the given formula string is not vaild
        built_tree = None

    # Return the resultant built tree
    return built_tree


def draw_formula_tree(root):
    """
    (FormulaTree) -> str
    Given a root of a FormulaTree, return a string representation of the given
    FormulaTree, which draw the given FormulaTree so the whole Formula Tree
    is drawn rotated 90 degrees to the left where the parent and child are
    related by the level of indentation such that the children of the root are
    indented 2 spaces more.
    REQ: Must be given a vaild Tree
    >>> formula = '-a'
    >>> tree = build_tree(formula)
    >>> draw_formula_tree(tree)
    '- a'
    >>> formula = '-(a*b)'
    >>> tree = build_tree(formula)
    >>> draw_formula_tree(tree)
    '* - a\n  b'
    >>> formula = '((a+b)*-(-b+-a))'
    >>> tree = build_tree(formula)
    >>> draw_formula_tree(tree)
    '* - + - a\n      - b\n  + b\n    a'
    formula = '-((-a+b)*-c)'
    >>> tree = build_tree(formula)
    >>> draw_formula_tree(tree)
    '- * - c\n    + b\n      - a'
    """
    # Set the starting indentation level
    indentaion_level = 0
    # Draw the given FormulaTree into a string representation
    drawn_formula_tree = draw_formula_tree_helper(root, indentaion_level)
    # Strip the drawn formula tree of trailing spaces and new lines
    drawn_formula_tree = drawn_formula_tree.strip('\n')
    # Return the drawn string represntation of this formula tree
    return drawn_formula_tree


def evaluate(root, variables, values):
    """
    (FormulaTree, str, str) -> int
    Given the root of a Formula Tree representing a formula, a String list of
    variables form the given tree, and a String list of values which are the
    truth values for the corresponding given String of variables, uses
    the given variables and corresponding truth values to evalueate the
    Formula Tree, returng the evaluated truth value of the given Formula Tree
    which is either a 1 or 0.
    REQ: len(variables) == len(values)
    REQ: Root must be of a valid Formula Tree
    REQ: Each variable(character) in the variables must be a symbol of a Leaf
    in the given FormulaTree rooted at the root and there cannot be dupilcates
    for any of the variables (character) in the variable String
    REQ: veriables string must be all lower case
    REQ: no spaces in between the character for the variables and values
    strings
    >>> formula = 'a'
    >>> root = build_tree(formula)
    >>> variables = 'a'
    >>> values = '1'
    >>> evaluate(root, variables, values)
    1
    >>> formula = '(a*b)'
    >>> root = build_tree(formula)
    >>> variables = 'ab'
    >>> values = '10'
    >>> evaluate(root, variables, values)
    0
    >>> formula = '(a*-b)'
    >>> root = build_tree(formula)
    >>> variables = 'ab'
    >>> values = '10'
    >>> evaluate(root, variables, values)
    1
    >>> formula = '((a*-b)*(-b+c))'
    >>> root = build_tree(formula)
    >>> variables = 'abc'
    >>> values = '101'
    >>> evaluate(root, variables, values)
    1
    >>> formula = '(-a*(-b+-c))'
    >>> root = build_tree(formula)
    >>> variables = 'abc'
    >>> values = '101'
    >>> evaluate(root, variables, values)
    0
    >>> formula = '(-a*(((b+c)*-b)+c))'
    >>> root = build_tree(formula)
    >>> variables = 'abc'
    >>> values = '101'
    >>> evaluate(root, variables, values)
    0
    """
    # Determine if the current given root node is a Leaf
    if(isinstance(root, Leaf)):
        # Find the index value of this current Leaf symbol in the given list
        # of variables
        index_value = variables.find(root.symbol)
        # Find the corresponding value to this current Leasf symbol(variable)
        resultant_value = int(values[index_value])
    else:

        # Determine if the current given root node is a OrTree or NotTree
        if(isinstance(root, NotTree)):
            # Thne this current given root node is a NotTree node therefore:
            # Get the only child of this NotTree node
            child = root.children[0]
            # Determine the given value of this node's only child
            given_value = evaluate(child, variables, values)
            # Determine the resultant truth value
            resultant_value = (given_value - 1) * -1

        elif(isinstance(root, OrTree)):
            # Then this current given root node is an OrTree therefore:
            # Get the left child of this OrTree node
            left_child = root.children[0]
            # Get the given evaluation of the left child for this OrTree node
            left_given_value = evaluate(left_child, variables, values)
            # Get teh right child of tis OrTree node
            right_child = root.children[1]
            # Get the given evaluation of the right child for this OrTree node
            right_given_value = evaluate(right_child, variables, values)
            # Evaluate this OrTree node by determining the maxinum value
            # between the left and right child
            resultant_value = max(left_given_value, right_given_value)

        else:
            # Then the this current given root node is an AndTree therefore:
            # Get the left child of this AndTree node
            left_child = root.children[0]
            # Get the given evaluation of the left child for this AndTree node
            left_given_value = evaluate(left_child, variables, values)
            # Get teh right child of tis AndTree node
            right_child = root.children[1]
            # Get the given evaluation of the right child for this AndTree node
            right_given_value = evaluate(right_child, variables, values)
            # Evaluate this AndTree node by determining the minimum value
            # between the left and right child
            resultant_value = min(left_given_value, right_given_value)

    # Return the found resultant evaluation for the current given node
    return int(resultant_value)


def play2win(root, turns, variables, values):
    """
    (FormulaTree, str, str, str) -> int
    Given the root of a Formula Tree representing a formula, turns for Players
    E and A that correspond to the given given veriables, a String list of
    variables form the given tree, and a String list of values which are the
    truth value choice of each player respectively for the corresponding given
    String of variables, this creates a game configuration and returns the
    best move that will allow player who's next turn it is to win such that
    ifthere is no winning strategy, or if choosing either 1 or 0 results in a
    win then 1 is returned if it is player E’s turn, and 0 is returned if it
    is player A’s turn.
    REQ: len(turns) > len(values)
    REQ: Each variable(character) in the variables must be a symbol of a Leaf
    in the given FormulaTree rooted at the root and there cannot be dupilcates
    for any of the variables (character) in the variable String
    REQ: Must be given a root of a vaild formual Tree
    REQ: veriables string must be all lower case
    REQ: no spaces in between the character for the variables and values
    strings
    REQ: turns must consist of only 'E' or 'A' characters
    >>> formula = '(a+b)'
    >>> root = build_tree(formula)
    >>> variables = 'ab'
    >>> values = ''
    >>> turns = 'AE'
    play2win(root,turns, variables, values)
    0
    >>> formula = '(((a+b)+c)*-d)'
    >>> root = build_tree(formula)
    >>> variables = 'ab'
    >>> values = ''
    >>> turns = 'AE'
    >>> play2win(root,turns, variables, values)
    0
    >>> formula = '(((a+b)+c)*-d)'
    >>> root = build_tree(formula)
    >>> variables = 'abcd'
    >>> values = '11'
    >>> turns = 'AEEA'
    >>> play2win(root,turns, variables, values))
    1
    """
    # Determine the next best move the next player and whihc player(s) win
    winning_move_data = play2win_helper(root, turns, variables, values)
    # Store the integer representation of winning move for the next player
    winning_move = int(winning_move_data[2])
    # Return the winning move for the next player
    return winning_move

# HELPER FUNCTIONS


def draw_formula_tree_helper(root, current_level):
    """
    (FormulaTree, int) -> str
    Given a root of a FormulaTree, and a current indendtaion quantity,
    return a string representation of the given Formula Tree, which draw
    the given FormulaTree so the whole Formula Tree is drawn rotated 90
    degrees to the left where the parent and child are related by the level of
    indentation such that the children of the root are indented 2 spaces more
    and parent is indented based on the current given indendtation quantity.
    REQ: Must be given a valid root of a Formula Tree
    REQ: current_level > -1
    >>> formula = '---a'
    >>> tree = build_tree(formula)
    >>> draw_formula_tree_helper(tree, 0)
    '- - - a\n'
    >>> formula = '(a+b)'
    >>> root = build_tree(formula)
    >>> draw_formula_tree_helper(root, 0)
    '+ b\n  a\n'
    >>> formula = '(((a+b)+(a*b))*-c)'
    >>> root = build_tree(formula)
    >>> draw_formula_tree_helper(root, 0)
    '* - c\n  + * b\n      a\n    + b\n      a\n'
    """
    # Increase the current indentaiton level for the child nodes
    current_level += 2

    # Check if the given root for a FormulaTree is None
    if(root is not None):
        # Check current root node is a leaf or NotTree node
        if(isinstance(root, Leaf)):
            # If the current root node is a Leaf node then add the symbol
            # of this Leaf to the drawn string and start a new line of the
            # other child
            drawn_string = root.symbol + '\n'

        elif(isinstance(root, NotTree)):
            # If the current root node is a NotTree node then add the symbol
            # of this NotTree to the draw stirng
            drawn_string = root.symbol
            # And then add the child of this NotTree to the drawn string
            # properly spaced out
            drawn_string += ' ' + draw_formula_tree_helper(root.children[0],
                                                           current_level)

        else:
            # Then the current root node must be either a OrTree or an AndTree
            # which both have two children meaning it's a BinaryTree
            # Therefore, add the symol of this current root node to the
            # resultant drawn string
            drawn_string = root.symbol
            # Add the right child of this current root node to the drawn
            # string with proper spacing first so that this child is on the
            # right side of the drawn stirng representation of the
            # Formula Tree
            drawn_string += ' ' + draw_formula_tree_helper(root.children[1],
                                                           current_level)
            # Add the left child of this current root node to the drawn
            # string wiht proper spacing first so that this child is on the
            # left side of the drawn string representation of this given
            # Formula Tree
            drawn_string += (' ' * current_level +
                             draw_formula_tree_helper(root.children[0],
                                                      current_level))

    else:
        # Then the given root node is None therefore nothing should be drawn
        # in the string representation
        drawn_string = ''

    # Returnt the resultant drawn string representation of the current given
    # FormulaTree
    return drawn_string


def play2win_helper(root, turns, variables, values):
    """
    (FormulaTree, str, str, str) -> tuple of bool and str
    Given the root of a Formula Tree representing a formula, turns for Players
    E and A that correspond to the given given veriables, a String list of
    variables form the given tree, and a String list of values which are the
    truth value choice of each player respectively for the corresponding given
    String of variables, this creates a game configuration and returns a
    tuple so that the of wether Player A will win or wether player E will win
    And the move that causes that result such that if there is no winning
    strategy, or if choosing either 1 or 0 results in win then 1 is returned
    if it is player E’s turn, and 0 is returned if it
    is player A’s turn.
    REQ: len(turns) > len(values)
    REQ: Each variable(character) in the variables must be a symbol of a Leaf
    in the given FormulaTree rooted at the root and there cannot be dupilcates
    for any of the variables (character) in the variable String
    REQ: Must be given a root of a vaild formual Tree
    REQ: veriables string must be all lower case
    REQ: no spaces in between the character for the variables and values
    strings
    REQ: turns must consist of only 'E' or 'A' characters
    >>> formula = '(b+c)'
    >>> root = build_tree(formula)
    >>> variables = 'ab'
    >>> values = ''
    >>> turns = 'EA'
    >>> play2win_helper(root,turns, variables, values)
    (True, False, '1')
    >>> formula = '(b+c)'
    >>> root = build_tree(formula)
    >>> variables = 'ab'
    >>> values = ''
    >>> turns = 'EA'
    >>> play2win_helper(root,turns, variables, values)
    (True, False, '1')
    >>> formula = '((b+c)*(a+-c))'
    >>> root = build_tree(formula)
    >>> variables = 'abc'
    >>> values = ''
    >>> turns = 'EAE'
    >>> play2win_helper(root,turns, variables, values)
    (False, True, '1')
    >>> formula = '((b*c)*(a*-c))'
    >>> root = build_tree(formula)
    >>> variables = 'abc'
    >>> values = ''
    >>> turns = 'EAE'
    >>> play2win_helper(root,turns, variables, values)
    (True, True, '1')
    >>> formula = '(a*(a*-c))'
    >>> root = build_tree(formula)
    >>> variables = 'abc'
    >>> values = '1'
    >>> turns = 'AAE'
    >>> play2win_helper(root,turns, variables, values)
    (False, True, '0')
    >>> formula = '(a*-c)'
    >>> root = build_tree(formula)
    >>> variables = 'abc'
    >>> values = '01'
    >>> turns = 'AAE'
    >>> play2win_helper(root,turns, variables, values)
    (True, True, '1')
    """
    # Check if the next player is the last turn for the game
    if(len(turns)-1 == len(values)):
        # Determine the evaluation if the the next player's move is a 1
        evaluated_for_one = evaluate(root, variables, values+"1")
        # Determine the evaluation if the the next player's move is a 0
        evaluated_for_zero = evaluate(root, variables, values+"0")

        # Check if the the last turn is player E's turn or player A's turn
        if(turns[-1] == "E"):
            # Check if which move, if both or no move, of 1 or 0, result in
            # player E winning meaning the evaluation of the formula is 1
            if(evaluated_for_one == 1 and evaluated_for_zero == 1):
                # If both 1 and 0 allow player E to win then player E's
                # winning move should be 1
                play2win_move = (False, True, "1")

            elif(evaluated_for_one == 1):
                # If only 1 allows player E to win then player E's
                # winning move is 1
                play2win_move = (False, True, "1")

            elif(evaluated_for_zero == 1):
                # If only 0 allows player E to win then player E's
                # winning move is 0
                play2win_move = (False, True, "0")
            else:
                # If neither 1 or 0 allow player E to win then player E's
                # best chance of a winning move is 1 since that's E's goal
                # and player A or player E could win
                play2win_move = (True, True, "1")
        else:
            # Check if which move, if both or no move, of 1 or 0, result in
            # player A winning meaning the evaluation of the formula is 0
            if(evaluated_for_one == 0 and evaluated_for_zero == 0):
                # If both 1 and 0 allow player A to win then player A's
                # winning move should be 0
                play2win_move = (True, False, "0")
            elif(evaluated_for_one == 0):
                # If only 1 allows player A to win then player A's
                # winning move is 1
                play2win_move = (True, False, "1")

            elif(evaluated_for_zero == 0):
                # If only 0 allows player A to win then player A's
                # winning move is 0
                play2win_move = (True, False, "0")
            else:
                # If neither 1 or 0 allow player A to win then player A's
                # best chance of a winning move is 1 since that's A's goal
                play2win_move = (True, False, "0")

    else:
        # Get the resultant data of the which player wins if 0 is the next
        # move
        does_A_win0, does_E_win0, move_0 = play2win_helper(root, turns,
                                                           variables,
                                                           values + "0")
        # Get the resultant data of the which player wins if 1 is the next
        # move
        does_A_win1, does_E_win1, move_1 = play2win_helper(root, turns,
                                                           variables,
                                                           values + "1")

        # Check if it's player A's turn or player E's turn
        if(turns[len(values)] == "E"):
            # Check if player E can win by either choosing 1 or 0
            if(does_E_win0 and not does_A_win0 and
               does_E_win1 and not does_A_win1):
                # Then player E wins by using it's default move of 1
                play2win_move = (False, True, "1")

            # Check if player E can win by choosing 0
            elif(does_E_win0 and not does_A_win0):
                # Then player E wins by using it's default move of 0
                play2win_move = (False, True, "0")

            # Check if player E can win by choosing 1
            elif(does_E_win1 and not does_A_win1):
                # Then player E wins by using it's default move of 0
                play2win_move = (False, True, "1")

            # Then player E and A can both win no mater what move player E
            # makes
            elif(does_E_win0 and does_A_win0 or does_E_win1 and does_A_win1):
                # The player E should just choose it's default move of 1
                play2win_move = (True, True, "1")

            # Then no matter what player E chooses E's loses
            else:
                # Then player E show just choose it's default move of 1
                play2win_move = (True, False, "1")

        else:
            # Check if player A can win by either choosing 1 or 0
            if(does_A_win0 and not does_E_win0 and
               does_A_win1 and not does_E_win1):
                # Then player A wins by using it's default move of 0
                play2win_move = (True, False, "0")

            # Check if player A can win by choosing 0
            elif(does_A_win0 and not does_E_win0):
                # Then player A wins by using it's default move of 0
                play2win_move = (True, False, "0")

            # Check if player A can win by choosing 1
            elif(does_A_win1 and not does_E_win1):
                # Then player A wins by using it's default move of 0
                play2win_move = (True, False, "1")

            # Then player A and E can both win no mater what move player A
            # makes
            elif(does_E_win0 and does_A_win0 or does_E_win1 and does_A_win1):
                # The player A should just choose it's default move of 1
                play2win_move = (True, True, "0")

            # Then no matter what player A chooses A's loses
            else:
                # Then player A show just choose it's default move of 1
                play2win_move = (False, True, "0")

    # Return the resulting play to win move data
    return play2win_move
