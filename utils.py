import os
import pygame
from threading import Thread
import sys

data = [0, 0, 0]
clock = 0
width = 1600
height = 900
sep = os.path.sep
points = 0
time_remaining = 27
text_colour = (0, 0, 0)
win_sound = 0
lose_sound = 0
done_setup = False
stage = 0


def map(x, in_min, in_max, out_min, out_max):
    """
    From https://www.arduino.cc/reference/en/language/functions/math/map/
    Re-maps a number from one range to another.
    That is, a value of fromLow would get mapped to toLow,
    a value of fromHigh to toHigh, values in-between to values in-between, etc.

    - value: the number to map.
    - fromLow: the lower bound of the value’s current range.
    - fromHigh: the upper bound of the value’s current range.
    - toLow: the lower bound of the value’s target range.
    - toHigh: the upper bound of the value’s target range.
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def check_data_integrity(screen):
    """
    This functions makes sure that the microbit has not been disconnected.
    All the items in the array have a value of -1 if the connection is lost.
    In case it is, the user needs to restart the game.

    - screen: The screen to draw directions on.
    """
    if data[0] == -1:
        screen.fill((0, 0, 0))
        text_colour = (255, 255, 255)
        draw_text(screen, "Controller disconnected", width / 2, height / 2)
        draw_text(screen, "Please restart the game", width / 2, (height / 2) + 200)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

def run_in_thread(func):
    """
    This function is used to run a function
    fun in a separate thread.
    - func: The function to run in a different thread.
    """
    thread = Thread(target=func)
    thread.daemon = True
    thread.start()


def draw_text(screen, text, X, Y):
    """
    This function draws any text to the screen.
    - screen: pygame.displayto draw to.
    - text: string of the text to draw.
    - X: x coordinate of the center of the text.
    - Y: y coordinate of the center of the text.
    """
    font = pygame.font.Font("fonts/dpcomic/dpcomic.ttf", 100)
    text_img = font.render(text, True, text_colour)
    text_rect = text_img.get_rect()
    text_rect.center = (X, Y)
    screen.blit(text_img, text_rect)


def draw_number_counter(screen, number):
    """
    This function draws the remaining time to
    complete an action.
    - screen: pygame.display to draw to.
    - number: int of time remaining.
    """
    X = int(width / 2)
    Y = 200
    draw_text(screen, str(number), X, Y)


def draw_points(screen):
    """
    This function draws the points scored by the user
    during the game.
    - screen: pygame.display to draw to.
    """
    X = width - 200
    Y = 50
    draw_text(screen, "Points: {}".format(points), X, Y)


def draw_time(screen, time):
    """
    This function draws the remaining game time.
    - screen: pygame.display to draw to.
    - time: int of time remaining.
    """
    if time == 10:
        X = 390
    else:
        X = 370
    Y = 50
    draw_text(screen, "Time remaining: {}s".format(time), X, Y)


def minigame_end(screen):
    """
    This function is called to display the recap screen
    after each minigame.
    - screen: pygame.display to draw to.
    """
    # Reset time
    time_remaining = 27

    screen.fill((0, 0, 0))
    # Points
    font = pygame.font.Font("fonts/dpcomic/dpcomic.ttf", 100)
    points_img = font.render("Points scored: {}".format(points), True, (255, 255, 255))
    points_rect = points_img.get_rect()
    X = int(width / 2)
    Y = int(height / 5)
    points_rect.center = (X, Y)
    # Continue
    font = pygame.font.Font("fonts/dpcomic/dpcomic.ttf", 100)
    continue_img = font.render("Press any button to continue", True, (255, 255, 255))
    continue_rect = continue_img.get_rect()
    X = int(width / 2)
    Y = height - int(height / 5)
    continue_rect.center = (X, Y)
    # Draw
    screen.blit(points_img, points_rect)
    screen.blit(continue_img, continue_rect)
    pygame.display.flip()
