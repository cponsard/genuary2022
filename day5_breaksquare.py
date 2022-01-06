"""
Genuary2022 Day 5 Destroy a square
Tribute to breakout by C. Ponsard
Free under the terms of GPLv3 license

Run and press space TWICE to start
"""

import pygame
from pygame.locals import *

# constants
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 640
BALL_DIAM = 16
BRICK_WIDTH, BRICK_HEIGHT = 32, 32
BALL_SPEED = 25

class Breakout_Sprite(pygame.sprite.Sprite):
    """ Breakout Sprite class that extends following classes

        Attributes:
            image_file (str): Sprite-image filename.
    """
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)

        # load image & rect
        self.image = pygame.image.load('images/' + image_file).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

class Brick(pygame.sprite.Sprite):
    """ Brick: Statically positionned in (x, y).
    """
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)

        # load image & rect
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Ball(pygame.sprite.Sprite):
    """ Ball: Moves according to speed (speed_x, speed_y).

        Attributes:
            speed_x (int): Ball's x-speed.
            speed_y (int): Ball's y-speed.
    """
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([BALL_DIAM, BALL_DIAM])
        pygame.draw.circle(self.image, color, (BALL_DIAM/2, BALL_DIAM/2), BALL_DIAM/2)
        self.rect = self.image.get_rect()
        self.rect.bottom = WINDOW_HEIGHT/2 +8
        self.rect.left = WINDOW_WIDTH /2 -10
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)

        # bounce against borders
        if self.rect.x > WINDOW_WIDTH - self.image.get_width() or self.rect.x < 0:
            self.speed_x *= -1
        if self.rect.y > WINDOW_HEIGHT - self.image.get_height() or self.rect.y < 0:
            self.speed_y *= -1

def main():
    # game init
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Genuary2022 - DAY5 - Breakout the square  by C.Ponsard - PRESS SPACE TWICE')
    pygame.key.set_repeat(400, 30)
    clock = pygame.time.Clock()
    score = 0

    # groups
    all_sprites_group = pygame.sprite.Group()
    player_bricks_group = pygame.sprite.Group()
    bricks_group = pygame.sprite.Group()

    orange = Color(255,160,55)
    red = Color(200,0,0)

    # add sprites to their group
    ball = Ball(red)
    all_sprites_group.add(ball)

    for i in range(17):
        for j in range(17):
            brick = Brick(orange, (i+1)*(BRICK_WIDTH + 2), (j+1)*(BRICK_HEIGHT + 2))
    #        if i==9 and j==9: continue
            all_sprites_group.add(brick)
            bricks_group.add(brick)
            player_bricks_group.add(brick)

    clock = pygame.time.Clock()
    space = 0

    # game loop
    while True:
        clock.tick(300)

        # move player horizontally
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                space = space+1
                if space==2:
                    ball.speed_x=BALL_SPEED
                    ball.speed_y=BALL_SPEED

        # collision detection (ball bounce against brick & player)
        hits = pygame.sprite.spritecollide(ball, player_bricks_group, False)
        if hits:
            hit_rect = hits[0].rect
            # bounce the ball (according to side collided)
            if hit_rect.left > ball.rect.left or ball.rect.right < hit_rect.right:
                ball.speed_y *= -1
            else:
                ball.speed_x *= -1

            # collision with blocks
            if pygame.sprite.spritecollide(ball, bricks_group, True):
                score += len(hits)
                print("Score: %s" % score)

        # render groups
        window.fill((0, 0, 0))
        all_sprites_group.draw(window)

        if space<1:
            pygame.draw.rect(window, orange,(BRICK_WIDTH+2,BRICK_HEIGHT+2,WINDOW_WIDTH-2*BRICK_WIDTH,WINDOW_HEIGHT-2*BRICK_HEIGHT))

        # refresh screen
        all_sprites_group.update()
        clock.tick(60)
        pygame.display.flip()

if __name__ == '__main__': main()