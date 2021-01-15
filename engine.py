import pygame, utils, engine_files.engine_temp, engine_files.smoke, sys, time
from random import randint

def engine_game(screen, get_data):
    """
    This function handles the 'wheelie' minigame.
    - screen: pygame screen.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global angle
    global angle_opponent
    blow_points = 0
    old_blow_points = 0
    stage = 0

    # Init car sprite
    X = 600
    Y = utils.height - 20 - 320 # 320 is the sprite's height
    car = pygame.image.load("engine_files" + utils.sep + "car.png").convert_alpha()

    # Init engine temperature sprite
    temp_indicator = engine_files.engine_temp.EngineTemp()
    indicator_sprites = pygame.sprite.Group()
    indicator_sprites.add(temp_indicator)

    # Init smoke sprite
    smoke = engine_files.smoke.Smoke()
    smoke_sprites = pygame.sprite.Group()
    smoke_sprites.add(smoke)

    # Init backgound images
    background = pygame.image.load("engine_files" + utils.sep + "background.png").convert_alpha()

    # Game
    seconds_counter = time.time()
    utils.text_colour = (190, 150, 200)
    while True:
        old_blow_points = blow_points

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
            # Using the potentiometer for dev purposes
            blow = utils.map(utils.data[2], 2, 1023, 0, 100)
            if blow > 50:
                blow_points += 0.01
            elif blow > 90:
                blow_points += 0.05
            if int(blow_points) > int(old_blow_points):
                if stage == 5:
                    #win_animation()
                    utils.time_remaining = 0 # Make sure the game stops
                else:
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