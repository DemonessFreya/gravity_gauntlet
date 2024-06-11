#***********************************************
"""
gravity_gauntlet1.11.py - revision 1 of main file
Author: Freya Marika

Date: 5/06/2024 - 14/06/2024
"""
#***********************************************

import pygame
from pygame.locals import USEREVENT
import os
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Gauntlet")

bg = pygame.image.load("Sprites/Tilemap/tilemap-backgrounds_packed.png").convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = pygame.image.load("Sprites/Tiles/Characters/tile_0002.png").convert()
    jump = pygame.image.load("Sprites/Tiles/Characters/tile_0003.png").convert()
    fall = pygame.image.load("Sprites/Tiles/Characters/tile_0003.png").convert()
    #jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.falling = False
        self.jumpCount = 0
        self.runCount = 0

    def draw(self, screen):
        if self.falling:
            screen.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            #self.y -= self.jumpList[self.jumpCount] * 1.3
            screen.blit(self.jump, (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)

        else:
            if self.runCount > 42:
                self.runCount = 0
            screen.blit(self.run, (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-13)

        #pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)

class saw(object):
    rotate = [pygame.image.load("Sprites/Planets/planet07.png").convert(), pygame.image.load("Sprites/Planets/planet07.png").convert(), pygame.image.load("Sprites/Planets/planet07.png").convert(), pygame.image.load("Sprites/Planets/planet07.png").convert()]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self, screen):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)
        # pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        screen.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))
        self.rotateCount += 1

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class spike(saw):
    img = pygame.image.load("Sprites/Planets/planet07.png").convert()

    def draw(self, screen):
        self.hitbox = (self.x + 10, self.y, 28,315)
        # pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        screen.blit(self.img, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last



def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 60
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.jumping = False

        screen.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        screen.blit(lastScore, (SCREEN_WIDTH/2 - lastScore.get_width()/2,150))
        screen.blit(currentScore, (SCREEN_WIDTH/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0

def redrawscreendow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    screen.blit(bg, (bgX, 0))
    screen.blit(bg, (bgX2,0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    runner.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    screen.blit(text, (700, 10))
    pygame.display.update()


pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT + 2, 3000)
speed = 60

score = 0

run = True
runner = player(200, 313, 64, 64)

obstacles = []
pause = 0
fallSpeed = 0

while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = speed//10 - 3

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            runner.falling = True

            if pause == 0:
                pause = 1
                fallSpeed = speed
        if obstacle.x < -64:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.4

    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

        if event.type == USEREVENT+1:
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
            elif r == 1:
                obstacles.append(spike(810, 0, 48, 310))

    if runner.falling == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(runner.jumping):
                runner.jumping = True


    clock.tick(speed)
    redrawscreendow()
