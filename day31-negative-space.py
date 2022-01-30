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
SCREEN_W, SCREEN_H = (1100, 400)
GHOSTS1 = []
GHOSTS2 = []
CUT = 25

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
    img1 = None
    img2 = None

    def __init__(self, type):
        self.type = type
        self.z = random.uniform(0.10,0.25)
        self.img1 = pygame.transform.rotozoom(GHOSTS1[self.type],0.0, self.z)
        self.img2 = pygame.transform.rotozoom(GHOSTS2[self.type],0.0, self.z)
        self.random_pos()
        self.random_speed()

    def random_pos(self):
        self.px = random.randint(0,SCREEN_W-self.img1.get_width())
        self.py = random.randint(0,SCREEN_H-self.img1.get_height())

    def random_speed(self):
        self.dx = random.uniform(0.5,2)
        self.dy = random.uniform(0.5,2)

    def draw(self, screen):
        screen.blit(self.img1, (int(self.px), int(self.py)), None, BLEND_RGBA_ADD)
#        screen.blit(self.img2, (int(self.px), int(self.py)), None, BLEND_RGB_MULT)
        shadow(screen, self.img2, int(self.px), int(self.py))

    def update(self):
        self.px = self.px+self.dx
        self.py = self.py+self.dy
        if (self.px<0) or (self.px>SCREEN_W-self.img1.get_width()):
            self.dx = -self.dx
        if (self.py<0) or (self.py>SCREEN_H-self.img1.get_height()):
            self.dy = -self.dy

    def in_screen(self):
        if self.px<-0: return False
        if self.py<-0: return False
        if self.px>SCREEN_W-self.img.get_width(): return False
        if self.py>SCREEN_H-self.img.get_height(): return False
        return True

def shadow(screen, img, xs, ys):
    ws,hs = screen.get_size()
    w,h = img.get_size()
    for x in range(w):
        if xs<0: continue
        if xs+x>=ws: continue
        for y in range(h):
            if ys<0: continue
            if ys+y>=hs: continue
            p=(xs+x,ys+y)
            r,g,b,_ = screen.get_at(p)
            if (r==255) and (g==255) and (b==255):
                screen.set_at(p,img.get_at((x,y)))

def gen_char(text,screen,font,x,y,neg):
    if neg:
        text = font.render(text, False, (255, 255, 255))
        w,h=text.get_size()
        bg = pygame.Surface((w-2*CUT,h-CUT))
        bg.fill((0, 0, 0))
        screen.blit(bg, (x+CUT, y))
        screen.blit(text, (x, y))
    else:
        text = font.render(text, False, (0, 0, 0))
        screen.blit(text, (x,y))

def generate(text,screen,font,x,y):
    delta = 0
    neg = False
    for i in range(len(text)):
        gen_char(text[i],screen,font,x+delta,y,neg)
        delta += font.size(text[i])[0]-2*CUT
        neg = not(neg)

def convert(img):
    res = pygame.Surface.copy(img)
    w,h = res.get_size()
    for x in range(w):
        for y in range(h):
            r,g,b,a = res.get_at((x,y))
#            print(str(r)+" "+str(g)+" "+str(b)+" "+str(a))
            if (a==255):
                res.set_at((x,y),(0,0,0,0))
            elif (r==255) and (g==255) and (b==255):
                res.set_at((x,y),(255,255,128,0))
            else:
                res.set_at((x,y),(255,255,255,0))
    return res

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY6 - Trade Style With a Friend by C.Ponsard')

    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()

    # load ghosts types
    GHOSTS1.append(pygame.image.load('day6_blinky.png').convert_alpha())
    GHOSTS1.append(pygame.image.load('day6_clyde.png').convert_alpha())
    GHOSTS1.append(pygame.image.load('day6_inky.png').convert_alpha())
    GHOSTS1.append(pygame.image.load('day6_pinky.png').convert_alpha())
    GHOSTS1.append(pygame.image.load('day6_afraid.png').convert_alpha())

    #convert
    for i in range(len(GHOSTS1)):
        GHOSTS2.append(convert(GHOSTS1[i]))

    # font
    font = pygame.font.SysFont('C64 Pro Mono', 200) # C64 Pro Mono

    ghosts = []
    for i in range(N):
        ghosts.append(Ghost(i % len(GHOSTS1))) #random.randint(0, len(GHOSTS)-1)

    clock = pygame.time.Clock()
    while 1:
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        background.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        generate("GENUARY",screen,font,20-CUT,100)

        for i in range(N):
            ghosts[i].draw(screen)
            ghosts[i].update()

        pygame.display.flip()


if __name__ == '__main__': main()