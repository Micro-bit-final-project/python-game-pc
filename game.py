import pygame
import serial
import sys
import os
import utils
import microbit_serial as ubit
import connection_files.checkmark
from random import randint

# Minigames
import wheelie
import engine
minigames = [wheelie.wheelie_game, engine.engine_game]

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
    if port.in_waiting > 0:
        # Obtain data from the microbit
        utils.data = ubit.data(port)
        while type(utils.data) != list: # Make sure message is intact and wait for it to come
            utils.data = ubit.data(port)
        print(utils.data)
        port.write("Y".encode()) # Let the microbit know we received the data


def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        utils.time_remaining = 27
        minigame = minigames[randint(0, len(minigames) - 1)]
        minigame(screen, get_data)


def menu():
    """
    This function handles the game menu.
    """
    screen.fill((0, 0, 0))
    utils.draw_text(screen, "Press any button to start the game", utils.width / 2, utils.height - utils.height / 5)
    pygame.display.flip()

if __name__ == "__main__":
    menu()
    port.write("Y".encode()) # Sync microbit and computer
    while True:
        get_data()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if type(utils.data[0]) == float and utils.data[0] != 0:
            break
    game()

