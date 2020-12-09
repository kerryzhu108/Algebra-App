import random
"""
Helper for this file: Liam Ogilvie 
"""


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


def cleanerupper(given: list) -> list:
    # Version 1.2.0 June 13 2020
    # [C] Liam Ogilvie
    """Given an list with a negative number, separate it to a string element and int/float.
    Returns the modified list."""
    cleaned = []
    for i in range(len(given)):
        try:
            if given[i] < 0 and i != 0:
                cleaned.append(0)
                cleaned.append("-")
                cleaned.append(abs(given[i]))
            else:
                cleaned.append(given[i])
        except TypeError:
            cleaned.append(given[i])

    for item in cleaned:
        if item == "+":
            if cleaned[cleaned.index("+")+1] == "-":
                cleaned.remove("+")
        if item == "x":
            i = cleaned.index("x")
            cleaned[i] = "1x"
    if cleaned[0] == '-':
        if '.' in str(cleaned[1]):
            cleaned[1] = float(cleaned[1]) - (2*float(cleaned[1]))
        else:
            cleaned[1] = int(cleaned[1]) - (2*int(cleaned[1]))
        cleaned.pop(0)
    if cleaned[0] == '+':
        cleaned.pop(0)
    return cleaned


def listmas(expr: list) -> list:
    # Version 2.1.1 June 13 2020
    # precondition: list is a valid expression
    # [C] Liam Ogilvie
    # After the May rewrite, it's extremely messy, consider this a warning.
    """Preforms bedmas on list"""
    expr = cleanerupper(expr)
    expr2 = []
    for element in expr:
        # allows it to also handle numbers in strings and '—' instead of '/'
        if element == '—':
            expr2.append('/')
        else:
            try:
                expr2.append(float(element))
            except:
                expr2.append(element)
    order = 'e'
    bedmas = ['e', 'd', 'a', 'done']
    x = 0
    expr = []
    for i in range(len(expr2)):
        expr.append(expr2[i])
    i = 1
    while order != 'done' and len(expr) > 1:
        if expr[i] == '**' and order == 'e':
            arg1 = expr[expr.index('**')-1]
            arg2 = expr[expr.index('**')+1]
            expr[i] = arg1 ** arg2
            expr.pop(i+1)
            expr.pop(i-1)
            i = 1
            if len(expr) == 1:
                break

        elif expr[i] == '/' and order == 'd':
            arg1 = expr[expr.index('/')-1]
            arg2 = expr[expr.index('/')+1]
            xis = False
            if 'x' in str(arg1):
                arg1 = float(arg1[:-1])
                xis = True
            elif 'x' in str(arg2):
                arg2 = float(arg2[:-1])
                xis = True
            if xis is True:
                expr[i] = str(arg1 / arg2)+'x'
            else:
                expr[i] = arg1 / arg2
            expr.pop(i+1)
            expr.pop(i-1)

            i = 1
            if len(expr) == 1:
                break

        elif expr[i] == '\u2022' and order == 'd':
            arg1 = expr[expr.index('\u2022')-1]  # '\u2022' == '*'
            arg2 = expr[expr.index('\u2022')+1]
            xis = False
            if 'x' in str(arg1):
                arg1 = float(arg1[:-1])
                xis = True
            elif 'x' in str(arg2):
                arg2 = float(arg2[:-1])
                xis = True
            if xis is True:
                expr[i] = str(arg1 * arg2)+'x'
            else:
                expr[i] = arg1 * arg2
            expr.pop(i+1)
            expr.pop(i-1)

            i = 1
            if len(expr) == 1:
                break

        elif i < len(expr) != 1:
            if i+2 >= len(expr):

                x += 1
                order = bedmas[x]
                i = 1
            else:
                i += 2

    xlist = []
    expr3 = []
    for item in expr:
        expr3.append(item)
    for i in range(len(expr3)):
        if 'x' in str(expr3[i]):
            if i != 0:
                xlist.append(expr3[i-1])
                expr.pop(i-(len(expr3)-len(expr))-1)
            xlist.append(expr3[i][:-1])
            expr.pop(i-(len(expr3)-len(expr)))
    if len(expr) == 0:
        expr.append(0)
    if len(xlist) == 0:
        xlist.append(0)
    expr = cleanerupper(expr)
    expr2 = []
    for element in expr:
        # allows it to also handle numbers in strings and '—' instead of '/'
        if element == '—':
            expr2.append('/')
        else:
            try:
                expr2.append(float(element))
            except:
                expr2.append(element)
    # total = 0
    order = 'a'
    bedmas = ['e', 'd', 'a', 'done']
    # bedmas = ['e', 'd', 'm', 'a', 's', 'done']
    x = 2
    # used = []
    expr = []
    for i in range(len(expr2)):
        expr.append(expr2[i])
    i = 1
    while order != 'done' and len(expr) > 1:
        # print("i "+ str(i))
        if expr[i] == '+' and order == 'a':
            # expr[i] = expr[expr.index('**')-1] ** expr[expr.index('**')+1]
            arg1 = expr[expr.index('+')-1]
            arg2 = expr[expr.index('+')+1]
            expr[i] = arg1 + arg2
            expr.pop(i+1)
            expr.pop(i-1)

            i = 1
            if len(expr) == 1:
                break

        elif expr[i] == '-' and order == 'a':
            # expr[i] = expr[expr.index('**')-1] ** expr[expr.index('**')+1]
            arg1 = expr[expr.index('-')-1]
            arg2 = expr[expr.index('-')+1]
            expr[i] = arg1 - arg2
            expr.pop(i+1)
            expr.pop(i-1)
            i = 1
            if len(expr) == 1:
                break

        elif len(expr) == 1:
            break

        elif i < len(expr) != 1:
            if i+2 >= len(expr):

                x += 1
                order = bedmas[x]
                i = 1
            else:
                i += 2
    xlist = cleanerupper(xlist)
    expr2 = []
    for element in xlist:
        # allows it to also handle numbers in strings and '—' instead of '/'
        if element == '—':
            expr2.append('/')
        else:
            try:
                expr2.append(float(element))
            except:
                expr2.append(element)
    # total = 0
    order = 'a'
    bedmas = ['e', 'd', 'a', 'done']
    # bedmas = ['e', 'd', 'm', 'a', 's', 'done']
    i = 1
    x = 2
    # used = []
    xlist = []
    for i in range(len(expr2)):
        xlist.append(expr2[i])
    # print(expr)
    i = 1
    while order != 'done' and len(xlist) > 1:
        # print("i "+ str(i))
        if xlist[i] == '+' and order == 'a':
            # expr[i] = expr[expr.index('**')-1] ** expr[expr.index('**')+1]
            arg1 = xlist[xlist.index('+')-1]
            arg2 = xlist[xlist.index('+')+1]
            xlist[i] = arg1 + arg2
            xlist.pop(i+1)
            xlist.pop(i-1)

            i = 1
            if len(xlist) == 1:
                break

        elif xlist[i] == '-' and order == 'a':
            # expr[i] = expr[expr.index('**')-1] ** expr[expr.index('**')+1]
            arg1 = xlist[xlist.index('-')-1]
            arg2 = xlist[xlist.index('-')+1]
            xlist[i] = arg1 - arg2
            xlist.pop(i+1)
            xlist.pop(i-1)
            i = 1
            if len(xlist) == 1:
                break

        elif len(xlist) == 1:
            break

        elif i < len(xlist) != 1:
            if i+2 >= len(xlist):

                x += 1
                order = bedmas[x]
                i = 1
            else:
                # print('iiiii')
                i += 2
    result = []
    if xlist[0] != 0:
        if '.' in str(xlist[0]):
            if str(xlist[0])[str(xlist[0]).find('.')+1] == '0':
                result.append(str(int(str(xlist[0])[:str(xlist[0]).find('.')]))+'x')
            else:
                result.append(str(float(str(xlist[0])[:str(xlist[0]).find('.')+1]))+'x')
        else:
            result.append(str(int(str(xlist[0])))+'x')
    if expr[0] > 0:
        result.append('+')
    elif expr[0] < 0:
        result.append('-')
        expr[0] = str(expr[0])[1:]
    if expr[0] != 0:
        if '.' in str(expr[0]):
            if str(expr[0])[str(expr[0]).find('.')+1] == '0':
                result.append(int(str(expr[0])[:str(expr[0]).find('.')]))
            else:
                result.append(float(str(expr[0])[:str(expr[0]).find('.')+1]))
        else:
            result.append(int(str(expr[0])))
    if result == []:
        result = [0]
    result = cleanerupper(result)
    return result


answer = None
def equation_gen(num: int) -> list:
    """
    Returns a random equation broken up and stored in a list.
    Equations are randomly generated by num number of terms desired.
    Denominators will always be at end of multiplication chain.
    see example 3

    >>> equation_gen(3)
    [8, '\u2022', 2, '+', 3, '=', 19]
    >>> equation_gen(5)
    [7, '/', 6, '/', 2, '-', 3, '\u2022', 9, '=', '-', 26.42]
    >>> equation_gen(5)
    [2, '+', 6, '\u2022', 2, '\u2022', 3, '/', 7, '=', 30]
    """
    # Version 1.1.0 May 13 2020
    # [C]Liam Ogilvie
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
    total = round(listmas(equation_list)[0], 2)
    if total < 0:
        equation_list.extend(['=', '-', abs(total)])
    else:
        equation_list.extend(['=', abs(total)])
    good_num = False
    while not good_num:
        global x_insert
        x_insert = random.randint(2, len(equation_list)-2)
        if x_insert % 2 == 0:
            good_num = True
    ans = equation_list[x_insert]
    global answer
    answer = str(ans)
    x = equation_list[x_insert]
    if x == "-":
        x = -1
    equation_list[x_insert] = 'x'
    return equation_list

# -=-=-=-=-=-=-=-Debugging-=-=-=-=-=-=-=-#
"Inputs to be able to handle"
# print(listmas(['-4x', '+', '3x']))
# print(listmas(['3x', '+', 4, '\u2022', '2x', '+', 2]))
# print(listmas(['3x', '+', '4x', '-', 3, '\u2022', '6']))
# print(listmas(['3x', '-', '3x']))
# print(listmas(['3', '-', '5']))
# print(listmas([7, '•', 3, '-', 2, '+', 5, '/', 7, '/', 7]))
# print(listmas([8, '-', '9x', '/', 3, '+', 'x', '+', 1]))
# print(listmas([8, '-', 9, '/', 3, '+',2, '+', 1, '/', 7]))
# print(listmas(['106', '-', '2', '/', '2', '+', '3']))

# print(listmas(['2', '+', '6(x)', '-', '2', '•', '7', '•', '4(x)']))
# print(listmas(['2', '•', '8', '/', 'x', '-', '5(3)', '+', '7(3)']))
# print(listmas(['3', '•', 'x', '•', '9(2)', '+', '2', '-', '3(2)']))
# print(listmas(['2', '+', '6(x)', '-', '2', '•', '7', '•', '4(x)']))
# print(listmas(['2', '•', '8', '/', 'x', '/', '3', '-', '5', '+', '7']))
# print(listmas(['2', '•', '8', '/', 'x', '-', '5(3)', '+', '7(3)']))
# print(listmas(['9', '/', '3', '-', '7', '+', '5', '/', 'x', '+', '4']))
