import pygame, utils, overcoock_files.meat, overcoock_files.fire, sys, time

# Global variables
X = 0
Y = 0
background = 0

def end_anim(screen, points, decrease_lives):
    """
    This function handles the final animation of a game.
    - screen: pygame.display to draw to.
    - points: points scored
    """
    global X
    global Y
    global background

    if points == 5:
        img = pygame.image.load("overcoock_files" + utils.sep + "win.png").convert_alpha()
    elif points == 2:
        img = pygame.image.load("overcoock_files" + utils.sep + "ok.png").convert_alpha()
    else:
        decrease_lives()
        img = pygame.image.load("overcoock_files" + utils.sep + "lose.png").convert_alpha()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    img_rect = img.get_rect()
    img_rect.center = (utils.width / 2, utils.height/2)
    screen.blit(img, img_rect)

    # Increment points
    utils.points += points

    # Sound
    if points > 0:
        pygame.mixer.Sound.play(utils.win_sound).set_volume(utils.volume)
    else:
        pygame.mixer.Sound.play(utils.lose_sound).set_volume(utils.volume)

    # Info
    utils.draw_points(screen)
    utils.draw_time(screen, utils.time_remaining)

    pygame.display.flip()
    pygame.time.wait(3000)

def overcoock_game(screen, get_data, decrease_lives):
    """
    This function handles the overcoock minigame.
    - screen: pygame.display to draw to.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global X
    global Y
    global background

    # Initialise here the points variables
    points = 0
    stage = 0
    presses = 0


    # Init meat sprite
    meat_sprite = overcoock_files.meat.Meat()
    meat_sprite_g = pygame.sprite.Group()
    meat_sprite_g.add(meat_sprite)

    # Init fire sprite
    fire_sprite = overcoock_files.fire.Fire()
    fire_sprite_g = pygame.sprite.Group()
    fire_sprite_g.add(fire_sprite)

    # Load backgound image
    background = pygame.image.load("overcoock_files" + utils.sep + "background.png").convert_alpha()

    # Game
    pygame.mixer.music.load("overcoock_files" + utils.sep + "music.ogg")
    pygame.mixer.music.play(1) # Do not loop the song, play it once. -1 to play in a loop if you ever need it.
    seconds_counter = time.time()
    utils.text_colour = (98, 28, 68) # Set the text colour for the minigame
    utils.data[0] = 0 # Resest the control number as it might get mashed from the mid minigames screen.
    while True:
        # Game logic
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

            # Register 125 (5 / (1 / 25)) button inputs (Down) to increase cooking state.
            # Register 1 button input (Up) to finish cooking.
            up = (utils.data[0] == 1)
            down = (utils.data[0] == 3)
            if down == True:
                presses += 1 / 25
                if int(presses) == 5:
                    presses = 0
                    if stage < 6:
                        stage += 1
                    meat_sprite.animate(stage)
            elif up == True:
                if stage < 3:
                    points = 0
                elif stage < 5:
                    points = 2
                elif stage < 6:
                    points = 5
                else:
                    points = 0
                utils.time_remaining = 0

            # Animate the fire sprite
            fire_sprite.animate()

            screen.blit(background, (0, 0))
            meat_sprite_g.draw(screen)
            fire_sprite_g.draw(screen)
            meat_sprite_g.update()
            fire_sprite_g.update()

            # Info
            utils.draw_text(screen, "U to finish, D to cook", utils.width / 2, 322)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)

            pygame.display.flip()
            utils.clock.tick(60)
        else:
            pygame.mixer.music.stop()
            end_anim(screen, points, decrease_lives)
            utils.minigame_end(screen, get_data)
            break
    return