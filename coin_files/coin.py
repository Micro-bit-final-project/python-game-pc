import pygame, os, utils
from random import randint

class Coin(pygame.sprite.Sprite):
    """
    This class handles the coin sprite
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
        self.sprites.append(pygame.image.load(path + "coin_00.png"))
        self.sprites.append(pygame.image.load(path + "coin_01.png"))
        self.sprites.append(pygame.image.load(path + "coin_02.png"))
        self.sprites.append(pygame.image.load(path + "coin_03.png"))
        self.sprites.append(pygame.image.load(path + "coin_04.png"))
        self.sprites.append(pygame.image.load(path + "coin_05.png"))
        self.sprites.append(pygame.image.load(path + "coin_06.png"))
        self.sprites.append(pygame.image.load(path + "coin_07.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        # Coordinates, change as needed
        self.X = randint(50, utils.width - 50)
        self.Y = -320 / 2 # 320 is the sprite's height
        self.rect = self.image.get_rect(center=(self.X, self.Y))
        self.bucket_rect = 0

        # Sound effect
        self.coin_sound = pygame.mixer.Sound(path + "coin.ogg")

    def animate(self, bucket_rect):
        """
        This function is called to animate
        the sprite.
        """
        self.stage += 0.25
        if self.stage > 7:
            self.stage = 0

        self.bucket_rect = bucket_rect

    def update(self):
        """
        This function handles the sprite animation.
        """
        self.image = self.sprites[int(self.stage)]

        self.Y += 3.5
        self.rect = self.image.get_rect(center=(self.X, self.Y))
        if self.rect.colliderect(self.bucket_rect) == True:
            pygame.mixer.Sound.play(self.coin_sound)
            self.Y = -320 / 2 # 320 is the sprite's height
            self.X = randint(50, utils.width - 50)
            utils.points += 1
        elif self.Y > utils.height:
            self.Y = -320 / 2 # 320 is the sprite's height
            self.X = randint(50, utils.width - 50)