"""
Genuary2022 Day 10 Wrong AI
Terminator revisited by C. Ponsard
Free under the terms of GPLv3 license
"""
import pygame
from pygame.locals import *

SCREEN_W, SCREEN_H = (800, 450)

def filter(surface, cr, cg, cb):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            r, g, b, _ = surface.get_at((x, y))
            r = (int)(r*cr)
            if r>255: r=255
            g = (int)(g*cg)
            if g>255: g=255
            b = (int)(b*cb)
            if r>255: r=255
            surface.set_at((x, y), Color(r,g,b))

def print_listing(screen,listing, font, d, n):
    for i in range(0, n):
        text = font.render(listing[(i+d) % len(listing)], False, (255, 255, 255))
        screen.blit(text, (0, i*16+50))

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY7 - Sol Lewitt by C.Ponsard - PRESS SPACE for new Sol Lewitt')

    f = open("day6_listing.txt", "r")
    listing = f.read()
    lines = listing.splitlines()
    myfont = pygame.font.SysFont('Courrier New', 18)

    # image.set_alpha(128)

    john = pygame.image.load('day6_john.jpg')
    john = pygame.transform.rotozoom(john, 0.0, SCREEN_W/john.get_width())
    filter(john,0.6,0.1,0.1)

    i = 0
    clock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        screen.blit(john, (0, 0))
        print_listing(screen,lines,myfont,i,20)
        i += 1

        pygame.display.flip()
        clock.tick(15)

if __name__ == '__main__': main()
