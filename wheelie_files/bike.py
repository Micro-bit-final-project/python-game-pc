import pygame, os, utils

class Bike(pygame.sprite.Sprite):
    """
    This class handles the bike sprite
    and its animation.
    """
    def __init__(self):
        """
        This function initialises the sprite by loading
        all the needed sprites for the animation and
        by generating the relative rect.
        """
        super().__init__()
        root = os.path.dirname(os.path.realpath(__file__))
        path = root + utils.sep

        self.sprites = []
        self.sprites.append(pygame.image.load(path + "bike_00.png"))
        self.sprites.append(pygame.image.load(path + "bike_01.png"))
        self.sprites.append(pygame.image.load(path + "bike_02.png"))
        self.sprites.append(pygame.image.load(path + "bike_03.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        self.X = 600
        self.Y = 600
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
        elif self.angle > 10 and self.angle < 25:
            self.image = self.sprites[1]
        elif self.angle > 25 and self.angle < 35:
            self.image = self.sprites[2]
        elif self.angle > 35:
            self.image = self.sprites[3]