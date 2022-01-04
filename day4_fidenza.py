"""
Genuary2022 Day 4 Next Next Fidenza
Vector field ride by C. Ponsard
Free under the terms of GPLv3 license

Run and press space to start the design
"""

import os, sys, random
import pygame
from pygame.locals import *
import math

# Constants
SCREEN_W, SCREEN_H = (800, 600)
XMIN=-10.0
XMAX=10.0
YMIN=-10.0
YMAX=10.0
RX=XMAX-XMIN
RY=YMAX-YMIN
N = 50
STEP = 0.2

def in_range(x,y):
    if x<XMIN: return False
    if y<YMIN: return False
    if x>XMAX: return False
    if y>YMAX: return False
    return True

def in_screen(x,y):
    if x<0: return False
    if y<0: return False
    if x>=SCREEN_W: return False
    if y>=SCREEN_H: return False
    return True

def field_value(x,y):
    dx = x-y
    dy = x+y
    lg = math.sqrt(dx*dx+dy*dy)
    return (x-y,x+y,lg)

def conv(x,y):
    return(int((x-XMIN)/RX*SCREEN_W),int((y-YMIN)/RY*SCREEN_H))

def create_empty_field(screen):
    field = pygame.Surface(screen.get_size())
    field = field.convert()
    field.fill((255, 255, 255))
    return field

def create_vector_field(screen,n,m):
    field = pygame.Surface(screen.get_size())
    field = field.convert()
    field.fill((255, 255, 255))
    sx = RX/n
    sy = RY/m

    for i in range(n):
        for j in range(m):
            x = XMIN+i*sx
            y = YMIN+j*sy
            dx, dy, lg = field_value(x,y)
            if (lg==0): continue
            f = STEP/lg
            p1=conv(x-dx*f,y-dy*f)
            p2=conv(x+dx*f,y+dy*f)
            pygame.draw.line(field, (0, 0, 0), p1, p2)
    return field

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY4 - Next Next Fidenza by C.Ponsard - PRESS SPACE')

    # create vector field
    #field = create_vector_field(screen,N,N)
    field = create_empty_field(screen)

    # main loop
    i = 0
    n = 0
    cx = 0
    cy = 0
    cnx = 0
    cny = 0
    col = (0,0,0)

    clock = pygame.time.Clock()
    while 1:
        clock.tick(200)
        i = i + 1

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                start = True

        if n == 0:
            cx = random.uniform(XMIN,XMAX)
            cy = random.uniform(YMIN,YMAX)
            cr,cg,cb,ca=field.get_at(conv(cx,cy))
            if cr<255 or cg<255 or cb<255: continue
            n = random.randint(20,50)
            col = (random.randint(128,255),random.randint(128,255),random.randint(128,255))
            r = random.randint(5,10)
            step = r*RX/SCREEN_W
        else:
            n = n-1

        dx, dy, lg = field_value(cx,cy)
        f = step/lg
        cnx = cx + dx*f
        cny = cy + dy*f

        p=conv(cx,cy)
        pn=conv(cnx,cny)
        if not in_screen(pn[0],pn[1]):
            n = 0
        else:
            cr,cg,cb,ca = field.get_at(pn)
            if cr<255 or cg<255 or cb<255:
                n = 0

        # draw at the end
        pygame.draw.circle(field, col, p, r)

        # update
        cx=cnx
        cy=cny

        screen.blit(field, (0, 0))
        pygame.display.flip()

if __name__ == '__main__': main()