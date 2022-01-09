"""
Genuary2022 Day 10 Wrong AI
Terminator revisited by C. Ponsard
Free under the terms of GPLv3 license
"""
import pygame
import pygame.camera
from pygame.locals import *
from pygame import surfarray
import numpy as N
import math

SCREEN_W, SCREEN_H = (640, 480)

def filter(surface, cr=0.6, cg=0.1, cb=0.1):
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

def fast_filter(surface):
    rgbarray = surfarray.array3d(surface)
    redimg = N.array(rgbarray)
    redimg[:,:,1:] = 0
    redimg[:, :, :] += redimg[:, :, :]//2
    return redimg

def print_listing(screen,listing, font, d, n):
    for i in range(0, n):
        text = font.render(listing[(i+d) % len(listing)], False, (255, 255, 255))
        screen.blit(text, (0, i*16+50))

def print_status(screen, font, boom, i):
    d = (i//10) % 10
    if d == 0:
        text = "TARGET ACQUIRED"
    elif (i//5) % 2 == 0:
        text = ""
    else:
        text = "DETECTING... "

    if (d>7):
        face = "John Connor 100%"
    else:
        face = ""
    text = font.render(text, False, (255, 255, 255))
    screen.blit(text, (screen.get_width()-200, 50))

    W = 150
    H = 200
    x1 = (SCREEN_W-W)//2+120*math.sin((i/100.0)*math.pi)
    x2 = x1 + W
    y1 = (SCREEN_H-H)//2-10+40*abs(math.sin((i/100.0)*math.pi))
    y2 = y1 + H
    col = (200,200,200)
    pygame.draw.line(screen,col,(x1,y1),(x2,y1))
    pygame.draw.line(screen,col,(x2,y1),(x2,y2))
    pygame.draw.line(screen,col,(x2,y2),(x1,y2))
    pygame.draw.line(screen,col,(x1,y2),(x1,y1))
    text = font.render(face, False, (255, 255, 255))
    screen.blit(text, (x1-10, y1-20))

    ie = i-int(i/100.0)*100
    if ie>80:
      effect = pygame.transform.rotozoom(boom, 0.0, (ie-90)/10.0)
      screen.blit(effect, ((SCREEN_W-effect.get_width())//2,(SCREEN_H-effect.get_height())/2))

def main():
    # basic start
    pygame.init()
    pygame.camera.init()

    if 'numpy' in surfarray.get_arraytypes():
        surfarray.use_arraytype('numpy')
        print("NUMPY DETECTED")
    else:
        print("CANNOT OPERATE WITH SURF ARRAY (numpy)")
        return

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY 10 - Machine learning, wrong answers only')

    f = open("day6_listing.txt", "r")
    listing = f.read()
    lines = listing.splitlines()
    font_listing = pygame.font.SysFont('Courrier New', 18)
    font_status = pygame.font.SysFont('Courrier New', 30)

    target = pygame.image.load('day10_target.png').convert_alpha()
    target = pygame.transform.rotozoom(target, 0.0, SCREEN_W/6/target.get_width())
    target.set_alpha(50)

    boom = pygame.image.load('day10_boom.png').convert_alpha()

    camlist = pygame.camera.list_cameras()
    use_cam = False

    if camlist:
        cam = pygame.camera.Camera(camlist[0])
        cam.set_controls(hflip=True, vflip=False)
        cam.start()
        use_cam = True
        john =  pygame.display.set_mode(cam.get_size())
    else:
        john = pygame.image.load('day10_john.jpg')
        john = pygame.transform.rotozoom(john, 0.0, SCREEN_H/john.get_height())
        filter(john,0.6,0.1,0.1)

    i = 0
    clock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        if use_cam:
            cam.get_image(john)
 #           john = pygame.transform.rotozoom(john, 0.0, SCREEN_W/john.get_width())
            redimg = fast_filter(john)
            surfarray.blit_array(screen, redimg)

        screen.blit(john, (0, 0))
        screen.blit(target, ((SCREEN_W-target.get_width())//2,(SCREEN_H)//2))
        print_status(screen, font_status, boom, i)
        print_listing(screen, lines, font_listing, i, 25)

        i += 1
        pygame.display.flip()
        clock.tick(15)

if __name__ == '__main__': main()
