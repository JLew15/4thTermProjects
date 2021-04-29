from settings import *
import pygame as pg
from random import choice

vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def getImage(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width//2, height//2))
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super(Player, self).__init__()
        self.game = game
        self.walking = False
        self.jumping = False
        self.currentFrame = 0
        self.lastUpdate = 0
        self.loadImages()
        self.image = self.standingFrames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def loadImages(self):
        self.standingFrames = [self.game.spritesheet.getImage(614, 1063, 120, 191),
                               self.game.spritesheet.getImage(690, 406, 120, 201)]
        for frame in self.standingFrames:
            frame.set_colorkey(BLACK)
        self.walkingFramesR = [self.game.spritesheet.getImage(678, 860, 120, 201),
                              self.game.spritesheet.getImage(692, 1458, 120, 207)]
        self.walkingFramesL = []
        for frame in self.walkingFramesR:
            frame.set_colorkey(BLACK)
            self.walkingFramesL.append(pg.transform.flip(frame, True, False))
        self.jumpingFrame = self.game.spritesheet.getImage(382, 763, 150, 181)
        self.jumpingFrame.set_colorkey(BLACK)

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jumpSound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jumpCut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2:
            self.pos.x = WIDTH + self.rect.width/2
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.lastUpdate > 200:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.walkingFramesL)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walkingFramesR[self.currentFrame]
                else:
                    self.image = self.walkingFramesL[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jumpingFrame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.lastUpdate > 350:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.standingFrames)
                bottom = self.rect.bottom
                self.image = self.standingFrames[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Platform, self).__init__()
        self.game = game
        images = [self.game.spritesheet.getImage(0, 288, 380, 94),
                  self.game.spritesheet.getImage(213, 1662, 201, 100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
