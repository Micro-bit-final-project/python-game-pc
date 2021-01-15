import pygame, utils, engine_files.engine_temp, engine_files.smoke, sys, time
from random import randint

# Global variables
X = 0
Y = 0
car = 0
background = 0

def win_animation(screen):
    global X
    global Y
    global car
    global background

    win = pygame.image.load("engine_files" + utils.sep + "win.png").convert_alpha()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(car, (X, Y))
    win_rect = win.get_rect()
    win_rect.center = (utils.width / 2, utils.height/2)
    screen.blit(win, win_rect)

    # Win sound
    pygame.mixer.Sound.play(utils.win_sound)

    # Info
    utils.draw_points(screen)
    utils.draw_time(screen, utils.time_remaining)

    pygame.display.flip()
    pygame.time.wait(3000)

def engine_game(screen, get_data):
    """
    This function handles the 'wheelie' minigame.
    - screen: pygame screen.
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
            win_animation(screen)
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
            blow = utils.map(utils.data[3], 570, 1023, 0, 100)
            if blow > 35:
                blow_points += 0.05
            elif blow > 90:
                blow_points += 0.08

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
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)

            pygame.display.flip()
            utils.clock.tick(60)
        else:
            pygame.mixer.music.stop()
            screen.fill((0, 0, 0))
            # Points
            font = pygame.font.Font("fonts/dpcomic/dpcomic.ttf", 100)
            points_img = font.render("Points scored: {}".format(utils.points), True, (255, 255, 255))
            points_rect = points_img.get_rect()
            X = int(utils.width / 2)
            Y = int(utils.height / 5)
            points_rect.center = (X, Y)
            # Continue
            font = pygame.font.Font("fonts/dpcomic/dpcomic.ttf", 100)
            continue_img = font.render("Press any button to continue".format(utils.points), True, (255, 255, 255))
            continue_rect = continue_img.get_rect()
            X = int(utils.width / 2)
            Y = utils.height - int(utils.height / 5)
            continue_rect.center = (X, Y)
            # Draw
            screen.blit(points_img, points_rect)
            screen.blit(continue_img, continue_rect)
            pygame.display.flip()

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