#***********************************************
"""
gravity_gauntlet.py - final revision of main file
Author: Freya Marika
github: https://github.com/DemonessFreya/gravity_gauntlet

Date: 12/06/2024 - 14/06/2024

Sources used: https://realpython.com/pygame-a-primer/ ; https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_jump.md
"""
#***********************************************

# Import the pygame module
import pygame
import Sprites # imports the Sprites.py file


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    K_ESCAPE,
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


# Create custom events for adding a new enemy and a PLANET
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDPLANET = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANET, 1000)

# Instantiate player as a rectangle.
player = Sprites.Player()

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
            new_enemy = Sprites.Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
        # Add a new PLANET?
        elif event.type == ADDPLANET:
            # Create the new PLANET and add it to sprite groups
            new_planet = Sprites.Planet()
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

    # Flip everything and send it to the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)
