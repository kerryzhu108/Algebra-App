import buttons
import helpers
import importlib
import nums
import pygame
import settings

"""Keeps track of selected number"""
past = nums.past_position
present = nums.present_position
selected = nums.numbers.sprites()[0]

"""Application's main loop"""

running = True
while running:  # main game loop
    for event in pygame.event.get():
        past = present
        present = selected.rect.x
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                helpers.get_info(nums.history, nums.history_index, -1, nums.numbers, nums.bracket_nums)
            elif event.key == pygame.K_r:
                helpers.get_info(nums.history, nums.history_index, 1, nums.numbers, nums.bracket_nums)
            elif event.key == pygame.K_ESCAPE:
                # return to main menu from game
                nums.menu.menu(settings.width, settings.height, settings.grey)
                importlib.reload(buttons)
                importlib.reload(nums)

            # resents past/present tracker so it wont mistakenly think number
            # crossed equal sign bc past referred to position on other side
            past = selected.rect.x - 1
            present = selected.rect.x

        if event.type == pygame.MOUSEBUTTONDOWN:
            # toggles select/simplify box after 'select' button is clicked,
            # does so via assigning select_box a real init_pos
            if buttons.next_click_select:
                # also resets button image
                buttons.select.image = pygame.image.load('images\simplify.png')
                buttons.select_box.init_pos = pygame.mouse.get_pos()
                buttons.next_click_select = False
                buttons.next_click_simplify = True
            elif buttons.next_click_simplify:
                helpers.simplify(nums.numbers, buttons.select_box.init_pos, nums.equal_sign)
                # updates error message
                simplifiable = settings.font.render(helpers.simplifiable[0], True, settings.white, settings.grey)
                buttons.select_box.init_pos = (-1, -1)
                buttons.next_click_simplify = False

            for num in nums.numbers:
                if num.mouse_mode or num.group_move:
                    helpers.get_new_bonds(nums.numbers.sprites())
                    # if dropping a number, redetermine bonds
                    # for denoms and right multiplying nums\
                    helpers.store_info(nums.numbers, nums.bracket_nums, nums.history,
                                       nums.history_index, buttons.spawn_special_div_line)
                    # stores all sprites' info into their history for undo/redo

                    num.mouse_mode = False
                    num.group_move = False
                    # allows sprites to be dropped

                elif num.rect.x-10 < pygame.mouse.get_pos()[0] < num.rect.x+40 \
                        and num.rect.y-1 < pygame.mouse.get_pos()[1] < num.rect.y+40:
                    num.mouse_mode = True
                    selected = num

                    # disables bond follow if only two numbers left on side
                    helpers.enable_disable_bond_follow(nums.numbers)
                    # resents past/present tracker so it wont mistakenly think number
                    # crossed equal sign bc past referred to position on other side
                    present = pygame.mouse.get_pos()[0]
                    past = present-1

                    if selected in nums.bracket_nums:
                        # if clicked on a number inside bracket_group, whole group is selected
                        selected.group_move = True
                        selected.mouse_mode = False  # disabled so clicked number wont be moved
                        nums.init_mouse_pos = [pygame.mouse.get_pos()]
                        nums.init_nums_pos = []
                        for number in nums.bracket_nums:
                            nums.init_nums_pos.append((number.rect.x, number.rect.y))

            for button in buttons.buttons_group:
                # if click on any button
                if button.rect.x - 10 < pygame.mouse.get_pos()[0] < button.rect.x + 110 \
                        and button.rect.y < pygame.mouse.get_pos()[1] < button.rect.y + 40:
                    if button == buttons.answer:  # if click on answer button, remove all number sprites
                        helpers.store_info(nums.numbers, nums.bracket_nums, nums.history,
                                           nums.history_index, buttons.spawn_special_div_line)
                        helpers.remove_and_give_answer(nums.equal_sign, nums.numbers, nums.answer)
                        buttons.spawn_special_div_line = False
                    if button == buttons.select:
                        # if click on select, select box will appear next click
                        buttons.next_click_select = True
                        button.image = pygame.image.load('images/s_simplify.png')

        if past < nums.equal_sign.rect.x <= present or present <= nums.equal_sign.rect.x < past:
            # when number crosses equal sign
            selected.event_handler()
    # draw
    screen = settings.screen
    screen.fill(settings.grey)  # background colour
    selected.update()  # updates selected sprite
    buttons.select_box.update_box(screen)  # updates highlight box
    nums.numbers.draw(screen)  # draws all the players
    buttons.buttons_group.draw(screen)

    """On screen messages"""
    font = settings.font
    return_menu_msg = font.render('Press ESC to return to main menu', True, settings.light_grey, settings.grey)
    undo_instr = font.render('Press Z to undo R to redo', True, settings.light_grey, settings.grey)
    simplifiable = font.render(helpers.simplifiable[0], True, settings.light_grey, settings.grey)

    screen.blit(return_menu_msg, (670, 20))  # draws return to menu text
    screen.blit(undo_instr, (670, 40))  # draws undo redo text
    screen.blit(simplifiable, (400, 70))  # shows text if cannot simplify
    pygame.display.flip()  # have this last to show colour
