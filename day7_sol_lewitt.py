import random

import pygame
from pygame.locals import *

SCREEN_W, SCREEN_H = (1000, 800)
BORDER = 20
N1 = 50
N2 = 20

def generate_118(screen):
    art = pygame.Surface(screen.get_size())
    art = art.convert()
    art.fill((255, 255, 255))

    pt = []
    for i in range(N1):
        x = random.randint(BORDER, SCREEN_W-BORDER)
        y = random.randint(BORDER, SCREEN_H-BORDER)
        pt.append((x,y))

    for i in range(N1):
        for j in range(N1):
            pygame.draw.line(art, (40,40,40), pt[i], pt[j])

    return art

def generate_273(screen):
    art = pygame.Surface(screen.get_size())
    art = art.convert()
    art.fill((255, 255, 255))

    ptc = [(0,0),(0,SCREEN_H),(SCREEN_W,0),(SCREEN_W,SCREEN_H)]
    ptm = [(SCREEN_W//2,0),(0,SCREEN_H//2),(SCREEN_W,SCREEN_H//2),(SCREEN_W//2,SCREEN_H)]

    red = (200,0,0)
    yellow = (255,233,0)
    blue = (0,0,200)

    pt = []
    for i in range(N2):
        x = random.randint(BORDER, SCREEN_W-BORDER)
        y = random.randint(BORDER, SCREEN_H-BORDER)
        pt.append((x,y))

    for i in range(N2):
        for j in range(i,N2):
            pygame.draw.line(art, yellow, pt[i],pt[j])

    for i in range(4):
        for j in range(1, N2):
            pygame.draw.line(art, blue, ptc[i], pt[j])

    for i in range(4):
        for j in range(1, N2):
            pygame.draw.line(art, red, ptm[i], pt[j])

    return art


def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY7 - Sol Lewitt by C.Ponsard - PRESS SPACE for new Sol Lewitt')

    clock = pygame.time.Clock()
    drawing = generate_118(screen)
    i = 0

    while 1:
        screen.blit(drawing, (0, 0))
        pygame.display.flip()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                i += 1
                if i % 2:
                    drawing = generate_273(screen)
                else:
                    drawing = generate_118(screen)

if __name__ == '__main__': main()
