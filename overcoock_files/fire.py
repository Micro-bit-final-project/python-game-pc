import pygame, os, utils

class Fire(pygame.sprite.Sprite):
    """
    This class handles the fire sprite
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
        self.sprites.append(pygame.image.load(path + "fire_00.png"))
        self.sprites.append(pygame.image.load(path + "fire_01.png"))
        self.sprites.append(pygame.image.load(path + "fire_02.png"))
        self.sprites.append(pygame.image.load(path + "fire_03.png"))
        self.sprites.append(pygame.image.load(path + "fire_04.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        # Coordinates, change as needed
        self.X = utils.width / 2
        self.Y = (utils.height / 2) + 300
        self.rect = self.image.get_rect(center=(self.X, self.Y))

    def animate(self):
        """
        This function is called to animate
        the sprite.
        """
        self.stage += 0.05
        if self.stage > 4:
            self.stage = 0

    def update(self):
        """
        This function handles the sprite animation.
        """
        self.image = self.sprites[int(self.stage)]