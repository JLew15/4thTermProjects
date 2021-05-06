import pygame as pg
import sys
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.loadData()

    def loadData(self):
        gameFolder = path.dirname(__file__)
        self.mapData = []
        with open(path.join(gameFolder, 'map.txt'), 'rt') as f:
            for line in f:
                self.mapData.append(line)

    def new(self):
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.mapData):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.allSprites.update()

    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.drawGrid()
        self.allSprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def showStartScreen(self):
        pass

    def showGOScreen(self):
        pass


g = Game()
g.showStartScreen()
while True:
    g.new()
    g.run()
    g.showGOScreen()

pg.quit()
