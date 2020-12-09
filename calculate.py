import requests
import urllib.parse
import sympy


def simplify(equation: list)-> list:
    """Takes in an equation in the form of a list
    such as:
    [2, '+', 6, '\u2022', 3, '\u2022', 7, '/', 2, '=', 30]
    and returns the simplified version in the same format.
    """
    left_of_eq = ""
    right_of_eq = ""
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
    for element in simplified:
        if element.isnumeric():
            simplified_list.append(int(float(element)))
        elif element == '*':
            simplified_list.append('\u2022')
        else:
            simplified_list.append(element)
    return simplified_list

print(simplify([2, '+', 6, '\u2022', 3, '\u2022', 7, '/', 2, '=', 30]))


#left_eq = urllib.parse.urlencode({"expr": "1+2(3x)"})
#simplified = str(requests.get("http://api.mathjs.org/v4/?"+left_eq).json())
