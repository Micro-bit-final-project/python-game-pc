import pygame
import serial
import sys
import microbit_serial as ubit

# Init pygame
pygame.init()
clock = pygame.time.Clock()
width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))

data = [0, 0]

# Connect to the microbit
port = ubit.connect()
while type(port) is not serial.Serial:
    print("Looking for a microbit")
    port = ubit.connect()

print("Microbit Found")
port.open()

def get_data():
    global data
    if port.in_waiting > 0:
        # Obtain data from the microbit
        data = ubit.data(port)
        while type(data) != list: # Make sure message is intact and wait for it to come
            data = ubit.data(port)
        print(data)


def game():
    pygame.quit()
    sys.exit()


def menu():
    """
    This function handles the game menu.
    """
    font = pygame.font.Font("fonts/dpcomic/dpcomic.ttf", 100)
    press_btn_img = font.render("Press any button to start the game", True, (255, 255, 255))
    press_btn_rect = press_btn_img.get_rect()
    X = int(width / 2)
    Y = height - int(height / 5)
    press_btn_rect.center = (X, Y)
    screen.blit(press_btn_img, press_btn_rect)
    pygame.display.flip()

if __name__ == "__main__":
    menu()
    while True:
        get_data()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if type(data[0]) == float and data[0] != 0:
            break
    game() # Placeholder for further development

