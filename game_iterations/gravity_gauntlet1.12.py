#***********************************************
"""
gravity_gauntlet1.12.py - revision 2 of main file
Author: Freya Marika

Date: 5/06/2024 - 14/06/2024
"""
#***********************************************

# Import the pygame module
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
    K_RIGHT,
    K_ESCAPE,
    #K_SPACE,
    KEYDOWN,
    QUIT,
)

# Constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Gauntlet")


# Define the Player object by extending pygame.sprite.Sprite
# Instead of a surface, use an image for a better-looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Sprites/Tiles/Characters/tile_0002.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, [25, 25])
        self.rect = self.surf.get_rect(center=(
            -SCREEN_WIDTH + 50,
            SCREEN_HEIGHT,
        ))
        #self.pressJump = False

    # jump function
    """def jump(self):
        self.jumpCount = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10]

        #self.rect.move_ip(0, -10)

        for frame in self.jumpCount:
            if self.pressJump:
                self.rect.move_ip(0, -1)
            frame += 1"""

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            #self.pressJump = True
            #self.jump()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

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
# Instead of a surface, use an image for a better-looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("Sprites/Planets/planet06.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, [20, 20])
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the PLANET object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super(Planet, self).__init__()
        self.surf = pygame.image.load("Sprites/Planets/planet08.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, [50, 50])
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the PLANET based on a constant speed
    # Remove the PLANET when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super(Ground, self).__init__()
        self.surf = pygame.image.load("Sprites/Planets.planet05.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf, [25, 25])
        self.surf = pygame.Rect.center


# Create custom events for adding a new enemy and a PLANET
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDPLANET = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANET, 1000)
ADDGROUND = pygame.USEREVENT + 3
pygame.time.set_timer(ADDGROUND, 100)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites, PLANET sprites, and all sprites
# - enemies is used for collision detection and position updates
# - planets is used for position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
planets = pygame.sprite.Group()
ground = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
        # Add a new PLANET?
        elif event.type == ADDPLANET:
            # Create the new PLANET and add it to sprite groups
            new_planet = Planet()
            planets.add(new_planet)
            all_sprites.add(new_planet)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of enemies and PLANETs
    enemies.update()
    planets.update()

    # Fill the screen with sky blue
    screen.fill((15, 15, 15))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    #pygame.draw.rect(screen, (64, 64, 64), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    pygame.draw.circle(screen, (20, 20, 20), (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 1400), 1500.0)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    # Flip everything to the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)
