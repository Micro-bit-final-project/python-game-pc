import pygame, wheelie_files.bike, utils, sys, time
from random import randint

bgX = 0 # Start of the screen

angle = 0
angle_opponent = randint(0, 70)

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


def wheelie_game(screen, get_data):
    """
    This function handles the 'wheelie' minigame.
    - screen: pygame screen.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global angle
    global angle_opponent

    # Init bike sprite
    X = 350
    Y = 805 - (372 / 2) # 372 is the sprite's height
    bike = wheelie_files.bike.Bike(X, Y, False)
    bike_sprites = pygame.sprite.Group()
    bike_sprites.add(bike)

    # Init opponent bike sprite
    X = 950
    opponent = wheelie_files.bike.Bike(X, Y, True)
    opponent_sprites = pygame.sprite.Group()
    opponent_sprites.add(opponent)

    # Init backgound images
    background = pygame.image.load("wheelie_files" + utils.sep + "background.png").convert_alpha()

    # Game
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

                if abs(angle - angle_opponent) <= 9:
                    utils.points += 1

                angle_opponent = randint(0, 70)

            seconds_counter = time.time()

        if utils.time_remaining > 0:
            utils.run_in_thread(get_data)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            screen.fill((0, 0, 0))
            # Backgound
            scroll_background(background, screen)

            # Info
            utils.draw_number_counter(screen, mathcing_time_remaining)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)

            # Map the data coming from the microbit to a
            # scale of 0 to 60.
            angle = utils.map(utils.data[2], 2, 1023, 0, 70)

            bike_sprites.draw(screen)
            opponent_sprites.draw(screen)
            bike.wheel_angle(angle)
            opponent.wheel_angle(angle_opponent)

            bike_sprites.update()
            opponent_sprites.update()

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