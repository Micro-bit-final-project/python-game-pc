import pygame, os, utils

class Meat(pygame.sprite.Sprite):
    """
    This class handles the meat sprite
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
        self.sprites.append(pygame.image.load(path + "meat_00.png"))
        self.sprites.append(pygame.image.load(path + "meat_01.png"))
        self.sprites.append(pygame.image.load(path + "meat_02.png"))
        self.sprites.append(pygame.image.load(path + "meat_03.png"))
        self.sprites.append(pygame.image.load(path + "meat_04.png"))
        self.sprites.append(pygame.image.load(path + "meat_05.png"))
        self.sprites.append(pygame.image.load(path + "meat_06.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        # Coordinates, change as needed
        self.X = utils.width / 2
        self.Y = (utils.height / 2) + 100
        self.rect = self.image.get_rect(center=(self.X, self.Y))

    def animate(self, stage):
        """
        This function is called to animate
        the sprite.
        - stage: stage of the animation.
        """
        self.stage = stage

    def update(self):
        """
        This function handles the sprite animation.
        """
        self.image = self.sprites[int(self.stage)]