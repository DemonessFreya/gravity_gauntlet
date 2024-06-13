#***********************************************
"""
gravity_gauntlet.py - final revision of main file
Author: Freya Marika
github: https://github.com/DemonessFreya/gravity_gauntlet

Date: 12/06/2024 - 14/06/2024

Sources used: https://realpython.com/pygame-a-primer/ ; https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_jump.md ; https://stackoverflow.com/questions/78615856/how-to-make-my-sprite-go-back-to-its-original-frame-after-changing-in-pygame/78615910#78615910 ; https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
"""
#***********************************************

# Import the pygame module
import pygame
import pygame.freetype # import freetype for ui elements
from enum import Enum # import Enum for button pressed event

import Sprites # imports the Sprites.py file


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    QUIT,
)

# Constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# colour definitions using RGB
BLACK = (15, 15, 15)
GREY = (20, 20, 20)
VIOLET = (92, 22, 137)
WHITE = (255, 255, 255)

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Gauntlet")


# Create custom events and the time between each for adding a new enemy and a PLANET
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


# **************************************************************************************
# defines ui elements for the start and death screens
def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(pygame.sprite.Sprite):
    # An user interface element that can be added to a surface

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        # calls the init method of the parent sprite class
        super().__init__()
        self.action = action
    
    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    
    def update(self, mouse_pos, mouse_up):
        # Updates the element's appearance depending on the mouse position and returns the button's action if clicked.
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        # Draws element onto a surface
        surface.blit(self.image, self.rect)

class ButtonState(Enum):
    PRESSED = True # when buttton pressed

# UI ELEMENTS
# start button
start_btn = UIElement(
    center_position=(400, 200),
    font_size=30,
    bg_rgb=VIOLET,
    text_rgb=WHITE,
    text="Gravity Gauntlet",
    action=ButtonState.PRESSED,
)

# quit button
quit_btn = UIElement(
    center_position=(400, 500),
    font_size=30,
    bg_rgb=VIOLET,
    text_rgb=WHITE,
    text="Quit",
    action=ButtonState.PRESSED,
)

# button when you die
dead_btn = UIElement(
    center_position=(400, 200),
    font_size=30,
    bg_rgb=VIOLET,
    text_rgb=WHITE,
    text="You Died",
    action=ButtonState.PRESSED,
)
# **************************************************************************************


# Variable for each loop Boolean
app_running = True
game_running = False
is_dead = False


# main main loop
while app_running:
    # defines button pressing
    mouse_up = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_up = True
    screen.fill(VIOLET) # background colour

    # performs a function if button clicked
    start_ui_action = start_btn.update(pygame.mouse.get_pos(), mouse_up)
    if start_ui_action:
        game_running = True
    start_btn.draw(screen)

    # performs a function if button clicked
    quit_ui_action = quit_btn.update(pygame.mouse.get_pos(), mouse_up)
    if quit_ui_action:
        app_running = False
    quit_btn.draw(screen)

    # render screen
    pygame.display.flip()

    # quit app if quit
    if pygame.event.get(eventtype=QUIT):
        app_running = False

    # game loop
    while game_running:
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                game_running = False
                app_running = False

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

        # Fill the screen with sky VIOLET
        screen.fill(BLACK)

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # circle representing a planet
        pygame.draw.circle(screen, GREY, (SCREEN_WIDTH / 2, SCREEN_HEIGHT + 1400), 1500.0)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then stop the loop
            #player.kill()
            game_running = False
            is_dead = True

        # render everything
        pygame.display.flip()

        # Ensure program maintains a rate of 60 frames per second
        clock.tick(60)

    # end screen loop
    while is_dead:
        # defines button pressing
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(VIOLET)

        # performs a function if button clicked
        dead_ui_action = dead_btn.update(pygame.mouse.get_pos(), mouse_up)
        if dead_ui_action:
            is_dead = False
            game_running = True
        dead_btn.draw(screen)

        # performs a function if button clicked
        quit_ui_action = quit_btn.update(pygame.mouse.get_pos(), mouse_up)
        if quit_ui_action:
            is_dead = False
            app_running = False
        quit_btn.draw(screen)

        for event in pygame.event.get():
            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                is_dead = False
                app_running = False

        pygame.display.flip() # render
