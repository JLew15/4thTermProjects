import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Jumpy Jump")
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def new(self):
        self.allSprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player()
        self.allSprites.add(self.player)
        p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
        self.allSprites.add(p1)
        self.platforms.add(p1)
        p2 = Platform(WIDTH/2 - 50, HEIGHT * 3 / 4, 100, 20)
        self.allSprites.add(p2)
        self.platforms.add(p2)
        self.run()

    def update(self):
        self.allSprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            self.player.vel.y = 0

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.allSprites.draw(g.screen)
        pg.display.flip()

    def showStartScreen(self):
        pass

    def showGOScreen(self):
        pass


g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGOScreen()

pg.quit()
