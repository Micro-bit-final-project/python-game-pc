import pygame, os, utils
from pathlib import Path

class Backgrounds(pygame.sprite.Sprite):
    """
    This class handles the background sprites
    in the main menu and their animation.
    """
    def __init__(self, root, shade):
        """
        This function initialises the sprite by loading
        all the needed sprites for the animation and
        by generating the relative rect.
        """
        super().__init__()
        path = root + utils.sep
        
        self.shade = shade

        self.sprites = [] # Array containing all the sprites for animation.
        paths = list(Path(root).rglob("background.png")) # Find all the background images in subdirs
        for f in paths:
            self.sprites.append(pygame.image.load(str(f))) # Append all the background images

        self.stage = 0
        self.image = self.sprites[self.stage]
        # Coordinates, change as needed
        self.X = utils.width / 2
        self.Y = utils.height / 2
        self.rect = self.image.get_rect(center=(self.X, self.Y))

    def animate(self):
        """
        This function is called to animate
        the sprite.
        """
        self.stage += 0.01
        if self.stage > len(self.sprites):
            self.stage = 0
        utils.stage = self.stage

    def update(self):
        """
        This function handles the sprite animation.
        """
        self.image = self.sprites[int(self.stage)]