import pygame
import sys


def menu(width: int, height: int, colour: tuple) -> None:
    """Menu screen at start of game. Takes in width and height
    for window screen and color for background color"""
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.Font('freesansbold.ttf', 32)
    sm_font = pygame.font.Font('freesansbold.ttf', 16)
    light_grey = (169, 169, 169)
    dark_grey = (131, 139, 139)
    white = (255, 255, 255)
    menu_backgrounds = [[pygame.Surface((350, 70)).get_rect(y=100, x=300), light_grey],
                        [pygame.Surface((350, 70)).get_rect(y=250, x=300), light_grey],
                        [pygame.Surface((350, 70)).get_rect(y=400, x=300), light_grey],
                        [pygame.Surface((215, 40)).get_rect(y=130, x=660), light_grey]]
    button_colours = [light_grey, light_grey, light_grey, light_grey]

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # if click on random equation
                if menu_backgrounds[0][1] == dark_grey:
                    in_menu = False
                # if click on custom equation
                elif menu_backgrounds[1][1] == dark_grey:
                    if enter_custom_equation(width, height, colour):
                        in_menu = False
                # if click on instructions
                elif menu_backgrounds[2][1] == dark_grey:
                    enter_instructions(width, height, colour)
                # if click on Custom Length
                elif menu_backgrounds[3][1] == dark_grey:
                    if random_equation_length(width, height, colour):
                        in_menu = False

            # for hovering colour change
            for index in range(len(menu_backgrounds)):
                # if menu_backgrounds[index][0] rect box was in mouse position
                if menu_backgrounds[index][0].collidepoint(pygame.mouse.get_pos()):
                    # changes rect box colour and text background colour
                    menu_backgrounds[index][1] = dark_grey
                    button_colours[index] = dark_grey
                else:
                    menu_backgrounds[index][1] = light_grey
                    button_colours[index] = light_grey

        # have this in while but before rending anything so background refreshes when switching menu
        screen.fill(colour)
        for background in menu_backgrounds:
            pygame.draw.rect(screen, background[1], background[0])

        rand_eq = font.render('Random Equation', True, white, button_colours[0])
        custom_eq = font.render('Custom Equation', True, white, button_colours[1])
        instructions = font.render('Instructions', True, white, button_colours[2])
        really_rand_eq = sm_font.render('Custom Length (buggy)', True, white, button_colours[3])
        screen.blit(rand_eq, pygame.Surface((0, 0)).get_rect(center=(327, 119)))
        screen.blit(custom_eq, pygame.Surface((0, 0)).get_rect(center=(327, 269)))
        screen.blit(instructions, pygame.Surface((0, 0)).get_rect(center=(370, 419)))
        screen.blit(really_rand_eq, pygame.Surface((0, 0)).get_rect(center=(675, 143)))
        pygame.display.flip()


equation = []  # possible custom equation to display


def enter_custom_equation(width: int, height: int, colour: tuple) -> bool:
    """Custom equation screen for user to enter custom equation
    at start of menu. Returns true if successful custom equation entered.
    Returns false if esc button pressed."""
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont('cambria', 20)
    dark_grey = (131, 139, 139)
    white = (255, 255, 255)
    return_menu = font.render('Press ESC to return to main menu', True, white, colour)
    instr = ["-Type Custom Equation", "-Use  + - / *  to represent operators",
             "-Need at lease one x variable and equal sign ( = )", "Ex: 2+5x/3+2*4=5/2"]
    bad_input = ''  # error message for bad input
    text_pos = [80, 110, 140, 195]

    equation_box = pygame.Rect(150, 250, 400, 50)
    text = ''

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    equation.clear()
                    return False
                # tries to initialize custom equation
                if event.key == pygame.K_RETURN:
                    all_inputs_valid = True
                    for ch in text:
                        if ch not in '123456789x+-/*=':
                            text = ''
                            bad_input = 'Error: invalid input in equation'
                            all_inputs_valid = False
                    if all_inputs_valid:  # if all good, turn text eq into formatted equation
                        number = ''  #
                        for ch in text:
                            if ch.isdigit():
                                number += ch
                            elif number:
                                equation.append(int(number))
                                number = ''
                                if ch == '*':
                                    equation.append('\u2022')
                                elif ch == 'x':
                                    equation.append('\u2022')
                                    equation.append('x')
                                else:
                                    equation.append(ch)
                            else:  # to get last number
                                equation.append(ch)
                        if number and '=' in equation and 'x' in equation:
                            equation.append(int(number))
                            return True  # if all valid, modify equation and exist this
                        elif '=' not in equation or 'x' not in equation:
                            bad_input = 'Please have at least one x and equal sign in equation.'
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill(colour)
        for i in range(len(instr)):
            screen.blit(font.render(instr[i], True, white, colour), pygame.Rect(150, text_pos[i], 680, 50))
        pygame.draw.rect(screen, dark_grey, equation_box)  # draws background box
        eq = font.render(text, True, white, dark_grey)
        screen.blit(eq, (210, 261))  # then draws equation on top
        error_message = font.render(bad_input, True, white, colour)
        screen.blit(error_message, (150, 400))  # then draws equation on top
        screen.blit(return_menu, (670, 20))  # draws return to menu text
        pygame.display.flip()


def enter_instructions(width: int, height: int, colour: tuple) -> None:
    """Instruction menu explaining how application is used."""
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont('cambria', 20)
    white = (255, 255, 255)
    return_menu = font.render('Press ESC to return to main menu', True, white, colour)
    instr = []
    text_pos = [120]  # y coord of first line of text
    with open('in_game_instr.txt', 'r') as instructions:
        for line in instructions:
            instr.append(line.strip())
            text_pos.append(text_pos[-1]+30)
    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_menu = False

        screen.fill(colour)
        for i in range(len(instr)):
            screen.blit(font.render(instr[i], True, white, colour), pygame.Rect(80, text_pos[i], 680, 100))
        screen.blit(return_menu, (670, 20))  # draws return to menu text
        pygame.display.flip()


def random_equation_length(width: int, height: int, colour: tuple) -> bool:
    """Screen getting user to enter random equation of length 3-9. If valid
    length, returns True, if user wants to return to menu, return False."""
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont('cambria', 20)
    white = (255, 255, 255)
    return_menu = font.render('Press ESC to return to main menu', True, white, colour)
    message = "How long would you like the random equation to be? Press a number between 3-9"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                length = event.unicode
                if length.isdigit() and 3 <= int(length) <= 9:
                    equation.clear()
                    equation.extend(['generate equation', int(length)])
                    return True
                elif event.key == pygame.K_ESCAPE:

                    return False
            elif event.type == pygame.QUIT:
                sys.exit()

        screen.fill(colour)
        screen.blit(font.render(message, True, white, colour), pygame.Rect(80, 200, 680, 100))
        screen.blit(return_menu, (670, 20))  # draws return to menu text
        pygame.display.flip()


# allows menu to be entered upon initialization
window_width = 1000
window_height = 600
background_colour = (48, 48, 48)
menu(window_width, window_height, background_colour)
