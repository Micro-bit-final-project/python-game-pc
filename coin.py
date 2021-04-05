import pygame, utils, coin_files.coin, sys, time
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
    global car
    global background

    if win:
        img = pygame.image.load("coin_files" + utils.sep + "win.png").convert_alpha()
    else:
        img = pygame.image.load("coin_files" + utils.sep + "lose.png").convert_alpha()

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

def coin_game(screen, get_data, decrease_lives):
    """
    This function handles the 'coin' minigame.
    - screen: pygame.display to draw to.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global X
    global Y
    global background

    # Initialise here the points variables
    points_counter = utils.points
    other_useful_var = 0

    # Load bucket sprite
    bucket_sprite = pygame.image.load("coin_files" + utils.sep + "bucket.png").convert_alpha()

    # Main sprite's coordinates
    X = utils.width / 2
    Y = utils.height - (320 / 2) - 20 # 320 is the sprite's height


    # Init coin sprite
    coin_sprite = coin_files.coin.Coin()
    coin_sprite_g = pygame.sprite.Group()
    coin_sprite_g.add(coin_sprite)

    # Load backgound image
    background = pygame.image.load("coin_files" + utils.sep + "background.png").convert_alpha()

    # Game
    pygame.mixer.music.load("coin_files" + utils.sep + "music.ogg")
    pygame.mixer.music.play(1) # Do not loop the song, play it once. -1 to play in a loop if you ever need it.
    seconds_counter = time.time()
    utils.text_colour = (200, 89, 78) # Set the text colour for the minigame
    while True:
        # Game logic
        if utils.points - points_counter == 5: # winning condition
            pygame.mixer.music.stop()
            end_anim(screen, True)
            utils.time_remaining = 0 # Make sure the game stops

        if time.time() - seconds_counter > 1:
            utils.time_remaining -= 1
            seconds_counter = time.time()

        if utils.time_remaining > 0:
            utils.run_in_thread(get_data)
            utils.check_data_integrity(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0, 0, 0))

            # Check what button has been pressed
            if utils.data[0] == 2: # Left
                X -= 5
            elif utils.data[0] == 4: # Right
                X += 5

            
            bucket_rect = bucket_sprite.get_rect(center=(X, Y))
            # Coin animation
            coin_sprite.animate(bucket_rect)

            screen.blit(background, (0, 0))
            coin_sprite_g.draw(screen)
            screen.blit(bucket_sprite, bucket_rect)
            coin_sprite_g.update()

            # Info
            utils.draw_text(screen, "R and L buttons to move", utils.width / 2, 222)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)

            pygame.display.flip()
            utils.clock.tick(60)
        else:
            pygame.mixer.music.stop()
            if utils.points - points_counter < 5: # If true, the user lost
                end_anim(screen, False)

            decrease_lives()
            utils.minigame_end(screen, get_data)
            break
    return