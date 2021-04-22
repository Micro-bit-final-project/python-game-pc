import pygame, utils, template-minigame_files.sprite1, sys, time
from random import randint

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
        img = pygame.image.load("template-minigame_files" + utils.sep + "win.png").convert_alpha()
    else:
        img = pygame.image.load("template-minigame_files" + utils.sep + "lose.png").convert_alpha()

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

def templateminigame_game(screen, get_data, decrease_lives):
    """
    This function handles the 'template-minigame' minigame.
    - screen: pygame.display to draw to.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global X
    global Y
    global background

    # Initialise points variable
    points_counter = utils.points

    # Load main sprite:
    # Use this method only if the sprite is a single image.
    # If you want to animate it, jump to line #68
    # to see how to import an animated sprite.
    main_sprite = pygame.image.load("template-minigame_files" + utils.sep + "main.png").convert_alpha()

    # Main sprite's coordinates
    X = 600
    Y = utils.height - 20 - 320 # 320 is the sprite's height, just an example

    # Init animated sprite
    animated_sprite = template-minigame_files.sprite1.Sprite1()
    animated_sprite_g = pygame.sprite.Group()
    animated_sprite_g.add(animated_sprite)

    # Load backgound image
    background = pygame.image.load("template-minigame_files" + utils.sep + "background.png").convert_alpha()

    # Game
    pygame.mixer.music.load("template-minigame_files" + utils.sep + "music.ogg")
    pygame.mixer.music.play(1) # Do not loop the song, play it once. -1 to play in a loop if you ever need it.
    seconds_counter = time.time()
    utils.text_colour = (255, 255, 255) # Set the text colour for the minigame
    while True:
        # Game logic
        if time.time() - seconds_counter > 1:
            # Timer
            utils.time_remaining -= 1
            seconds_counter = time.time()

        if utils.time_remaining > 0: # Enough time remaining condition
            utils.run_in_thread(get_data)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0, 0, 0))

            # Microbit input here. Manipulate the data
            # as per minigame's needs. The data comes in
            # an array stored in the utils.data variable.
            # Example of data manipulation (from dinorun minigame):
            jump = (utils.data[0] == 1)

            animated_sprite.animate()

            screen.blit(background, (0, 0))
            animated_sprite_g.draw(screen)
            animated_sprite_g.update()

            # Info
            utils.draw_text(screen, "Insert info here", utils.width / 2, 322)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)
            utils.run_in_thread(utils.draw_volume(screen))

            pygame.display.flip()
            utils.clock.tick(60) # Pick the clock that best suits your game
        else:
            pygame.mixer.music.stop()
            if utils.points - points_counter < 6:
                # If true, the user lost. Feel free to change the points needed to win
                decrease_lives()
                end_anim(screen, False)
            else:
                end_anim(screen, True)

            utils.minigame_end(screen, get_data)
            break
    return