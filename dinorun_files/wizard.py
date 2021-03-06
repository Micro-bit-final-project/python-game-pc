import pygame, os, utils

class Wizard(pygame.sprite.Sprite):
    """
    This class handles the wizard sprite
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

        self.sprites = [] # Array containing all the sprites for animation.
        self.sprites.append(pygame.image.load(path + "wizard_00.png"))
        self.sprites.append(pygame.image.load(path + "wizard_01.png"))
        self.sprites.append(pygame.image.load(path + "wizard_02.png"))
        self.sprites.append(pygame.image.load(path + "wizard_03.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        # Coordinates
        self.X = utils.width
        self.Y = utils.height - 100 - 160 # 160 is the sprite's height
        self.rect = self.image.get_rect(center=(self.X, self.Y))

    def animate(self):
        """
        This function is called to animate
        the sprite.
        """
        self.stage += 0.15
        if self.stage > 3:
            self.stage = 0

    def update(self):
        """
        This function handles the sprite animation.
        """
        self.image = self.sprites[int(self.stage)]
        self.X -= 5
        if self.X < 0:
            self.X = utils.width
        self.rect = self.image.get_rect(center=(self.X, self.Y))