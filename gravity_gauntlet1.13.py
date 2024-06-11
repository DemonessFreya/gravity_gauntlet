#***********************************************
"""
gravity_gauntlet1.13.py - revision 3 of main file
Author: Freya Marika

Date: 11/06/2024 - 14/06/2024
"""
#***********************************************

# Import pygame and random module
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
    K_SPACE,
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

# Create window object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Gauntlet")


rect = pygame.Rect(135, 220, 30, 30) 
velocity = 5
jump = False
jumpCount = 0
jumpMax = 15

run = True
while run:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: 
            if not jump and event.key == pygame.K_SPACE:
                jump = True
                jumpCount = jumpMax

    keys = pygame.key.get_pressed()    
    rect.centerx = (rect.centerx + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * velocity) % 300
    
    if jump:
        rect.y -= jumpCount
        if jumpCount > -jumpMax:
            jumpCount -= 1
        else:
            jump = False 

    window.fill((0, 0, 64))
    pygame.draw.rect(window, (64, 64, 64), (0, 250, 300, 100))
    pygame.draw.circle(window, (255, 0, 0), rect.center, 15)
    pygame.display.flip()

pygame.quit()
exit()
