import pygame, os, utils

class Smoke(pygame.sprite.Sprite):
    """
    This class handles the smoke sprite
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
        self.sprites.append(pygame.image.load(path + "smoke_00.png"))
        self.sprites.append(pygame.image.load(path + "smoke_01.png"))
        self.sprites.append(pygame.image.load(path + "smoke_02.png"))
        self.sprites.append(pygame.image.load(path + "smoke_03.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        self.X = utils.width / 2
        self.Y = utils.height - 100 - 267 # 267 is the sprite's height
        self.rect = self.image.get_rect(center=(self.X, self.Y))

    def animate(self):
        """
        This function is called to animate
        the smoke.
        """
        self.stage += 0.05
        if self.stage > 3:
            self.stage = 0

    def update(self):
        """
        This function handles the smoke animation.
        """
        self.image = self.sprites[int(self.stage)]