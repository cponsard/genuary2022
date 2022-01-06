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

def in_screen(x,y):
    if x<-200: return False
    if y<-200: return False
    if x>SCREEN_W+200: return False
    if y>SCREEN_H+200: return False
    return True

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY6 - Trade Style With a Friend by C.Ponsard')

    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    mask = pygame.image.load('day6_mask.png').convert_alpha()
    ghosts = []
    ghosts.append(pygame.image.load('day6_blinky.png').convert_alpha())
    ghosts.append(pygame.image.load('day6_clyde.png').convert_alpha())
    ghosts.append(pygame.image.load('day6_inky.png').convert_alpha())
    ghosts.append(pygame.image.load('day6_pinky.png').convert_alpha())

    clock = pygame.time.Clock()
    while 1:
        clock.tick(1)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for i in range(4):
            g = ghosts[i]
            w = g.get_width()
            h = g.get_height()
            x = random.randint(0,SCREEN_W-w)
            y = random.randint(0,SCREEN_H-h)
            screen.blit(g,(x,y))

        screen.blit(mask, (0,0))
        pygame.display.flip()


if __name__ == '__main__': main()