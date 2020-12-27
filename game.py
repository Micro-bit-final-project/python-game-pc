import pygame
import serial
import sys
import os
import utils
import microbit_serial as ubit

# Minigames
import wheelie

# Init pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((utils.width, utils.height))
utils.clock = pygame.time.Clock()

# Connect to the microbit
port = ubit.connect()
while type(port) is not serial.Serial:
    print("Looking for a microbit")
    port = ubit.connect()

print("Microbit Found")
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
    wheelie.wheelie_game(screen, get_data)


def menu():
    """
    This function handles the game menu.
    """
    font = pygame.font.Font("fonts/dpcomic/dpcomic.ttf", 100)
    press_btn_img = font.render("Press any button to start the game", True, (255, 255, 255))
    press_btn_rect = press_btn_img.get_rect()
    X = int(utils.width / 2)
    Y = utils.height - int(utils.height / 5)
    press_btn_rect.center = (X, Y)
    screen.blit(press_btn_img, press_btn_rect)
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

