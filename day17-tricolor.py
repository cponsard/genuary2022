"""
Genuary2022 Day 17 3 colors
Swipers by C. Ponsard
Free under the terms of GPLv3 license
"""

import random

import pygame
from pygame.locals import *

SCREEN_W, SCREEN_H = (800, 500)

SKY = (30, 30, 180)
WIPER = (0,0,0)
WIPER_W = SCREEN_W/2+130
WIPER_H = 10
DROP = (100, 100, 200)
MIN = 3
MAX = 8
N = 3

def generate_sky(screen,col):
    img = pygame.Surface(screen.get_size())
    img = img.convert()
    img.fill(col)
    return img

def generate_wiper(screen,col,w,h):
    img = pygame.Surface((w,h))
    img = img.convert_alpha()
    img.fill(col)
    return img

def add_drop(screen, col):
    for i in range(N):
        x = random.randint(0,screen.get_width())
        y = random.randint(0,screen.get_height())
        r = random.randint(MIN,MAX)
        pygame.draw.circle(screen, col, (x,y), r)

def add_spot(screen, spot):
    if random.randint(0, 20) == 0:
        x = random.randint(0,screen.get_width())
        y = random.randint(0,screen.get_height())
        r = random.uniform(0.0,360.0)
        z = random.uniform(0.2,0.5)
        img = pygame.transform.rotozoom(spot, r, z)
        screen.blit(img, (x,y))

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY17 - 3 Colors by C.Ponsard')

    clock = pygame.time.Clock()
    sky = generate_sky(screen, SKY)

    wiper_fg = generate_wiper(screen, WIPER, WIPER_W, WIPER_H)
    wiper_bg = generate_wiper(screen, SKY,  WIPER_W, WIPER_H)

    spot = pygame.image.load('day17_spot.png').convert_alpha()
    i = 0

    while 1:
        add_drop(sky, DROP)
        add_spot(sky, spot)
        angle = i % 180
        if (angle>90): angle = 180-angle
        img_fg = pygame.transform.rotate(wiper_fg, angle)
        img_bg = pygame.transform.rotate(wiper_bg, angle)
        sky.blit(img_bg, (0,SCREEN_H-img_bg.get_height()))
        sky.blit(img_bg, (SCREEN_W/2 ,SCREEN_H-img_bg.get_height()))
        screen.blit(sky, (0, 0))
        screen.blit(img_fg, (0,SCREEN_H-img_fg.get_height()))
        screen.blit(img_fg, (SCREEN_W/2,SCREEN_H-img_fg.get_height()))
        pygame.display.flip()
        i = i+1
        clock.tick(100)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

if __name__ == '__main__': main()
