import pygame
import random


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT
)

# Constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define the Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # create the two different frames for the player sprite
        self.surf_horizontal = pygame.image.load("Sprites/Characters/tile_0002.png").convert() # load image
        self.surf_horizontal.set_colorkey((0, 0, 0), RLEACCEL) # set sprite colour
        self.surf_horizontal = pygame.transform.scale(self.surf_horizontal, [25, 25]) # scale image
        self.surf_vertical = pygame.image.load("Sprites/Characters/tile_0003.png").convert() # load image
        self.surf_vertical.set_colorkey((0, 0, 0), RLEACCEL) # set sprite colour
        self.surf_vertical = pygame.transform.scale(self.surf_vertical, [25, 25]) # scale image
        self.surf = self.surf_horizontal # set default sprite to the horizontal frame
        self.rect = self.surf.get_rect(center=(-SCREEN_WIDTH + 50, SCREEN_HEIGHT,))

    # when the sprite is going up or down, change the frame accordingly
    def change_image(self, image_type):
        if image_type == "vertical":
            self.surf = self.surf_vertical
        else:
            self.surf = self.surf_horizontal

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        image_type = "horizontal"
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            image_type = "vertical"
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            image_type = "vertical"
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        self.change_image(image_type)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 500:
            self.rect.bottom = 500

# Define the enemy object by extending pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("Sprites/Planets/planet06.png").convert() # load image
        self.surf.set_colorkey((0, 0, 0), RLEACCEL) # set sprite colour
        self.surf = pygame.transform.scale(self.surf, [20, 20]) # scale image
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            ) # randomise the start position for the enemy
        )
        self.speed = random.randint(5, 20) # randomises the speed of each enemy

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the PLANET object by extending pygame.sprite.Sprite
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super(Planet, self).__init__()
        self.surf = pygame.image.load("Sprites/Planets/planet08.png").convert() # load image
        self.surf.set_colorkey((0, 0, 0), RLEACCEL) # set sprite colour
        self.surf = pygame.transform.scale(self.surf, [50, 50]) # scale image
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            ) # the starting position is randomly generated
        )

    # Move the PLANET based on a constant speed
    # Remove the PLANET when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
