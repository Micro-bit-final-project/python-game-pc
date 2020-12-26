import pygame, sys
import microbit_serial as ubit

# Init pygame
pygame.init()
clock = pygame.time.Clock()
width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    menu()