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
        self.Y = utils.height - 120 # -120 makes it look good on the ground
        self.rect = self.image.get_rect(center=(self.X, self.Y))
        
        self.dino_rect = 0
        self.collision = False

    def animate(self, dino_rect):
        """
        This function is called to animate
        the sprite.
        """
        self.dino_rect = dino_rect
        self.stage += 0.15
        if self.stage > 3:
            self.stage = 0

    def update(self):
        """
        This function handles the sprite animation.
        """
        self.image = self.sprites[int(self.stage)]
        self.X -= 7

        if self.X < 0:
            self.X = utils.width
            if self.collision == False:
                utils.points += 2
            elif self.collision == True and utils.points >= 2:
                utils.points -= 2
            self.collision = False

        self.rect = self.image.get_rect(center=(self.X, self.Y))
        if self.rect.colliderect(self.dino_rect) == True:
            self.collision = True