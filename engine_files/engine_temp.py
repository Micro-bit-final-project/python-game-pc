import pygame, os, utils

class EngineTemp(pygame.sprite.Sprite):
    """
    This class handles the engine temperature
    indicator and its animation.
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
        self.sprites.append(pygame.image.load(path + "engine_00.png"))
        self.sprites.append(pygame.image.load(path + "engine_01.png"))
        self.sprites.append(pygame.image.load(path + "engine_02.png"))
        self.sprites.append(pygame.image.load(path + "engine_03.png"))
        self.sprites.append(pygame.image.load(path + "engine_04.png"))
        self.sprites.append(pygame.image.load(path + "engine_05.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        self.X = utils.width / 2
        self.Y = 222 # Sprite's height + 100px
        self.rect = self.image.get_rect(center=(self.X, self.Y))

    def change_temp(self, stage):
        """
        This function is called to change
        the displayed engine temperature.
        - stage: new sprite stage.
        """
        self.stage = stage

    def update(self):
        """
        This function handles indicator animation.
        """
        self.image = self.sprites[self.stage]