import pygame, utils, dinorun_files.dino, dinorun_files.wizard, sys, time
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
        img = pygame.image.load("dinorun_files" + utils.sep + "win.png").convert_alpha()
    else:
        img = pygame.image.load("dinorun_files" + utils.sep + "lose.png").convert_alpha()

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

def dinorun_game(screen, get_data):
    """
    This function handles the dinorun minigame.
    - screen: pygame.display to draw to.
    - get_data: get_data function to retrieve data
                from the microbit.
    """
    global X
    global Y
    global background

    # Initialise points variable
    points = 0

    # Init dinosaur sprite
    dinosaur_sprite = dinorun_files.dino.Dino()
    dinosaur_sprite_g = pygame.sprite.Group()
    dinosaur_sprite_g.add(dinosaur_sprite)
    # Init wizard sprite
    wizard_sprite = dinorun_files.wizard.Wizard()
    wizard_sprite_g = pygame.sprite.Group()
    wizard_sprite_g.add(wizard_sprite)

    # Load backgound image
    background = pygame.image.load("dinorun_files" + utils.sep + "background.png").convert_alpha()

    # Game
    pygame.mixer.music.load("dinorun_files" + utils.sep + "music.ogg")
    pygame.mixer.music.play(1) # Do not loop the song, play it once. -1 to play in a loop if you ever need it.
    seconds_counter = time.time()
    utils.text_colour = (255, 255, 255) # Set the text colour for the minigame
    while True:
        # Game logic
        if points == 10: # winning condition
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

            jump = (utils.data[0] == 1)
            dinosaur_sprite.animate(jump)
            wizard_sprite.animate()

            screen.blit(background, (0, 0))
            dinosaur_sprite_g.draw(screen)
            wizard_sprite_g.draw(screen)
            dinosaur_sprite_g.update()
            wizard_sprite_g.update()

            # Info
            utils.draw_text(screen, "U to jump", utils.width / 2, 322)
            utils.draw_points(screen)
            utils.draw_time(screen, utils.time_remaining)

            pygame.display.flip()
            utils.clock.tick(60)
        else:
            pygame.mixer.music.stop()
            if points < 10: # If true, the user lost
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