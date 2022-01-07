"""
Genuary2022 Day 6 Trade Style
Ghosts revisited in retro PacMan mode  by C. Ponsard
Free under the terms of GPLv3 license
"""

import os, sys, random
import pygame
from pygame.locals import *

# Constants
N = 10
SCREEN_W, SCREEN_H = (800, 800)
GHOSTS = []

class Ghost():
    """ Breakout Sprite class that extends following classes

        Attributes:
            image_file (str): Sprite-image filename.
    """

    type = 0
    px = SCREEN_W//2
    py = SCREEN_H//2
    dx = 0
    dy = 0
    w = 0
    h = 0
    z = 1.0
    img = None

    def __init__(self, type):
        self.type = type
        self.z = random.uniform(0.15,0.85)
        self.img = pygame.transform.rotozoom(GHOSTS[self.type],0.0, self.z)
        self.random_pos()
        self.random_speed()

    def random_pos(self):
        self.px = random.randint(0,SCREEN_W-self.img.get_width())
        self.py = random.randint(0,SCREEN_H-self.img.get_height())

    def random_speed(self):
        self.dx = random.uniform(0.5,2)
        self.dy = random.uniform(0.5,2)

    def draw(self, screen):
        screen.blit(self.img, (int(self.px), int(self.py)))

    def update(self):
        self.px = self.px+self.dx
        self.py = self.py+self.dy
        if (self.px<0) or (self.px>SCREEN_W-self.img.get_width()):
            self.dx = -self.dx
        if (self.py<0) or (self.py>SCREEN_H-self.img.get_height()):
            self.dy = -self.dy

    def in_screen(self):
        if self.px<-0: return False
        if self.py<-0: return False
        if self.px>SCREEN_W-self.img.get_width(): return False
        if self.py>SCREEN_H-self.img.get_height(): return False
        return True

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY6 - Trade Style With a Friend by C.Ponsard')

    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    # load ghosts types
    GHOSTS.append(pygame.image.load('day6_blinky.png').convert_alpha())
    GHOSTS.append(pygame.image.load('day6_clyde.png').convert_alpha())
    GHOSTS.append(pygame.image.load('day6_inky.png').convert_alpha())
    GHOSTS.append(pygame.image.load('day6_pinky.png').convert_alpha())
    GHOSTS.append(pygame.image.load('day6_afraid.png').convert_alpha())

    mask = pygame.image.load('day6_mask.png').convert_alpha()
    ghosts = []
    for i in range(N):
        ghosts.append(Ghost(i % len(GHOSTS))) #random.randint(0, len(GHOSTS)-1)

    clock = pygame.time.Clock()
    while 1:
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for i in range(N):
            ghosts[i].draw(screen)
            ghosts[i].update()

        screen.blit(mask, (0,0))
        pygame.display.flip()


if __name__ == '__main__': main()