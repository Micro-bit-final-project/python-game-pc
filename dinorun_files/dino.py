import pygame, os, utils

class Dino(pygame.sprite.Sprite):
    """
    This class handles the dino sprite
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
        self.sprites.append(pygame.image.load(path + "dino_00.png"))
        self.sprites.append(pygame.image.load(path + "dino_01.png"))
        self.sprites.append(pygame.image.load(path + "dino_02.png"))
        self.sprites.append(pygame.image.load(path + "dino_03.png"))
        self.stage = 0
        self.image = self.sprites[self.stage]
        # Coordinates
        self.X = utils.width / 4
        self.Y = utils.height - 100 - 160 # 160 is the sprite's height
        self.rect = self.image.get_rect(center=(self.X, self.Y))

        self.jump_state = False
        self.jump_progression = 0
        self.jump_going_down = False

    def animate(self, jump):
        """
        This function is called to animate
        the sprite.
        """
        self.stage += 0.15
        if self.stage > 3:
            self.stage = 0
        if jump == True:
            if self.jump_state == False:
                self.jump_progression += 1
                self.jump_state = True

        if self.jump_state == True:
            if self.jump_progression < 300 and self.jump_going_down == False:
                self.jump_progression += 15
            else:
                self.jump_going_down = True
                self.jump_progression -= 5
                if self.jump_progression < 0:
                    self.jump_progression = 0
                    self.jump_state = False
                    self.jump_going_down = False

    def update(self):
        """
        This function handles the sprite animation.
        """
        self.image = self.sprites[int(self.stage)]
        self.rect = self.image.get_rect(center=(self.X, self.Y - self.jump_progression))