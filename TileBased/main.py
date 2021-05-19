# "topdown shooter" art by Kenny.nl
# Weapon pickup by: Guns by Gary <http://fossilrecords.net/> licensed under CC-BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>
# "espionage.ogg" by http://opengameart.org/users/haeldb

import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from random import choice, random
from tilemap import *

def drawPlayerHealth(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BARLENGTH = 100
    BARHEIGHT = 20
    fill = pct*BARLENGTH
    outlineRect = pg.Rect(x, y, BARLENGTH, BARHEIGHT)
    fillRect = pg.Rect(x, y, fill, BARHEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fillRect)
    pg.draw.rect(surf, WHITE, outlineRect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()

    def drawText(self, text, fontName, size, color, x, y, align="nw"):
        font = pg.font.Font(fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        if align == "nw":
            textRect.topleft = (x, y)
        if align == "ne":
            textRect.topright = (x, y)
        if align == "sw":
            textRect.bottomleft = (x, y)
        if align == "se":
            textRect.bottomright = (x, y)
        if align == "n":
            textRect.midtop = (x, y)
        if align == "s":
            textRect.midbottom = (x, y)
        if align == "e":
            textRect.midright = (x, y)
        if align == "w":
            textRect.midleft = (x, y)
        if align == "center":
            textRect.center = (x, y)
        self.screen.blit(textSurface, textRect)

    def loadData(self):
        gameFolder = path.dirname(__file__)
        imgFolder = path.join(gameFolder, 'img')
        audFolder = path.join(gameFolder, 'aud')
        musicFolder = path.join(gameFolder, 'music')
        self.mapFolder = path.join(gameFolder, 'maps')
        self.titleFont = path.join(imgFolder, 'ZOMBIE.TTF')
        self.hudFont = path.join(imgFolder, 'Impacted2.0.ttf')
        self.dimScreen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dimScreen.fill((0, 0, 0, 180))
        self.playerImg = pg.image.load(path.join(imgFolder, PLAYERIMAGE)).convert_alpha()
        self.bulletImages = {}
        self.bulletImages['lg'] = pg.image.load(path.join(imgFolder, BULLETIMAGE)).convert_alpha()
        self.bulletImages['sm'] = pg.transform.scale(self.bulletImages['lg'], (10, 10))
        self.mobImg = pg.image.load(path.join(imgFolder, MOBIMAGE)).convert_alpha()
        self.splat = pg.image.load(path.join(imgFolder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gunFlashes = []
        for img in MUZZLEFLASHES:
            self.gunFlashes.append(pg.image.load(path.join(imgFolder, img)).convert_alpha())
        self.itemImages = {}
        for item in ITEMIMAGES:
            self.itemImages[item] = pg.image.load(path.join(imgFolder, ITEMIMAGES[item])).convert_alpha()
        pg.mixer.music.load(path.join(musicFolder, BGMUSIC))
        self.effectsSounds = {}
        for type in EFFECTSSOUNDS:
            self.effectsSounds[type] = pg.mixer.Sound(path.join(audFolder, EFFECTSSOUNDS[type]))
        self.weaponSounds = {}
        for weapon in WEAPONSOUNDS:
            self.weaponSounds[weapon] = []
            for snd in WEAPONSOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(audFolder, snd))
                s.set_volume(0.3)
                self.weaponSounds[weapon].append(s)
        self.zombieMoanSounds = []
        for snd in ZOMBIEMOANSOUNDS:
            s = pg.mixer.Sound(path.join(audFolder, snd))
            s.set_volume(0.2)
            self.zombieMoanSounds.append(s)
        self.playerHitSounds = []
        for snd in PLAYERHITSOUNDS:
            self.playerHitSounds.append(pg.mixer.Sound(path.join(audFolder, snd)))
        self.zombieHitSounds = []
        for snd in ZOMBIEHITSOUNDS:
            self.zombieHitSounds.append(pg.mixer.Sound(path.join(audFolder, snd)))

    def new(self):
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.mapFolder, 'level1.tmx'))
        self.mapImg = self.map.makeMap()
        self.map.rect = self.mapImg.get_rect()
        for tileObject in self.map.tmxdata.objects:
            objCenter = vec(tileObject.x + tileObject.width / 2, tileObject.y + tileObject.height / 2)
            if tileObject.name == 'player':
                self.player = Player(self, objCenter.x, objCenter.y)
            if tileObject.name == 'zombie':
                Mob(self, objCenter.x, objCenter.y)
            if tileObject.name == 'wall':
                Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
            if tileObject.name in ['health', 'shotgun']:
                Item(self, objCenter, tileObject.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.drawDebug = False
        self.paused = False
        self.effectsSounds['levelStart'].play()

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.allSprites.update()
        self.camera.update(self.player)
        if len(self.mobs) == 0:
            self.playing = False
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYERHEALTH:
                hit.kill()
                self.effectsSounds['healthUp'].play()
                self.player.addHealth(HEALTHPACKAMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effectsSounds['gunPickup'].play()
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collideHitRect)
        for hit in hits:
            if random() < 0.7:
                choice(self.playerHitSounds).play()
            self.player.health -= MOBDAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOBKNOCKBACK, 0).rotate(-hits[0].rot)
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.mapImg, self.camera.apply(self.map))
        for sprite in self.allSprites:
            if isinstance(sprite, Mob):
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.drawDebug:
                pg.draw.rect(self.screen, CYAN, self.camera.applyRect(sprite.hitRect), 1)
        if self.drawDebug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.applyRect(wall.rect), 1)
        drawPlayerHealth(self.screen, 10, 10, self.player.health / PLAYERHEALTH)
        self.drawText('Zombies: {}'.format(len(self.mobs)), self.hudFont, 30, WHITE, WIDTH - 10, 10, align = "ne")
        if self.paused:
            self.screen.blit(self.dimScreen, (0, 0))
            self.drawText("Paused", self.titleFont, 105, RED, WIDTH / 2, HEIGHT /2, align="center")
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.drawDebug = not self.drawDebug
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def showStartScreen(self):
        pass

    def showGOScreen(self):
        self.screen.fill(BLACK)
        self.drawText("GAME OVER", self.titleFont, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        self.drawText("Press a key to start", self.titleFont, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.waitForKey()

    def waitForKey(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.showStartScreen()
while True:
    g.new()
    g.run()
    g.showGOScreen()
