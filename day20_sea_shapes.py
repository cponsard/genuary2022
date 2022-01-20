"""
Genuary2022 Day 20 Sea of Shapes
More shapes of seas by C. Ponsard
Free under the terms of GPLv3 license
"""

import os, sys, random
import pygame
from pygame.locals import *
from perlin_noise import PerlinNoise
import time
import math

# Constants
N = 15
M = 200
SCREEN_W, SCREEN_H = (800, 600)
MAX_DEPC = 800
MAX_DEPT = 5000
FPS = 30
SCROLL = 5

def remap(val, o1, o2, d1, d2):
    return (val - o1) / (o2 - o1) * (d2 - d1) + d1

class Specie():
    """
    Creature Specie
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

    def __init__(self, tSize, step, sca):
        self.create(tSize, step, sca)

    def create(self, size, step, sca):
        img = pygame.Surface((size,size),pygame.SRCALPHA)  # TODO check step
        noise = PerlinNoise(seed=time.time())
        xmin = size
        ymin = size
        xmax = 0
        ymax = 0

        for i in range(0, size, step):
#            print(i)
            for j in range(0, size, step):
                x = int(remap(noise([i * sca, j * sca]), -1.0, 1.0, 0, size))
                y = int(remap(noise([j * sca, i * sca]), -1.0, 1.0, 0, size))
#                print(str(x)+" "+str(y)+" "+str(noise([i * sca, j * sca])))
                if (x<0) or (y<0) or (x>=size) or (y>=size): continue
                r,g,b, _ = img.get_at((x,y))
                if (r==0): r=100
                else: r += 20
                if (r>255): r=255
                if (g==0): g=100
                else: g += 20
                if (g>255): g=255
                if (b==0): b=100
                else: b += 20
                if (b>255): b=255
                img.set_at((x,y),(r,g,b))

                if (x<xmin): xmin=x
                if (y<ymin): ymin=y
                if (x>xmax): xmax=x
                if (y>ymax): ymax=y
        z=size/(xmax-xmin)
#        print("ZOOM "+str(z))
#        print(str(self.xmax)+" "+str(self.xmin))
#        print(str(self.ymax)+" "+str(self.ymin))
#        img.blit(img,(-self.xmin,-self.ymin))
        self.img = pygame.Surface((xmax-xmin,ymax-ymin),pygame.SRCALPHA)
        self.img.blit(img,(-xmin,-ymin))
#        self.img = img

class Creature():
    """
    Creature Instance
    """

    specie = None
    px = 0
    py = 0
    a  = 0
    z  = 0
    img = None

    def __init__(self, specie, px, py, a, z, col):
        self.specie = specie
        self.px = px
        self.py = py
        self.a  = a
        self.z  = z
        self.random_speed()
        mask = pygame.Surface(self.specie.img.get_size()).convert_alpha()
        mask.fill(col)
        self.img = pygame.Surface.copy(specie.img)
        self.img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def random_speed(self):
        v = random.uniform(0.5,2)
        ar = (self.a+45)/180*math.pi
        self.dx = v * math.sin(ar)
        self.dy = v * math.cos(ar)

    def draw(self, screen):
        screen.blit(pygame.transform.rotozoom(self.img,self.a,self.z), (int(self.px), int(self.py)))

    def update(self,scroll):
        self.px = self.px+self.dx
        self.py = self.py+self.dy-scroll
#        if (self.px<0) or (self.px>SCREEN_W-self.specie.img.get_width()):
#            self.dx = -self.dx
#        if (self.py<0) or (self.py>SCREEN_H-self.specie.img.get_height()):
#            self.dy = -self.dy

    def in_screen(self):
        if self.px<-0: return False
        if self.py<-0: return False
        if self.px>SCREEN_W-self.specie.img.get_width(): return False
        if self.py>SCREEN_H-self.specie.img.get_height(): return False
        return True

def get_col(y):
    r = y / MAX_DEPT * 170 + random.randint(0,75)
    g = (MAX_DEPT - y) / MAX_DEPT * 170 + random.randint(0,75)
    b = random.randint(0,100)
    return (r,g,b)

def print_gauge(screen, font, dept):
    dd = (dept//100)*100
    for d in range(dd, dd+SCREEN_H+200,100):
        text = font.render("-"+str(d//10), False, (150, 150, 150))
        screen.blit(text, (0, d-dept))

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY20 - Sea of Shapes (of Sea) by C.Ponsard')

    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((20,20,255))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # load font
    font = pygame.font.SysFont('Courrier New', 40)

    # species
    specie = []
    for i in range(N):
        print("CREATE SPECIE#"+str(i))
        specie.append(Specie(150, 3, 0.01))

    # surface creatures
    creature = []
    for i in range(M):
        x = random.randint(-50,SCREEN_W)
        y = random.randint(0,SCREEN_H+200)
        t = random.randint(0,int(i/M*8))
        a = random.uniform(0,360)
        z = random.uniform(0.3,1.0)
        col = get_col(y)
        creature.append(Creature(specie[t],x,y,a,z,col))

    i = 0
    clock = pygame.time.Clock()
    fps = FPS
    while 1:
        print(i)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        dept = i

        # background going to black
        col = (0,0,0)
        if (dept<MAX_DEPC):
            f = 1.0-(dept/MAX_DEPC)
            col = (int(20*f),int(20*f),int(255*f))
#        print(col)
        background.fill(col)
        screen.blit(background, (0, 0))

        for c in range(M):
            creature[c].draw(screen)
            if dept < MAX_DEPT:
                creature[c].update(SCROLL)
            else:
                creature[c].update(0)
            if (creature[c].py < -20):
                x = random.randint(-50, SCREEN_W)
                y = random.randint(SCREEN_H, SCREEN_H + 100)
                t = random.randint(int(dept*N / MAX_DEPT) - 2, int(dept*N / MAX_DEPT) + 2)
                print("TYPE "+str(t))
                if (t < 0): t = 0
                if (t >= N): t = N - 1
                a = random.uniform(0, 360)
                if (dept<2000):
                    z = random.uniform(0.3, 1.2)
                elif (dept<3500):
                    z = random.uniform(0.2, 1.0)
                else:
                    z = random.uniform(0.1, 0.8)

                col = get_col(dept)
                creature[c] = Creature(specie[t], x, y, a, z, col)

        # adding bubbles ?

        # dept gauge
        print_gauge(screen, font, dept)

        # display
        pygame.display.flip()

        # next step
        if dept<MAX_DEPT:
            i += SCROLL
            if (dept>MAX_DEPT-200):
                fps -= 0.2

        clock.tick(int(fps))
        print(int(fps))

if __name__ == '__main__': main()