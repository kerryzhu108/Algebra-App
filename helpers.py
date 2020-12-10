from typing import Optional
import pygame
import math
import operator
import random
import calculate


def bond_follow(sprite) -> None:
    """Makes the sprite's bonded number (and the number its bond may be bonded to)
    (and div_line if bonded is a denominator) follow it.
    Precondition: Sprite must have a bonded number in the first place"""
    if sprite.bond and sprite.bond.left_sign == '/' and sprite.bond.bond_follow:
        # if my bond is a denominator
        sprite.bond.rect.x = sprite.rect.x + 1
        if sprite.left_sign != '/':
            # if i am numerator, shift my denominator bond right a but more
            sprite.bond.rect.x += 8
        sprite.bond.rect.y = sprite.rect.y + 50
        sprite.bond.div_line.update_div_line(sprite.bond)
    elif sprite.bond and sprite.bond.left_sign == '\u2022' and sprite.bond.bond_follow:
        # if my bond is a multi
        sprite.bond.rect.x = sprite.rect.x + (len(sprite.number)-1)/3*40 + 45
        sprite.bond.rect.y = sprite.rect.y
    if sprite.bond and sprite.bond.bond and sprite.bond.bond.bond_follow:  # if sprite.bond has bond
        # rerere-recurrrsionn
        bond_follow(sprite.bond)


def bracket_group_move(bracket_numbers: list, init_mouse_pos: list, init_nums_pos: list):
    """Takes a list of bracket_numbers and moves them as a group.
    It does so by by setting every number equal to the current
    mouse pos plus the distance between init_nums_pos and init_mouse_pos
    click position. This keeps every number in the same place as the mouse moves."""
    bracket_numbers.sort(key=operator.attrgetter('rect.x'))
    for num, pos in zip(bracket_numbers, init_nums_pos):
        num.rect.x = pygame.mouse.get_pos()[0] + (pos[0] - init_mouse_pos[0][0])
        num.rect.y = pygame.mouse.get_pos()[1] + (pos[1] - init_mouse_pos[0][1])
        if num.left_sign == '/':  # gets individual div_lines to follow
            num.div_line.update_div_line(num)


def check_bond_relation(num1, num2) -> bool:
    """Helper function for spawn_div_numbers that takes in num1 and num2
    sprite and checks to see if they are related via bonds,
    returns True if it is. ex) 2x9x4/8 the 2 in this case is related
    via continuous bonds, like a linked tree to 8 so it shouldn't be
    multiplied by 8 if 8 crosses the equal sign, same with the 9,4."""
    if num1.bond == num2 or num2.bond == num1:
        return True
    if num1.bond and check_bond_relation(num1.bond, num2):
        return True
    if num2.bond and check_bond_relation(num2.bond, num1):
        return True
    return False


def closest_number(numbers: list, target_sprite) -> 'number sprite':
    """Takes in all numbers and returns the closest number sprite to target_sprite"""
    closet_sprite = None
    closet_distance = 999999
    numbers_copy = numbers[:]
    numbers_copy.remove(target_sprite)
    for num in numbers_copy:
        d_new = math.sqrt(abs(num.rect.x-target_sprite.rect.x)**2 + abs(num.rect.y-target_sprite.rect.y)**2)
        if d_new < closet_distance:
            closet_distance = d_new
            closet_sprite = num
    return closet_sprite


def enable_disable_bond_follow(numbers: 'sprite group') -> None:
    """Enables or disables bond_follow feature when there are only two sprites
    remaining on one side of equal sign."""
    left_numbers = []
    right_numbers = []
    numbers_list = numbers.sprites()
    for number in numbers_list:
        if number.number == '=':
            pass
        elif number.side == 'left':
            left_numbers.append(number)
        else:
            right_numbers.append(number)
        number.bond_follow = True  # to reset others
    to_free = []
    if len(left_numbers) <= 2:
        to_free.extend(left_numbers)
    if len(right_numbers) <= 2:
        to_free.extend(right_numbers)
    for number in to_free:
        number.bond_follow = False
        if number.bond and number.bond.left_sign == '\u2022':
            number.left_sign = '\u2022'  # gets mutli num to behave like multi


def end_pos(numbers: list, opposite_side: Optional[str] = None, dont_count: Optional = None) -> list:
    """Takes in a list of number sprites and uses each element's rect.x to determine
    most left and right TOP number on [optional] opposite_side of equal sign given. Then
    returns these two number instances as elements of a list along with the
    distance between them. Will exclude dont_count sprite from calculation if provided."""
    most_left = 1000000
    most_right = -1
    right_num = None
    left_num = None
    for num in numbers:  # excludes dont_count sprite if given and ANY denominator sprites
        if num.number != '=' and (not opposite_side or num.side != opposite_side) and \
                (not dont_count or num != dont_count) and num.left_sign != '/':
            if num.rect.x > most_right:
                most_right = num.rect.x
                right_num = num
            if num.rect.x < most_left:
                most_left = num.rect.x
                left_num = num
    return [left_num, right_num, most_right-most_left]


def get_bracket_numbers(numbers: list) -> list:
    """returns all the numbers enclosed in multiplication brackets."""
    numbers.sort(key=operator.attrgetter('rect.x'))
    begin = None
    end = None
    include_div_bonds = None
    for index in range(len(numbers)):
        if '(' in numbers[index].left_sign:
            begin = index
        # second or to catch div nums further right of bracket_num
        if ')' in numbers[index].right_sign or \
                not include_div_bonds or check_bond_relation(include_div_bonds, numbers[index]):
            end = index
            include_div_bonds = numbers[index]
    return numbers[begin:end+1]


def get_equation(user_equation: list) -> list:
    """Takes a list that contains information on what equation the user wants.
    Returns random equation of custom length if given ['gen equation', int(length)]
    Returns custom equation if the list is a custom equation.
    Returns a preset equation if user_equation is empty.

    The solution to the x variable will be the second element of the list.
    ex) [8, '/', 'x', '-', 5 '=', 3], 1]
    """

    if user_equation and user_equation[0] == "gen equation":
        return calculate.equation_gen(3)
    elif user_equation:
        return user_equation
    eq_pool = [[[3, '•', 'x', '•', 9, '+', 5, '/', 2, '-', 3, '=', 107], 4],
               [[9, '/', 'x', '+', 6, '+', 2, '•', 7, '•', 4, '=', '-', 49], 3],
               [[2, '•', 8, '/', 'x', '/', 3, '-', 5, '+', 7, '=', 4], 12],
               [[9, '/', 3, '-', 7, '+', 5, '/', 'x', '+', 4, '=', '-', 5], 7],
               [[4, '•', 'x', '•', 6, '•', 7, '-', 3, '-', 9, '=', 492], 19]]
    random_index = random.randint(0, len(eq_pool) - 1)
    return [eq_pool[random_index][0], eq_pool[random_index][1]]


def get_info(history: list, history_index: list, undo_redo: int, numbers: 'sprite group', bracket_nums) -> None:
    """Uses history_index[0] and undo_redo to select right index in history (formatted as):
    [ [[sprite,values],[sprite,values]], [[sprite,values],[sprite,values],[sprite,values]] ]
    to either undo(-1) sprites to the past or redo(1) to the future (if possible).
    Also updates history_index[0] to keep track of index.
    May remove/add sprites to numbers if sprites were spawned.
    Bracket_nums' status also restored.
    """
    if 0 <= history_index[0] + undo_redo < len(history):
        history_index[0] += undo_redo
        history_sprites = []  # for finding which needs to be removed
        print(bracket_nums, 'right before getting info')
        for sprite_info in history[history_index[0]]:
            num = sprite_info[0]
            history_sprites.append(num)
            num.left_sign, num.number, num.right_sign = sprite_info[1], sprite_info[2], sprite_info[3],
            num.side, num.image, num.rect.x = sprite_info[4], sprite_info[5], sprite_info[6]
            num.rect.y, num.bond, num.mouse_mode = sprite_info[7], sprite_info[8], False
            num.group_move, num.bounded = False, sprite_info[9]
            num.update()
            num.div_line.update_div_line(num)
            # restores bracket_nums' status
            bracket_nums.clear()
            bracket_nums.extend(sprite_info[10])
            # restores group div line trigger
            import buttons
            buttons.spawn_special_div_line = sprite_info[11]

        # if going back and a sprite in numbers not in history_sprites, remove it
        for number in numbers.sprites()[:]:
            if number not in history_sprites:
                numbers.remove(number)
                number.div_line.update_div_line(None)
        # if going forwards and a sprite in history_sprites not in numbers, add it
        for number in history_sprites:
            if number not in numbers:
                numbers.add(number)


def get_new_bonds(group: list):
    """Takes sprite group and bonds denominators and right multiplying numbers(RMNs) to their
    left number (if exists) and numerator respectively by setting those number's
    .bonded_to attribute to refer to them. This allows use of the bracket_group_move
    function to make the demon or RMNs follow their bonded number.
    """
    group.sort(key=operator.attrgetter('rect.x'))
    for sprite in group:
        sprite.bond = None  # clears all bonds first !
    for i in range(len(group)):
        if group[i].left_sign == '\u2022':
            group[i-1].bond = group[i]
        elif group[i].left_sign == '/':
            # denominator bond determined by closest number above it
            numbers_above = []
            for number in group:
                if number.rect.y <= group[i].rect.y:
                    numbers_above.append(number)
            closest_number(numbers_above, group[i]).bond = group[i]


def remove_and_give_answer(equal_sign, group: 'sprite group', answer: int):
    """Takes in sprite group, removes all sprites except x
    variable and turns one sprite into answer at equal_sign y value"""
    x_var = None
    turn_into_answer = None
    for sprite in group:
        sprite.div_line.update_div_line(None)
        if 'x' in sprite.number:
            sprite.number = 'x'  # gets rid of anything in front
            sprite.left_sign = ' '
            x_var = sprite
            x_var.rect.y = equal_sign.rect.y
            x_var.update()
        elif sprite.number not in 'x=' and not turn_into_answer:
            turn_into_answer = sprite
        elif sprite.number != '=':
            sprite.left_sign = ' '
            group.remove(sprite)
    if x_var.rect.x < equal_sign.rect.x:
        turn_into_answer.rect.x = equal_sign.rect.x + 60
    else:
        turn_into_answer.rect.x = equal_sign.rect.x - 60
    turn_into_answer.rect.y = equal_sign.rect.y
    turn_into_answer.number = str(answer)
    turn_into_answer.left_sign = ' '
    turn_into_answer.update()


def remove_and_return_equal_sign(group: 'sprite group'):
    """Takes in a list of sprites then removes and returns equal sign sprite"""
    for number in group:
        if number.number == '=':
            group.remove(number)
            return number
    """NOT USED"""


simplifiable = [""]  # can't simplify equation error message


def simplify(numbers: 'sprite group', coordinate: tuple, equal_sign: 'sprite obj'):
    """Gets all the selected numbers between initial select box coordinate
    and current mouse position that are on the same side of equal_sign, simplifies them
    if possible and turns one sprite into the simplified answer."""
    selected = []  # holds numbers
    selected_sprites = []  # holds corresponding sprites
    sprite_list = numbers.sprites()
    sprite_list.sort(key=operator.attrgetter('rect.x'))
    side = 'left'
    if equal_sign.rect.x < coordinate[0]:
        side = 'right'
    for number in sprite_list:
        if coordinate[0]-5 < number.rect.x < pygame.mouse.get_pos()[0] and \
                coordinate[1] < number.rect.y < pygame.mouse.get_pos()[1] and \
                number.side == side:
            if ' ' not in number.left_sign:  # if not left-most number
                selected.append(number.left_sign)
            else:  # if the left-most number
                number.left_sign = '+'
            selected.append(number.number)
            selected_sprites.append(number)
    answer = None
    if selected:
        try:
            simplifiable[0] = ""
            answer = calculate.simplify(selected)
        except (ValueError, TypeError, IndexError):
            simplifiable[0] = "Sorry, encountered unexpected error when trying to simplify"
    # if there are numbers selected and they can be simplified
    if answer:
        # change some of selected sprites into answer
        # delete the rest of selected sprites, update everything once
        i = -1  # direction to iterate from
        for new in reversed(answer):
            if isinstance(new, int) or isinstance(new, float) or 'x' in new:
                selected_sprites[i].number = str(new)
                selected_sprites[i].left_sign = '  '
                # aligns with eq sign in case old sprite was denom
                selected_sprites[i].rect.y = equal_sign.rect.y
                selected_sprites[i].div_line.update_div_line(None)
                # shifts extra to make room for potentially longer number
                selected_sprites[i].rect.x += i/abs(i)*(len(str(new))-1)*9 + 70 * (i+1)
            elif isinstance(new, str):
                selected_sprites[i].left_sign = new
                i += -1
        # removes extra/unchanged sprites
        for left_over_sprites in selected_sprites[:i]:
            left_over_sprites.div_line.update_div_line(None)
            numbers.remove(left_over_sprites)
        numbers.update()


def spawn_numbers(numbers: list, selected_sprite, new_sprites: Optional[list] = None) -> None:
    """Takes in a all number sprites as a list and multiplies/divides
    appropriate numbers by selected_sprite and its bonds after it crosses equal sign.
    Then shifts all number sprites on spawned side to adjust for
    new numbers that appear (if seleced is a denom). Recursion step is to allow numbers
    to shift more when there is more than one denominator ie 7/2x. new_sprites are new dummy sprites
    to be turned into denominators, input list will be mutated to desired length (if selected is a multi).
    """
    numbers.sort(key=operator.attrgetter('rect.x'))
    got_multiplied = []
    for numb in numbers:
        # checks if number is bonded to denom sprite
        if numb.side == selected_sprite.side and numb != selected_sprite \
                and not check_bond_relation(selected_sprite, numb) and numb.number != '=':
            # not numb.bond forces div to apply to last num in bond
            # last bracket condition makes multi num spawn at last multi bond in chain
            if (selected_sprite.left_sign == '\u2022' and not numb.bond) or \
                    (selected_sprite.left_sign == '/' and (not numb.bond or numb.bond.left_sign == '/')):
                # checks if number is bonded to a number who already got multiplied
                if not got_multiplied or not check_bond_relation(got_multiplied[-1], numb):
                    got_multiplied.append(numb)
                    # what to do if selected sprite is denominator
                    if selected_sprite.left_sign == '/':
                        multiplied = selected_sprite.number
                        if selected_sprite.bond and selected_sprite.bond.left_sign == '/':
                            multiplied += selected_sprite.bond.number
                        numb.number += '(' + multiplied + ')'
        # adjustment/ shifting numbers to make room
    shift_direction = 1
    ith_num_from_eq = 0
    # ith_num_from_eq for shifting if selected is denominator or
    # for selecting/slicing new_sprites to desired len
    if selected_sprite.side == 'left':
        shift_direction = -1
        # flips list order to ensure always starts from center of eq sign
        numbers.reverse()
    for numb in numbers:
        if selected_sprite.left_sign == '/':
            # what to do if selected sprite is denominator part 2
            if numb.side == selected_sprite.side and not numb.mouse_mode\
                    and numb in got_multiplied:
                # nums that get multiplied are shifted by (gap)(direction)(ith # from eq)
                ith_num_from_eq += 1
                numb.rect.x += 35 * shift_direction * ith_num_from_eq
                # this makes first number not shift if they're right side numbers
                if shift_direction == 1 and ith_num_from_eq == 1:
                    numb.rect.x -= 35 * shift_direction * ith_num_from_eq
            elif numb.side == selected_sprite.side and not numb.mouse_mode\
                    and numb not in got_multiplied:
                # nums not multiplied are shifted the same as previous number
                numb.rect.x += 35 * shift_direction * ith_num_from_eq
        elif selected_sprite.left_sign == '\u2022':
            # what to do if selected is multiplication
            if numb.side == selected_sprite.side and not numb.mouse_mode \
                    and numb in got_multiplied and new_sprites:
                # turn each of em into denom sprites
                new_sprites[ith_num_from_eq].left_sign = '/'
                new_sprites[ith_num_from_eq].rect.x = numb.rect.x + 5
                new_sprites[ith_num_from_eq].rect.y = numb.rect.y + 50
                new_sprites[ith_num_from_eq].side = numb.side
                new_sprites[ith_num_from_eq].newly_spawned = True  # for future tracking
                ith_num_from_eq += 1
    if new_sprites:
        # gets rid of all unused new_sprites
        # the 10 must correspond to the value in nums
        for i in range(10-ith_num_from_eq):
            new_sprites.pop()
    if selected_sprite.bond:
        spawn_numbers(numbers, selected_sprite.bond)


def store_info(numbers: 'sprite group', bracket_nums, history: list, history_index: list,
               spawn_group_div: bool) -> None:
    """Takes numbers sprite group and stores each sprite's info
    into history in the form of: (3 sprites in second element to show new sprite spawning)
    [ [[sprite,values],[sprite,values]], [[sprite,values],[sprite,values],[sprite,values]] ]
    then updates history_index[0] for tracking. Bracket_num's status also stored each time"""
    chapter = []
    for num in numbers.sprites():
        chapter.append([num, num.left_sign, num.number, num.right_sign, num.side, num.image,
                        num.rect.x, num.rect.y, num.bond, num.bounded, bracket_nums[:], spawn_group_div])
    history_index[0] += 1
    # cuts future if redo and then new move
    temp_history = history[:history_index[0]]
    temp_history.append(chapter)
    history.clear()
    history.extend(temp_history)


def update_side(sprite) -> None:
    """Takes in sprite and updates its side attributes along
     with its bonds recursively."""
    if sprite.side == 'left':
        sprite.side = 'right'
    else:
        sprite.side = 'left'
    if sprite.bond and sprite.bond_follow:  # if not bond_follow,
        # then don't want to update its bond's side because it is not following it
        update_side(sprite.bond)


"""Colors"""
black = (0, 0, 0)
grey = (48, 48, 48)
light_grey = (131, 139, 139)
white = (255, 255, 255)
