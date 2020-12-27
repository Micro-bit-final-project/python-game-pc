import pygame, wheelie_files.bike, utils, sys

bgX = 0 # Start of the screen

angle = 0

def scroll_background(background, screen):
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

    # Init bike sprite
    bike = wheelie_files.bike.Bike()
    bike_sprites = pygame.sprite.Group()
    bike_sprites.add(bike)

    # Init backgound images
    background = pygame.image.load("wheelie_files" + utils.sep + "background.png").convert_alpha()

    # Game
    while True:
        utils.run_in_thread(get_data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((0, 0, 0))
        # Backgound
        scroll_background(background, screen)

        # Map the data coming from the microbit to a
        # scale of 0 to 60.
        #if utils.data and len(utils.data) == 3:
        angle = utils.map(utils.data[2], 2, 1023, 0, 60)

        bike_sprites.draw(screen)
        bike.wheel_angle(angle)

        bike_sprites.update()

        pygame.display.flip()
        utils.clock.tick(60)