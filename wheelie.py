import pygame, wheelie_files.bike, utils, sys, time
from random import randint

bgX = 0 # Start of the screen

angle = 0
angle_opponent = randint(0, 70)
background = 0

def scroll_background(background, screen):
    """
    This function handles the infinite background
    scrolling.
    - background: pygame.image backgound image
    - screen: pygame.display to draw to
    """
    global bgX
    # Infinite scroll by attaching 2 background images
    # and resetting their position once one of them
    # is completely out of the screen.
    # Based off https://www.youtube.com/watch?v=US3HSusUBeI
    rel_x = bgX % background.get_rect().width
    mx = rel_x - background.get_rect().width
    screen.blit(background, (mx, 0))
    if rel_x < utils.width:
        screen.blit(background, (rel_x, 0))
    bgX -= 5


def end_anim(screen, win):
    """
    This function handles the final animation of the wheelie minigame.
    - screen: pygame.display to draw to.
    - win: Whether or not the user won. Play a sound and
           display an image accordingly.
    """
    global X
    global Y
    global background

    if win:
        img = pygame.image.load("wheelie_files" + utils.sep + "win.png").convert_alpha()
    else:
        img = pygame.image.load("wheelie_files" + utils.sep + "lose.png").convert_alpha()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    img_rect = img.get_rect()
    img_rect.center = (utils.width / 2, utils.height/2)
    screen.blit(img, img_rect)

    # Sound
    if win:
        pygame.mixer.Sound.play(utils.win_sound).set_volume(utils.volume)
    else:
        pygame.mixer.Sound.play(utils.lose_sound).set_volume(utils.volume)

    # Info
    utils.draw_points(screen)
    utils.draw_time(screen, utils.time_remaining)

    pygame.display.flip()
    pygame.time.wait(3000)


def wheelie_game(screen, get_data, decrease_lives):
    """
    This function handles the 'wheelie' minigame.
    - screen: pygame screen.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global angle
    global angle_opponent
    global background

    # Initialise points variable
    points_counter = utils.points

    # Init bike sprite
    X = 350
    Y = (utils.height - 15) - (372 / 2) # 372 is the sprite's height, 20 is the floor's height
    bike = wheelie_files.bike.Bike(X, Y, False)
    bike_sprites = pygame.sprite.Group()
    bike_sprites.add(bike)
    angle = 0

    # Init opponent bike sprite
    X = 950
    opponent = wheelie_files.bike.Bike(X, Y, True)
    opponent_sprites = pygame.sprite.Group()
    opponent_sprites.add(opponent)

    # Init backgound images
    background = pygame.image.load("wheelie_files" + utils.sep + "background.png").convert_alpha()

    # Game
    pygame.mixer.music.load("wheelie_files" + utils.sep + "music.ogg")
    pygame.mixer.music.play(1) # Do not loop the song, play it once. -1 to play in a loop if you ever need it.
    seconds_counter = time.time()
    mathcing_time_remaining = 3
    utils.text_colour = (255, 0, 0)
    while True:
        if time.time() - seconds_counter > 1:
            utils.time_remaining -= 1
            mathcing_time_remaining -= 1

            # Check if the user has matched the opponent
            if mathcing_time_remaining == 0:
                mathcing_time_remaining = 3

                if abs(angle - angle_opponent) <= 15:
                    utils.points += 1

                angle_opponent = randint(0, 70)

            seconds_counter = time.time()

        if utils.time_remaining > 0:
            utils.run_in_thread(get_data)
            utils.check_data_integrity(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            screen.fill((0, 0, 0))
            # Backgound
            scroll_background(background, screen)

            # Check what button has been pressed
            if utils.data[0] == 3 and angle > 0: # Down
                angle -= 0.5
            elif utils.data[0] == 1 and angle < 70: # Up
                angle += 0.5

            bike_sprites.draw(screen)
            opponent_sprites.draw(screen)
            bike.wheel_angle(angle)
            opponent.wheel_angle(angle_opponent)

            bike_sprites.update()
            opponent_sprites.update()

            # Info
            utils.draw_text(screen, "U/D to wheelie", utils.width / 2, 322)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)
            utils.draw_number_counter(screen, mathcing_time_remaining)
            utils.run_in_thread(utils.draw_volume(screen))

            pygame.display.flip()
            utils.clock.tick(60)
        else:
            pygame.mixer.music.stop()
            if utils.points - points_counter < 3:
                # If true, the user lost.
                decrease_lives()
                end_anim(screen, False)
            else:
                end_anim(screen, True)
            
            utils.minigame_end(screen, get_data)

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