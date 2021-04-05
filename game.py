import pygame
import serial
import sys
import os
import utils
import microbit_serial as ubit
import connection_files.checkmark
from menu_files.backgrounds import Backgrounds
from random import randint

# Minigames
import wheelie
import engine
import coin
import overcoock
import match
import dinorun

#minigames = [wheelie.wheelie_game, engine.engine_game, coin.coin_game, overcoock.overcoock_game, match.match_game]
minigames = [engine.engine_game, coin.coin_game, overcoock.overcoock_game, match.match_game, dinorun.dinorun_game]

# Init pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((utils.width, utils.height))
utils.clock = pygame.time.Clock()
utils.win_sound =  pygame.mixer.Sound("sounds" + utils.sep + "win.ogg")
utils.lose_sound = pygame.mixer.Sound("sounds" + utils.sep + "lose.ogg")
utils.text_colour = (255, 255, 255)

def connect_notice(status):
    """
    This function displays information about
    the microbit connection status before the
    game starts.
    status - Boolean value, true if connected.
    """
    screen.fill((0, 0, 0))
    microbit_img = pygame.image.load("connection_files" + utils.sep + "microbit.png").convert_alpha()
    microbit_rect = microbit_img.get_rect()
    microbit_rect.center = (utils.width / 2, utils.height / 2)
    screen.blit(microbit_img, microbit_rect)
    if status == False:
        utils.draw_text(screen, "Please connect a microbit controller", utils.width / 2, utils.height - (utils.height / 5))
        pygame.display.flip()
    else:
        # Init checkmark sprite
        checkmark = connection_files.checkmark.Checkmark()
        checkmark_sprites = pygame.sprite.Group()
        checkmark_sprites.add(checkmark)
        while utils.done_setup == False:
            checkmark.animate()
            checkmark_sprites.update()
            checkmark_sprites.draw(screen)
            pygame.display.flip()
            utils.clock.tick(60)
        pygame.time.wait(1500)


# Connect to the microbit
port = ubit.connect()
run_notice = False
while type(port) is not serial.Serial:
    print("Looking for a microbit")
    run_notice = True
    port = ubit.connect()
    connect_notice(False)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

print("Microbit Found")
if run_notice == True:
    connect_notice(True)

port.open()

def get_data():
    """
    This function is used to loop the retrieving of data
    from the microbit. It depends on microbit_serial
    functions.
    """
    try:
        if port.in_waiting > 0:
            # Obtain data from the microbit
            utils.data = ubit.data(port)
            while type(utils.data) != list: # Make sure message is intact and wait for it to come
                utils.data = ubit.data(port)
            print(utils.data)
            port.write("Y".encode()) # Let the microbit know we received the data
            utils.check_data_integrity(screen)
    except: # Controller disconnected
        utils.data = [-1, -1, -1, -1]

def decrease_lives():
    """
    This function decreases by one the lives variable
    and sends an instruction to the microbit so that
    it turns off one LED.
    """
    try:
        utils.lives -= 1
        port.write("D".encode())
    except: # Controller disconnected
        utils.data = [-1, -1, -1, -1]

def reset_lives():
    """
    This function sends an instruction to the microbit
    so that all the 8 LEDs light up and it resets
    the lives variable to 8.
    """
    try:
        utils.lives = 8
        port.write("R".encode())
    except: # Controller disconnected
        utils.data = [-1, -1, -1, -1]

def game():
    """
    This function is used to handle the randomisation of the
    minigames sequence. It randomises the order, starts a minigame
    and eventually return back to the main menu if the user loses
    all the lives.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        utils.time_remaining = 27
        minigame = minigames[randint(0, len(minigames) - 1)]
        print("LIVES: {}".format(utils.lives))
        minigame(screen, get_data, decrease_lives)
        print("LIVES: {}".format(utils.lives))
        if (utils.lives == 0):
            decrease_lives()
            utils.lives = 8
            break


def menu():
    """
    This function handles the game menu.
    """
    # Reset lives
    reset_lives()

    options = ["Press any button to start the game", "Credits"]

    # Create shade surface
    shade = pygame.Surface((utils.width, utils.height))
    shade.fill((0, 0, 0))
    alpha = 0
    shade.set_alpha(alpha)
    alpha_increment = True # Whether or not to increment the shade's alpha
    animate = True # Whether or not to animate the menu backgrounds

    # Init backgrounds sprite
    backgrounds_sprite = Backgrounds(os.path.dirname(os.path.realpath(__file__)), shade)
    backgrounds_sprite_g = pygame.sprite.Group()
    backgrounds_sprite_g.add(backgrounds_sprite)

    selected_option = 0

    while True:
        utils.run_in_thread(get_data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Elaborate microbit data
        if utils.data[0] == 1 and selected_option > 0:
            selected_option -= 1
        elif utils.data[0] == 3 and selected_option < 1:
            selected_option += 1
        elif utils.data[0] == 2 or utils.data[0] == 4:
            utils.run_in_thread(get_data)
            utils.data[0] = 0 # Clean to avoid interferance with games
            break # TODO: Implement credits screen
        print(utils.data)
        screen.fill((0, 0, 0))
        # Shade alpha
        if (int(utils.stage) < int(utils.stage + 0.01) and animate == True) or (alpha == 0 and alpha_increment == False):
            alpha_increment = not alpha_increment
            backgrounds_sprite.animate() # Animate for one last time so that the next background fades in
        if alpha_increment == True:
            alpha += 2
        else:
            alpha -= 2
        shade.set_alpha(alpha)
        # Draw backgrounds
        if alpha_increment == True:
            backgrounds_sprite.animate()
            animate = True
        else:
            animate = False
        backgrounds_sprite_g.update()
        backgrounds_sprite_g.draw(screen)
        # Draw shade
        screen.blit(shade, (0, 0))
        # Draw options
        for o in range(0, len(options)):
            if selected_option == o:
                utils.text_colour = (255, 0, 0)
            else:
                utils.text_colour = (204, 136, 0)
            utils.draw_text(screen, options[o], utils.width / 2 - 5, (utils.height / 2) - 5 + 150 * o)
            utils.text_colour = (255, 255, 255)
            utils.draw_text(screen, options[o], utils.width / 2, (utils.height / 2) + 150 * o)
        pygame.display.flip()
        utils.clock.tick(15)

if __name__ == "__main__":
    while True:
        port.write("Y".encode()) # Sync microbit and computer
        menu()
        game()

