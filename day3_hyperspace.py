"""
Genuary2022 Day 3 Space
Hyperspace ride by C. Ponsard
loosely based on  Silveira Neto <me@silveiraneto.net>
http://silveiraneto.net/2009/08/12/pygame-simple-space-effect/
Free under the terms of GPLv3 license
"""

import os, sys, random
import pygame
from pygame.locals import *

# Constants
N = 500
SCREEN_W, SCREEN_H = (640, 480)

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
    pygame.display.set_caption('Genuary2022 - DAY3 - Into HyperSpace by C.Ponsard - PRESS SPACE')
    ox = SCREEN_W//2
    oy = SCREEN_H//2
    s = 0

    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    # generate N stars
    stars = [
        [random.uniform(0, SCREEN_W), random.uniform(0, SCREEN_H)]
        for x in range(N)
    ]

    # main loop
    i = 0
    n = 0
    mox = 0
    moy = 0
    STEPS = 25
    MAX = 5
    start = False

    clock = pygame.time.Clock()
    while 1:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                start = True

        if start:
            i = i+1
            p = (i % STEPS)
            n = i // STEPS
            # accelerating
            if (n == 0) and (p < STEPS):
                s = s + 0.01
            # decelerating
            if (n >= MAX) and (s>0):
                s = s - 0.0025
            # change direction
            if (p == 0) and (n <= MAX):
                if (n == MAX):
                    print("CENTERING ")
                    mox = (SCREEN_W/2-ox)/STEPS/4
                    moy = (SCREEN_H/2-oy)/STEPS/4
                else:
                    mox = (random.uniform(100,SCREEN_W)-ox)/STEPS
                    moy = (random.uniform(100,SCREEN_H)-oy)/STEPS
            if (s < 0):
                print("STOPPING")
                mox = 0
                moy = 0
                s = 0.0
            ox = ox+mox
            oy = oy+moy

        background.fill((0, 0, 0))
        for star in stars:
            x1=star[0]
            y1=star[1]
            vx=x1-ox
            vy=y1-oy
            x2=x1+vx*s
            y2=y1+vy*s
            pygame.draw.line(background,(255, 255, 255), (x1,y1), (x2,y2))
            if in_screen(x2,y2):
                star[0]=x2
                star[1]=y2
            else:
                star[0]=random.uniform(ox-100,ox+100)
                star[1] = random.uniform(oy-100,oy+100)
        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == '__main__': main()