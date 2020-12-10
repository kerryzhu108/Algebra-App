import sympy
import random


def simplify(equation: list)-> list:
    """Takes in an equation in the form of a list
    such as:
    [20, '•', 'x', '+', 6, '•', 3, '•', 7, '/', 2, '=', 30]
    and returns the simplified version in the same format:
    [20, '•', 'x', '+', 63, '=', 30]
    """
    left_of_eq = ""
    right_of_eq = ""
    # split equation into left and right of equal sign then simplify both sides
    i = 0
    while i < len(equation) and equation[i] != '=':
        if equation[i] == "\u2022":
            left_of_eq += '*'
        else:
            left_of_eq += str(equation[i])
        i += 1
    i += 1
    while i < len(equation):
        if equation[i] == "\u2022":
            right_of_eq += '*'
        else:
            right_of_eq += str(equation[i])
        i += 1
    simplified = str(sympy.simplify(left_of_eq))
    if right_of_eq:
        simplified += '=' + str(sympy.simplify(right_of_eq))
    # turn string back into list format
    simplified_list = []
    i = 0
    while i < len(simplified):
        # if ch is a num, keep collecting until operator is found as to collect entire number
        if simplified[i].isnumeric():
            number = simplified[i]
            j = i + 1
            while j < len(simplified) and (simplified[j].isdigit() or simplified[j] in ".x"):
                number += simplified[j]
                j += 1
            simplified_list.append(int(float(number)))
            i = j-1
        elif simplified[i] == '*':
            simplified_list.append('\u2022')
        elif simplified[i] != ' ':
            simplified_list.append(simplified[i])
        i += 1
    return simplified_list


def shift_denominators(equation: list) -> None:
    """Takes a equation_list of floats and strings as signs
    and shifts the denominator sign+number(s) to the end of
    the multiplication chain.
    >>> eq = [2, '+', 6, '/', 2, '\u2022', 3, '\u2022', 7, '=', 30]
    >>> shift_denominators(eq)
    >>> eq
    [2, '+', 6, '\u2022', 3, '\u2022', 7, '/', 2, '=', 30]
    """
    for i in range(len(equation)-3):
        if equation[i] == '/' and equation[i+2] == '\u2022':
            equation[i], equation[i+2] = equation[i+2], equation[i]
            equation[i+1], equation[i+3] = equation[i+3], equation[i+1]
    for i in range(len(equation) - 3):
        if equation[i] == '/' and equation[i + 2] == '\u2022':
            shift_denominators(equation)


def equation_gen(num: int) -> list:
    """
    Returns a random equation broken up and stored in a list
    with an x variable. Second element in returned list will be answer.
    Equations are randomly generated by 'num' of terms desired.
    Denominators will always be at end of multiplication chain.
    (see example 3)

    >> equation_gen(3)
    [x, '\u2022', 2, '+', 3, '=', 19], 8]
    >> equation_gen(5)
    [[7, '/', 6, '/', x, '-', 3, '\u2022', 9, '=', '-', 26.42], 2]
    >> equation_gen(5)
    [[2, '+', x, '\u2022', 2, '\u2022', 3, '/', 7, '=', 30], 6]
    """
    possible_nums = []
    for i in range(num):
        possible_nums.append(random.randint(1, 9))
    equation_list = []
    for number in range(num):
        equation_list.append(possible_nums[number])
    i = 1
    operators = ['+', '-', '\u2022', '/']  # '\u2022' = '*' for multiplication
    while i < len(equation_list):
        random_operator = operators[random.randint(0, len(operators)-1)]

        equation_list.insert(i, random_operator)
        # if there's about to be a zero division error, generate a new num > 0
        if random_operator == '/' and equation_list[i+1] == 0:
            equation_list[i+1] = random.randint(1, 9)
        i += 2
    shift_denominators(equation_list)
    total = simplify(equation_list)[0]
    if total < 0:
        equation_list.extend(['=', '-', abs(total)])
    else:
        equation_list.extend(['=', abs(total)])
    good_num = False
    x_insert_position = 0
    while not good_num:
        x_insert_position = random.randint(2, len(equation_list)-2)
        if x_insert_position % 2 == 0:
            good_num = True
    ans = equation_list[x_insert_position]
    equation_list[x_insert_position] = 'x'
    return [equation_list, str(ans)]
