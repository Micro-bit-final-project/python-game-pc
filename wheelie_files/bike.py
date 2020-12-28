import pygame, os, utils

class Bike(pygame.sprite.Sprite):
    """
    This class handles the bike sprite
    and its animation.
    """
    def __init__(self, x, y, opponent):
        """
        This function initialises the sprite by loading
        all the needed sprites for the animation and
        by generating the relative rect.
        """
        super().__init__()
        root = os.path.dirname(os.path.realpath(__file__))
        path = root + utils.sep

        self.sprites = []
        if opponent == True:
            self.sprites.append(pygame.image.load(path + "opponent_00.png"))
            self.sprites.append(pygame.image.load(path + "opponent_01.png"))
            self.sprites.append(pygame.image.load(path + "opponent_02.png"))
            self.sprites.append(pygame.image.load(path + "opponent_03.png"))
            self.sprites.append(pygame.image.load(path + "opponent_04.png"))
            self.sprites.append(pygame.image.load(path + "opponent_05.png"))
            self.sprites.append(pygame.image.load(path + "opponent_06.png"))
        else:
            self.sprites.append(pygame.image.load(path + "bike_00.png"))
            self.sprites.append(pygame.image.load(path + "bike_01.png"))
            self.sprites.append(pygame.image.load(path + "bike_02.png"))
            self.sprites.append(pygame.image.load(path + "bike_03.png"))
            self.sprites.append(pygame.image.load(path + "bike_04.png"))
            self.sprites.append(pygame.image.load(path + "bike_05.png"))
            self.sprites.append(pygame.image.load(path + "bike_06.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        self.X = x
        self.Y = y
        self.rect = self.image.get_rect(center=(self.X, self.Y))

        self.angle = 0

    def wheel_angle(self, angle):
        """
        This function is sued to receive the new
        angle of the bike.
        - angle: new angle.
        """
        self.angle = angle

    def update(self):
        """
        This function handles the bike rotation.
        """
        if self.angle < 10:
            self.image = self.sprites[0]
        elif self.angle > 10 and self.angle < 20:
            self.image = self.sprites[1]
        elif self.angle > 20 and self.angle < 30:
            self.image = self.sprites[2]
        elif self.angle > 30 and self.angle < 40:
            self.image = self.sprites[3]
        elif self.angle > 40 and self.angle < 50:
            self.image = self.sprites[4]
        elif self.angle > 50 and self.angle < 60:
            self.image = self.sprites[5]
        elif self.angle > 60:
            self.image = self.sprites[6]