import pygame, os, utils

class Checkmark(pygame.sprite.Sprite):
    """
    This class handles the checkmark sprite
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
        self.sprites.append(pygame.image.load(path + "check_00.png"))
        self.sprites.append(pygame.image.load(path + "check_01.png"))
        self.sprites.append(pygame.image.load(path + "check_02.png"))
        self.sprites.append(pygame.image.load(path + "check_03.png"))
        self.sprites.append(pygame.image.load(path + "check_04.png"))
        self.sprites.append(pygame.image.load(path + "check_05.png"))
        self.sprites.append(pygame.image.load(path + "check_06.png"))
        self.sprites.append(pygame.image.load(path + "check_07.png"))
        self.sprites.append(pygame.image.load(path + "check_08.png"))
        self.sprites.append(pygame.image.load(path + "check_09.png"))
        self.sprites.append(pygame.image.load(path + "check_10.png"))
        self.sprites.append(pygame.image.load(path + "check_11.png"))
        self.sprites.append(pygame.image.load(path + "check_12.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        self.X = utils.width / 2
        self.Y = utils.height / 2
        self.rect = self.image.get_rect(center=(self.X, self.Y))

    def animate(self):
        """
        This function is called to animate
        the checkmark.
        """
        self.stage += 0.6
        if self.stage > 12:
            self.stage = 12
            utils.done_setup = True

    def update(self):
        """
        This function handles the checkmark animation.
        """
        self.image = self.sprites[int(self.stage)]