import pygame
import operator
import helpers
from typing import Optional

pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
grey = (48, 48, 48)
light_grey = (131, 139, 139)
font = pygame.font.Font('freesansbold.ttf', 32)


class Buttons(pygame.sprite.Sprite):
    """Handles division lines, highlight box, and other
    miscellaneous features."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((0, 0))  # loads image
        self.rect = self.image.get_rect()  # allows it to be drawn
        self.rect.x = 0
        self.rect.y = 0
        self.init_pos = (-1, -1)  # for highlight box

    def update_div_line(self, following, numbers: Optional[list] = None):
        """Updates div_line length and position with reference
        to either a group of numbers it is following or just a single number.
        Length is extended if following is dividing a lot, length determined by numbers."""
        if isinstance(following, list):
            # div_line for groups
            line_len = helpers.end_pos(following)[2] + len(following[-1].number) * 23
            self.image = pygame.Surface((line_len, 4))
            self.image.fill(white)
            following.sort(key=operator.attrgetter('rect.x'))
            self.rect.x = following[0].rect.x - 5
            self.rect.y = following[0].rect.y - 10
        elif not following or following.left_sign != '/':
            # if following is False, hide div line
            self.image = pygame.Surface((0, 0))
        elif following.left_sign == '/':
            # div line for just one denominator
            line_len = 40
            if not following.bounded and numbers:  # stretch line_len if multi turning to div
                opposite_side = 'left'
                if following.side == 'left':
                    opposite_side = 'right'
                line_len += helpers.end_pos(numbers, opposite_side, following)[2]
            line_shift = line_len/2-10
            self.image = pygame.Surface((line_len, 4))
            self.rect.x = following.rect.x - line_shift
            self.rect.y = following.rect.y - 10
            self.image.fill(white)

    def update_box(self, screen):
        """ Uses init_pos to draw a dynamic rectangle box on screen.
        Only does so when init_pos is assigned a real value."""
        if self.init_pos != (-1, -1):
            wid = pygame.mouse.get_pos()[0] - self.init_pos[0]
            length = pygame.mouse.get_pos()[1] - self.init_pos[1]
            pygame.draw.rect(screen, green, [self.init_pos[0], self.init_pos[1], wid, length], 1)
        else:
            self.image = pygame.Surface((0, 0))

        if next_click_select:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, green, [mouse_pos[0], mouse_pos[1], 15, 10], 1)


buttons_group = pygame.sprite.Group()  # buttons sprite group

answer = Buttons()  # simplifies by combining all numbers at very end
answer.image = pygame.image.load('images/answer.png')
answer.rect.x = 0

select = Buttons()
select.image = pygame.image.load('images/simplify.png')
select.rect.x = 200

select_box = Buttons()  # highlight box
select_box.image = pygame.Surface((0, 0))
# Trigger for spawning select/simplify box
next_click_select = False
next_click_simplify = False
select_box_signal = Buttons()  # picture of select box that appears next to mouse

buttons_group.add(select_box_signal, select_box, select, answer)  # adds everything to buttons group

# Trigger for spawning div_line on top of brackets
spawn_special_div_line = False
