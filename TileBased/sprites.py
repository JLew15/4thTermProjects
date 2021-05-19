import pygame as pg
from settings import *
from tilemap import collideHitRect
import pytweening as tween
from itertools import chain
from random import uniform, choice, randint, random


def collideWithWalls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collideHitRect)
        if hits:
            if hits[0].rect.centerx > sprite.hitRect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hitRect.width / 2
            if hits[0].rect.centerx < sprite.hitRect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hitRect.width / 2
            sprite.vel.x = 0
            sprite.hitRect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collideHitRect)
        if hits:
            if hits[0].rect.centery > sprite.hitRect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hitRect.height / 2
            if hits[0].rect.centery < sprite.hitRect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hitRect.height / 2
            sprite.vel.y = 0
            sprite.hitRect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYERLAYER
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.playerImg
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hitRect = PLAYERHITRECT
        self.hitRect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.lastShot = 0
        self.health = PLAYERHEALTH
        self.weapon = 'pistol'
        self.damaged = False

    def getKeys(self):
        self.rotSpeed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rotSpeed = PLAYERROTSPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rotSpeed = -PLAYERROTSPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.lastShot > WEAPONS[self.weapon]['rate']:
            self.lastShot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARRELOFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bulletCount']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weaponSounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def hit(self):
        self.damaged = True
        self.damageAlpha = chain(DAMAGEALPHA * 4)

    def update(self):
        self.getKeys()
        self.rot = (self.rot + self.rotSpeed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.playerImg, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damageAlpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hitRect.centerx = self.pos.x
        collideWithWalls(self, self.game.walls, 'x')
        self.hitRect.centery = self.pos.y
        collideWithWalls(self, self.game.walls, 'y')
        self.rect.center = self.hitRect.center

    def addHealth(self, amount):
        self.health += amount
        if self.health > PLAYERHEALTH:
            self.health = PLAYERHEALTH

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOBLAYER
        self.groups = game.allSprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mobImg.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hitRect = MOBHITRECT.copy()
        self.hitRect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOBHEALTH
        self.speed = choice(MOBSPEEDS)
        self.target = game.player

    def avoidMobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dis = self.pos - mob.pos
                if 0 < dis.length() < AVOIDRADIUS:
                    self.acc += dis.normalize()

    def update(self):
        targetDist = self.target.pos - self.pos
        if targetDist.length_squared() < DETECTRADIUS**2:
            if random() < 0.002:
                choice(self.game.zombieMoanSounds).play()
            self.rot = targetDist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mobImg, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoidMobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hitRect.centerx = self.pos.x
            collideWithWalls(self, self.game.walls, 'x')
            self.hitRect.centery = self.pos.y
            collideWithWalls(self, self.game.walls, 'y')
            self.rect.center = self.hitRect.center
        if self.health <= 0:
            choice(self.game.zombieHitSounds).play()
            self.kill()
            self.game.mapImg.blit(self.game.splat, self.pos - vec(32, 32))

    def drawHealth(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOBHEALTH)
        self.healthBar = pg.Rect(0, 0, width, 7)
        if self.health < MOBHEALTH:
            pg.draw.rect(self.image, col, self.healthBar)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLETLAYER
        self.groups = game.allSprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bulletImages[WEAPONS[game.player.weapon]['bulletSize']]
        self.rect = self.image.get_rect()
        self.hitRect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * WEAPONS[game.player.weapon]['bulletSpeed'] * uniform(0.9, 1.1)
        self.spawnTime = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawnTime > WEAPONS[self.game.player.weapon]['bulletLifetime']:
            self.kill()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hitRect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTSLAYER
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gunFlashes), (size, size))
        self.rect = self.image.get_rect()
        self.hitRect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawnTime = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawnTime > FLASHDURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMSLAYER
        self.groups = game.allSprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.itemImages[type]
        self.rect = self.image.get_rect()
        self.hitRect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = BOBRANGE * (self.tween(self.step / BOBRANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOBSPEED
        if self.step > BOBRANGE:
            self.step = 0
            self.dir *= -1
