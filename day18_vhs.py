"""
Genuary2022 Day 18 VHS
Horror movie remixed by C. Ponsard
Free under the terms of GPLv3 license
"""

import random

import pygame
from pygame.locals import *

SCREEN_W, SCREEN_H = (600, 800)

N = 500
NC = 7
NL = 60
BC = 2
BL = 5
SC = 4
SL = 4

def fill(tab,col,l1,l2):
    for i in range(l1,l2+1):
        tab[BL+i-1][BC+col-1] = True

def init_tab():
    tab = [[False for j in range(NC+2*BC)] for i in range(NL+2*BL)]
    fill(tab,1,12,36)
    fill(tab,2,6,23)
    fill(tab,2,33,41)
    fill(tab,3,2,25)
    fill(tab,3,34,52)
    fill(tab,3,56,58)
    fill(tab,4,1,33)
    fill(tab,4,42,49)
    fill(tab,4,55,60)
    fill(tab,5,2,25)
    fill(tab,5,34,52)
    fill(tab,5,56,58)
    fill(tab,6,6,23)
    fill(tab,6,33,41)
    fill(tab,7,12,36)
    return tab

# TODO avoid previous move
def random_empty(tab):
    while True:
        l = random.randint(0,2*BL+NL-1)
        c = random.randint(0,2*BC+NC-1)
        if not tab[l][c]:
            return (l,c)

def get_borders(tab,p):
    res = []
    (l,c) = p
    ML=2*BL+NL-1
    MC=2*BC+NC-1
    if l>0 and tab[l-1][c]: res.append((l-1,c))
    if l<ML and tab[l+1][c]: res.append((l+1,c))
    if c>0 and tab[l][c-1]: res.append((l,c-1))
    if c<MC and tab[l][c+1]: res.append((l,c+1))
    return res

def random_move(tab):
    while True:
        p1 = random_empty(tab)
        lp2 = get_borders(tab,p1)
        if len(lp2)==0: continue
        i = random.randint(0,len(lp2)-1)
        p2 = lp2[i]
#        print(str(p1)+' '+str(tab[p1[0]][p1[1]]))
#        print(str(p2)+' '+str(tab[p2[0]][p2[1]]))
        return (p1,p2)

def mix_tab(tab):
    moves = []
    for i in range(N):
        (p1,p2)=random_move(tab)
        tab[p1[0]][p1[1]] = True
        tab[p2[0]][p2[1]] = False
        moves.append((p1,p2))
    return moves

def unmove(tab,move):
    (p1,p2) = move
    tab[p2[0]][p2[1]] = True
    tab[p1[0]][p1[1]] = False

def print_tab(tab):
    for i in range(NL):
        for j in range(NC):
            if tab[i][j]:
                print("XXXXXX", end='')
            else:
                print("      ", end='')
        print()

def generate_eraser(vhs):
    img = pygame.Surface(vhs.get_size())
    img = img.convert()
    img.fill((0,0,0))
    return img

def generate_poster(screen, tab, vhs, eraser, font):
    img = pygame.Surface(screen.get_size())
    img = img.convert()
    img.fill((0,0,0))
    W = vhs.get_width()+SC
    H = vhs.get_height()+SL
#    print(str(W)+" "+str(H))
    for i in range(NL+2*BL):
        for j in range(NC+2*BC):
#            print(str(j*W) + " " + str(i*H))
            if tab[i][j]:
                img.blit(vhs,(SC+j*W,i*H))
            else:
                img.blit(eraser,(SC+j*W,i*H))

    text = font.render("V/H/S", False, (230, 0, 0))
    img.blit(text, (142,H*NL+70))

    return img

def update_poster(poster, move, vhs, eraser):
    (p1,p2) = move
    W = vhs.get_width()+SC
    H = vhs.get_height()+SL
    poster.blit(eraser, (SC+p1[1] * W, p1[0] * H))
    poster.blit(vhs, (SC+p2[1] * W, p2[0] * H))
    return

def vhs_filter(source):
    dest = pygame.Surface.copy(source)
    w, h = source.get_size()
    for i in range(10):
        l = random.randint(0,h-10)
        nl = random.randint(4,8)
        dx = random.randint(4,8)
        for j in range(nl):
            y = l+j
            for x in range(w-dx):
                dest.set_at((x+dx, y), source.get_at((x, y)))
    return dest

def main():
    # basic start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption('Genuary2022 - DAY18 - VHS remixed by C.Ponsard')

    clock = pygame.time.Clock()
    tab = init_tab()
    print_tab(tab)
    moves = mix_tab(tab)
    print_tab(tab)
    vhs = pygame.image.load('day18_vhs01.png').convert_alpha()
    vhs = pygame.transform.rotozoom(vhs, 0.0, SCREEN_W/(vhs.get_width()*(NC+BC*2+1)))
    eraser = generate_eraser(vhs)
    font = pygame.font.SysFont('Courrier New', 175)
    poster = generate_poster(screen, tab, vhs, eraser, font)

    i = N-1
    start = True

#    for i in range(N):
#        unmove(tab, moves[N-i-1])
#    print_tab(tab)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                start = True

        if not start:
            clock.tick(1)
            continue

        if i >= 0:
            unmove(tab, moves[i])
            update_poster(poster, moves[i], vhs, eraser)
            vhs_poster=vhs_filter(poster)
            screen.blit(vhs_poster, (0, 0))
            pygame.display.flip()
            i -= 1

        clock.tick(100)


if __name__ == '__main__': main()
