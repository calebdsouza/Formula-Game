from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree
from formula_game_functions import build_tree, evaluate, play2win

def get_formula():
    got_good_formula = False
    while not got_good_formula:
        formula = input("Please enter formula: ")
        root = build_tree(formula)
        got_good_formula = (root != None)
        if not got_good_formula:
            print("invalid formula")
    return (formula, root)

def get_variables(formula):
    got_good_variables = False
    while not got_good_variables:
        variables = input("Please enter order of variables to assign: ")
        got_good_variables = True
        for x in variables:
            if not (x in formula):
                print("variable", x, "not in formula")
                got_good_variables = False
            elif (variables.count(x) > 1):
                print("variable", x, "appears more than once")
                got_good_variables = False
        for c in formula:
            if c.islower() and not (c in variables):
                print("variable", c, "not entered")
                got_good_variables = False
    return variables

def get_turns(num_variables):
    got_good_turns = False
    while not got_good_turns:
        turns = input("Please enter turns of players E and A: ")
        got_good_turns = True
        for p in turns:
            if p != 'E' and p != 'A':
                print(p, "is not a valid player")
                got_good_turns = False
        if len(turns) > num_variables:
            print("too many turns for number of variables")
            got_good_turns = False
        elif len(turns) < num_variables:
            print("too few turns for number of variables")
            got_good_turns = False
    return turns

def get_value(turns, variables, currturn):
    got_good_newval = False
    while not got_good_newval:
        newval = input("Player " + turns[currturn] +
                       " please enter value for variable " +
                       variables[currturn] + "[0/1/C(omputer)]: ")
        got_good_newval = (len(newval)==1) and (newval in "01C")
        if not got_good_newval:
            print("enter just one symbol (0 or 1 or C)")
    return newval

def play_game():
    (formula, root) = get_formula()

    variables = get_variables(formula)

    turns = get_turns(len(variables))

    values = ""
    for i in range(len(turns)):
        print("Turn", i)
        print("Formula:", formula)
        print("Turns:        ", turns)
        print("Variables:    ", variables)
        print("Values played:", values)
        newval = get_value(turns, variables, i)
        if newval == 'C':
            newval = str(play2win(root, turns, variables, values))
        values = values + newval

    print("Game over")
    print("Formula:", formula)
    print("Turns:        ", turns)
    print("Variables:    ", variables)
    print("Values played:", values)
    if evaluate(root, variables, values) == 1:
        winner = 'E'
    else:
        winner = 'A'
    print("Player", winner, "wins!")

if __name__ == "__main__":
    print("Hey Sherry! :D\nThis is the Formula Game, which is a fun " +
          "little activity to test your reasoning skills and knowledge of"
          " boolean logic!")
    play_game()





# Helper functions
def is_valid(formula, start_index, end_index):
    """
    (str) -> bool
    Given a string formula, returns true if the given formula is valid,
    otherwises, returns False if the given formula is not valid.
    REQ: The given string cannot be empty
    >>> forumla ='((-y*x)*(z+-x))'
    >>> is_valid(formula)
    True
    >>> forumla ='-y)*(z+-x)'
    >>> is_valid(formula)
    False
    """
    # Check the length of the foumula
    # if the length is one
    if(len(formula) == 1):
        # Then check if the that single element is a lower case letter
        if(formula[0].islower):
            # Then the given formula is valid
            is_valid = True
        else:
            # Then the given formula is not valid
            is_valid = False
    # Else check if the length of the formula is two
    elif(len(formula) == 2): 
        # Then check if the first token a negative sign
        if(formula[0] == '-'):
            # And check if the second token is a lower case letter
            if(formula[1].islower):
                # Then the given foumla is valid
                is_valid = True
            else:
                # Then the fiven formula is not valid
                is_valid = False
        else: 
            # Then the given forula is not valid
            is_valid = True
    # Else check if the formula has a length of 5
    elif(len(formula) == 5):
        # Then check if the first element
        pass
    
def find_all_or_and(formmula):
    """
    (str)->list of int
    Given a string representation of a forumla return a list of of integers, 
    representing the psoitoin indexes of all the OR and AND connectives in the
    given formula.
    REQ: len(formula) > 3
    """
    # Create a place to store all the indexes found
    all_or_and = []
    # Create a counter to store the current index position
    current_position = 0
    
    # Loop through each character in the string
    for position_index in range(len(formula)):
        # Check if the current character in the list is a OR or AND
        # connective
        if(formula[position_index] == '+' or formula[position_index] == '*'):
            # Add the current position index to the list
            all_or_and.append(position_index)
    # Return the list of found indexes
    return all_or_and



def draw_formula_tree_helper(root, depth):
    """
    (FormulaTree, depth) -> str
    """
    depth += 2
    if(root is not None):
        if(isinstance(root, Leaf)):
            drawn_string = root.symbol + '\n'
        elif(isinstance(root, NotTree)):
            drawn_string = root.symbol
            drawn_string += ' '+draw_formula_tree_helper(root.children[0], depth)
        else:
            if(isinstance(root, list)):
                number_of_children = len(root)
            else:
                number_of_children = len(root.children)

            drawn_string = draw_children_helper(root, depth, number_of_children)
            drawn_string = root.symbol + drawn_string

    return drawn_string


def draw_children_helper(root, depth, number_of_children):
    """
    """
    if(isinstance(root, list)):
        root = root[0]
    if(number_of_children == 1):
        drawn_string = ' ' + draw_formula_tree_helper(root.children[0], depth)
    else: 
        drawn_string = ' ' + draw_formula_tree_helper(root.children[:1], depth)
        drawn_string = ' '*depth +draw_formula_tree_helper(root.children[0], depth)
    return drawn_string