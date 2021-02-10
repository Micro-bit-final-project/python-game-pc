import pygame, utils, engine_files.engine_temp, engine_files.smoke, sys, time
from random import randint

# Global variables
X = 0
Y = 0
car = 0
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
    global car
    global background

    if win:
        img = pygame.image.load("engine_files" + utils.sep + "win.png").convert_alpha()
    else:
        img = pygame.image.load("engine_files" + utils.sep + "lose.png").convert_alpha()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(car, (X, Y))
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

def engine_game(screen, get_data):
    """
    This function handles the 'wheelie' minigame.
    - screen: pygame.display to draw to.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global angle
    global angle_opponent
    global X
    global Y
    global car
    global background

    blow_points = 0
    old_blow_points = 0
    stage = 0

    # Load car sprite
    car = pygame.image.load("engine_files" + utils.sep + "car.png").convert_alpha()

    # Car sprite's coordinates
    X = 600
    Y = utils.height - 20 - 320 # 320 is the sprite's height

    # Init engine temperature sprite
    temp_indicator = engine_files.engine_temp.EngineTemp()
    indicator_sprites = pygame.sprite.Group()
    indicator_sprites.add(temp_indicator)

    # Init smoke sprite
    smoke = engine_files.smoke.Smoke()
    smoke_sprites = pygame.sprite.Group()
    smoke_sprites.add(smoke)

    # Load backgound image
    background = pygame.image.load("engine_files" + utils.sep + "background.png").convert_alpha()

    # Game
    pygame.mixer.music.load("engine_files" + utils.sep + "music.ogg")
    pygame.mixer.music.play(1) # Do not loop the song, play it once
    seconds_counter = time.time()
    utils.text_colour = (190, 150, 200)
    while True:
        old_blow_points = blow_points

        if stage == 5:
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

            # Map the data coming from the microbit to a
            # scale of 0 to 100.
            # If the engine is not spinning, the pin is floating
            # due to the diode protection. Might need adjustement.
            blow = utils.map(utils.data[3], 7, 1023, 0, 100)
            if blow > 90:
                blow_points += 0.02

            if int(blow_points) > int(old_blow_points):
                stage += 1
                utils.points += 1
                temp_indicator.change_temp(stage)

            smoke.animate()

            screen.blit(background, (0, 0))
            indicator_sprites.draw(screen)
            screen.blit(car, (X, Y))
            smoke_sprites.draw(screen)
            smoke_sprites.update()
            indicator_sprites.update()

            # Info
            utils.draw_text(screen, "Blow on the fan!", utils.width / 2, 322)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)

            pygame.display.flip()
            utils.clock.tick(60)
        else:
            if stage < 5:
                end_anim(screen, False)

            pygame.mixer.music.stop()
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