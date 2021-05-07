import pygame as pg
import sys
from os import path
import math
import random as r

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.vx, self.vy = 0, 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_UP]:
            self.vy += 5
        if keystate[pg.K_DOWN]:
            self.vy += -5
        if keystate[pg.K_RIGHT]:
            self.vx += 5
        if keystate[pg.K_LEFT]:
            self.vx += -5


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(r.randint(0, WIDTH), r.randint(0, HEIGHT))
        self.vel = vec(MAXSPEED, 0).rotate(r.uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    def followMouse(self):
        mousePos = pg.mouse.get_pos()
        plpos = player.rect.center
        self.acc = (plpos - self.pos).normalize()

    def update(self):
        self.followMouse()
        self.vel += self.acc
        if self.vel.length() > MAXSPEED:
            self.vel.scale_to_length(MAXSPEED)
        self.pos += self.vel
        self.rect.center = self.pos
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT


MAXSPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIDTH = 1000
HEIGHT = 650
FPS = 60
TITLE = "Movement"
BGCOLOR = WHITE

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

allSprites = pg.sprite.Group()

player = Player()
mob = Mob()

allSprites.add(player)
allSprites.add(mob)

running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    allSprites.update()
    screen.fill(BLACK)
    allSprites.draw(screen)
    pg.display.flip()

pg.quit()
