import pygame
import helpers
import buttons
import menu
import settings
from settings import number_font as font
from typing import Union


class Player(pygame.sprite.Sprite):  # properties of the numbers
    """ Numbers, operators and their properties """
    position_x = 200  # initial position of first number sprite
    position_y = 300

    def __init__(self, numb: Union[float, str]):
        """Constructs number and assigns it various qualities"""
        pygame.sprite.Sprite.__init__(self)
        self.number = str(numb)
        self.left_sign = ' '
        self.right_sign = ' '
        self.side = None
        self.image = font.render(self.left_sign + ' ' + self.number, True, settings.grey, settings.white)
        self.rect = self.image.get_rect()
        self.rect.x = Player.position_x + 50
        self.rect.y = Player.position_y
        self.mouse_mode = False  # toggles selected number to follow mouse
        self.group_move = False  # toggles group of bracketed numbers to follow mouse
        self.bond = None  # used for denominator or RMN to follow it
        self.div_line = buttons.Buttons()  # spawns div line above number
        self.bounded = True  # when false, div_line length will stretch to cover all nums
        buttons.buttons_group.add(self.div_line)  # allows div lines to be drawn
        self.newly_spawned = False  # keeps track if this num spawned after initialization
        self.bond_follow = True  # allows self to follow its bond
        self.history = []  # keeps track of numbers info as tuple:
        # (left_sign, right_sign, side, image, rect.x, rect.y, mouse_mode, group_move, bond)
        self.history_index = -1  # keeps track of where undo/redo is at
        Player.position_x += 45 + 12 * len(self.number)  # spacing

    def update(self):
        """Updates sprite instance variables"""
        if self.mouse_mode:
            self.rect.x = pygame.mouse.get_pos()[0]
            self.rect.y = pygame.mouse.get_pos()[1]
            if self.bond and self.bond_follow:
                # gets bonded denom/RMN to follow it if self.bond_follow is active
                helpers.bond_follow(self)
        if self.group_move:
            # moves everything inside brackets
            helpers.bracket_group_move(bracket_nums, init_mouse_pos, init_nums_pos)
        if self.left_sign != '/':
            # renders number and left sign except for div sign
            img_and_sign = self.left_sign + ' ' + self.number
            self.image = font.render(img_and_sign, True, settings.white, settings.light_grey)
        elif self.left_sign == '/':
            # renders custom division line above division
            if self.bounded:
                self.div_line.update_div_line(self)
            else:
                self.div_line.update_div_line(self, numbers.sprites())
            self.image = font.render(' ' + self.number, True, settings.white, settings.light_grey)
            """if self in bracket_nums and self.left_sign != '/': # USELESS???
                self.div_line.update_div_line(bracket_nums)"""

        # activates div_line for groups via special trigger
        # second and catches case when this statement deactivates div_lin for reg denominator sprites
        if self in bracket_nums and buttons.spawn_special_div_line and self.left_sign != '/':
            self.div_line.update_div_line(bracket_nums)
        elif self in bracket_nums and not buttons.spawn_special_div_line and self.left_sign != '/':
            self.div_line.update_div_line(None)

    def event_handler(self):
        """Handles attribute changes when the number crosses equal sign"""
        # event handler for +/-
        if self not in bracket_nums:
            if self.left_sign in '-':
                self.left_sign = '+'
            elif self.left_sign in '+ ':
                self.left_sign = '-'
        # event handler for brackets ()
        if self in bracket_nums:
            # allow special div line to spawn on top of group via trigger
            if not buttons.spawn_special_div_line:
                buttons.spawn_special_div_line = True
            else:
                buttons.spawn_special_div_line = False

        # event handler for division /
        if self.left_sign == '/':
            # if multiplication number comes back, despawn everything
            if self in causer_sprite:
                self.left_sign = '\u2022'
                self.div_line.update_div_line(None)
                causer_sprite.remove(self)
                for sprite in new_div_sprites:
                    sprite.div_line.update_div_line(None)
                    numbers.remove(sprite)
                    numbers.remove(sprite)
            else:
                end_nums = helpers.end_pos(numbers.sprites(), self.side)
                end_nums[0].left_sign = '(' + end_nums[0].left_sign
                end_nums[1].number += ')'
                end_nums[1].right_sign = ')'
                helpers.spawn_numbers(numbers.sprites(), self)
                self.left_sign = ' '
                self.div_line.update_div_line(None)
                # adds all numbers inside brackets into sprite group
                bracket_nums.clear()
                for number in helpers.get_bracket_numbers(numbers.sprites()):
                    bracket_nums.append(number)
                numbers.update()  # updates everything to refresh
        # event handler for multiplication \u2022
        elif self.left_sign == '\u2022':
            # creates 10 new sprites for spawn_numbers to use
            # if change 10, gotta also change 10 in spawn_numbers
            for i in range(10):
                new_div_sprites.append(Player(self.number))
            helpers.spawn_numbers(numbers.sprites(), self, new_div_sprites)
            for new_sprite in new_div_sprites:
                numbers.add(new_sprite)
                new_sprite.update()
            causer_sprite.append(self)  # records self in case it comes back across
            self.left_sign = '/'  # allows div line to render
            self.bounded = False  # allows div_lin length to stretch

        # updates side attribute, always have at bottom
        helpers.update_side(self)


eq_set = helpers.get_equation(menu.equation)  # generates equation or gets one from user
equation = eq_set[0]
answer = eq_set[1]


numbers = pygame.sprite.Group()  # numbers sprite group for updating/drawing
equal_sign = None
reached_eq_sign = False  # flag for assigning side attribute
for index in range(len(equation)):
    if not isinstance(equation[index], str) or equation[index] in 'x=':
        # second or allows equal sign and x to spawn for spacing
        num = Player(equation[index])
        numbers.add(num)
        try:
            # adds left and right signs of num
            if isinstance(equation[index-1], str) and equation[index-1] not in 'x=':
                num.left_sign = equation[index-1]
                # allows sign left of number to render as part of it
                num.image = font.render(num.left_sign + num.number, True, settings.black, settings.white)
            if isinstance(equation[index+1], str) and equation[index+1] not in 'x=':
                num.right_sign = equation[index+1]

            if equation[index] == 'x' and num.left_sign != '/':
                num.rect.y += -1

            if num.left_sign == '/':
                # moves denominators down on initialization and shifts others to account
                num.rect.y += 50
                num.rect.x = numbers.sprites()[-2].rect.x
                # so next num doesn't spawn extra far right
                Player.position_x -= 45 + 12 * len(num.number)
                Player.position_y += 50  # so subsequent div is even further down
            if num.left_sign != '/':  # resets y pos if subsequent num is not div
                Player.position_y = 300
                num.rect.y = 300

            if num.number == '=':
                equal_sign = num

        except IndexError:
            pass
        # adds side attribute to each number
        if equation[index] == '=':
            reached_eq_sign = True
        if not reached_eq_sign:
            num.side = 'left'
        else:
            num.side = 'right'

past_position = -1  # keeps track of selected sprite's position
present_position = -1

new_div_sprites = []  # stores all newly spawned sprites from moving multiplication too early
causer_sprite = []  # stores the sprite that caused the new_div_sprites to spawn

bracket_nums = []  # list of numbers in brackets
init_mouse_pos = []  # these two stores initial mouse and numbers positions for group move
init_nums_pos = []

numbers.update()  # updates all sprite groups after initialization to render images
# especially div line
helpers.get_new_bonds(numbers.sprites())  # sets bonds for denom and RMN after initialization
for numbe in numbers.sprites():
    # adjusts positioning of multiple denominators on initialization
    helpers.bond_follow(numbe)

history = []  # stores every sprite's info in the form of
# [ [[sprite,values],[sprite,values]], [[sprite,values],[sprite,values],[sprite,values]] ]
history_index = [-1]

helpers.store_info(numbers, bracket_nums, history, history_index, False)
# stores all sprites' info into their history for undo/redo on initialization
