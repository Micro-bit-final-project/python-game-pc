import pygame, utils, sys, time
from random import shuffle

# Global variables
X = 0
Y = 0
background = 0

def end_anim(screen, win):
    """
    This function handles the final animation of a game.
    - screen: pygame.display to draw to.
    - win: Whether or not the user won. Play a sound and
           display an image accordingly.
    """
    global X
    global Y
    global background

    if win:
        img = pygame.image.load("match_files" + utils.sep + "win.png").convert_alpha()
    else:
        img = pygame.image.load("match_files" + utils.sep + "lose.png").convert_alpha()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    img_rect = img.get_rect()
    img_rect.center = (utils.width / 2, utils.height/2)
    screen.blit(img, img_rect)

    # Sound
    if win:
        pygame.mixer.Sound.play(utils.win_sound)
    else:
        pygame.mixer.Sound.play(utils.lose_sound)

    # Info
    utils.draw_points(screen)
    utils.draw_time(screen, utils.time_remaining)

    pygame.display.flip()
    pygame.time.wait(3000)
    return

def directions(screen, potions_list, buttons_list, get_data):
    """
    Provides the user with the initial shuffling code.
    - screen: The pygame.display to load into
    - potions_list: List of pygame Surfaces
    - buttons_list: List of the buttons related to the items in potions_list
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global X
    global Y

    buttons = buttons_list.copy()
    for i in range(0, len(buttons)):
        if buttons[i] == 1:
            buttons[i] = "U"
        elif buttons[i] == 2:
            buttons[i] = "L"
        elif buttons[i] == 3:
            buttons[i] = "D"
        elif buttons[i] == 4:
            buttons[i] = "R"
    screen.fill((0, 0, 0))
    # Adjusted coordinates for better display of the sprites
    rect0 = potions_list[0].get_rect()
    rect0.center = (X / 4, Y)
    rect1 = potions_list[1].get_rect()
    rect1.center = (X / 2, Y)
    rect2 = potions_list[2].get_rect()
    rect2.center = (X - (X / 4), Y)
    screen.blit(potions_list[0], rect0)
    screen.blit(potions_list[1], rect1) 
    screen.blit(potions_list[2], rect2)
    # Show which is which
    utils.draw_text(screen, buttons[0], X / 4, Y + 300)
    utils.draw_text(screen, buttons[1], X / 2, Y + 300)
    utils.draw_text(screen, buttons[2], X - (X / 4), Y + 300)
    pygame.display.flip()
    utils.run_in_thread(get_data) # Clean the buffer before the game starts
    pygame.time.wait(2000)
    utils.run_in_thread(get_data) # Clean the buffer before the game starts
    return

def blit_all(screen, potions_list, index):
    """
    This function loads essential game elements on the screen.
    - screen: The pygame.display to load into
    - potions_list: List of pygame Surfaces
    - index: Game variable used to track progreess
    """
    global X
    global Y
    global background

    screen.blit(background, (0, 0))
    if index == 2:
        rect = potions_list[2].get_rect()
        rect.center = (X / 2, Y)
        screen.blit(potions_list[2], rect)
    elif index == 1:
        # Adjusted coordinates for better display of the sprites
        rect1 = potions_list[1].get_rect()
        rect1.center = (X / 3, Y)
        rect2 = potions_list[2].get_rect()
        rect2.center = (X - (X / 3), Y)
        screen.blit(potions_list[1], rect1) 
        screen.blit(potions_list[2], rect2)
    else:
        # Adjusted coordinates for better display of the sprites
        rect0 = potions_list[0].get_rect()
        rect0.center = (X / 4, Y)
        rect1 = potions_list[1].get_rect()
        rect1.center = (X / 2, Y)
        rect2 = potions_list[2].get_rect()
        rect2.center = (X - (X / 4), Y)
        screen.blit(potions_list[0], rect0)
        screen.blit(potions_list[1], rect1) 
        screen.blit(potions_list[2], rect2)
    return

def shuffle_lists(potions_list, buttons_list):
    """
    This function shuffle two related lists by
    shuffling the indices.
    - potions_list: function 1
    - buttons_list: function 2
    From https://stackoverflow.com/a/11765138
    """
    index_shuf = list(range(len(potions_list)))
    shuffle(index_shuf)
    potions_new_list = []
    buttons_new_list = []
    for i in index_shuf:
        potions_new_list.append(potions_list[i])
        buttons_new_list.append(buttons_list[i])
    return potions_new_list, buttons_new_list

def match_game(screen, get_data):
    """
    This function handles the match minigame.
    - screen: pygame.display to draw to.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global X
    global Y
    global background

    # Initialise here the points variables
    points = 0

    # Load drinks sprite:
    red_sprite = pygame.image.load("match_files" + utils.sep + "red.png").convert_alpha()
    green_sprite = pygame.image.load("match_files" + utils.sep + "green.png").convert_alpha()
    blue_sprite = pygame.image.load("match_files" + utils.sep + "blue.png").convert_alpha()

    # Drink sprites' coordinates
    X = utils.width
    Y = utils.height / 2

    # Load backgound image
    background = pygame.image.load("match_files" + utils.sep + "background.png").convert_alpha()

    # Game
    pygame.mixer.music.load("match_files" + utils.sep + "music.ogg")
    
    seconds_counter = time.time()
    generated = False
    potions_list = [red_sprite, green_sprite, blue_sprite]
    shuffle(potions_list) # Shuffle list
    buttons_list_tmp = [1, 2, 3, 4]
    shuffle(buttons_list_tmp) # Shuffle list
    buttons_list = []
    for i in range(0, 3):
        buttons_list.append(buttons_list_tmp[i]) # make buttons and potions list same length

    index = 0
    button_press = 0
    colour = (255, 250, 0)
    utils.text_colour = colour
    utils.text_colour = (255, 255, 255) # Set the text colour for the minigame

    directions(screen, potions_list, buttons_list, get_data)

    utils.text_colour = colour
    pygame.mixer.music.play(-1) # Game can last more than 27 seconds
    while True:
        # Game logic
        if points == 12: # winning condition
            pygame.mixer.music.stop()
            end_anim(screen, True)
            utils.time_remaining = 0 # Make sure the game stops

        if time.time() - seconds_counter > 1:
            utils.time_remaining -= 1
            seconds_counter = time.time()

        if utils.time_remaining > 0:
            utils.run_in_thread(get_data)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0, 0, 0))

            if index == 3:
                index = 0
                generated = False

            if generated == False:
                potions_list, buttons_list = shuffle_lists(potions_list, buttons_list)
                generated = True

            # Make sure button presses are not duplicated
            if utils.data[0] != button_press:
                button_press = utils.data[0]
            else:
                button_press = 0

            if button_press == buttons_list[index]:
                blit_all(screen, potions_list, index)

                index += 1
                points += 1
                utils.points += 1
                counter = 0
                utils.text_colour = (9, 140, 0)
                utils.draw_text(screen, "Rigth!", X / 2, Y / 2)
                pygame.display.flip()
                pygame.time.wait(1200)
                utils.text_colour = colour
                utils.time_remaining += 3
                utils.data[0] = 0
            elif button_press != 0:
                blit_all(screen, potions_list, index)

                utils.text_colour = (0, 4, 198)
                utils.draw_text(screen, "Wrong!", X / 2, Y / 2)
                pygame.display.flip()
                pygame.time.wait(1200)
                utils.text_colour = colour
                utils.time_remaining -= 7
                utils.data[0] = 0

            blit_all(screen, potions_list, index)

            # Info
            #utils.draw_text(screen, "Directions", utils.width / 2, 322)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)

            pygame.display.flip()
            utils.clock.tick(60)
        else:
            pygame.mixer.music.stop()
            if points < 12: # If true, the user lost
                end_anim(screen, False)

            utils.minigame_end(screen)

            while True:
                get_data()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if type(utils.data[0]) == float and utils.data[0] != 0:
                    break
            break
    return