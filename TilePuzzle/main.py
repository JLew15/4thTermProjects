import pygame as pg
import sys
from settings import *
from sprites import *
import random as r
from os import path
import PIL
import image_slicer as slicer


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()
        self.mousePos = pg.mouse.get_pos()
        pg.mouse.set_visible(False)

    def loadData(self):
        gameFolder = path.dirname(__file__)
        imgFolder = path.join(gameFolder, 'img')
        self.imageList = []
        self.imageNames = []
        for col in range(4):
            for row in range(5):
                filename = "doggo_0{}_0{}.png".format(col+1, row+1)
                self.imageList.append(pg.image.load(path.join(imgFolder, filename)))
                self.imageNames.append(filename)

    def new(self):
        self.allSprites = pg.sprite.Group()
        self.imageTiles = pg.sprite.Group()
        self.lastPiece = pg.sprite.Group()
        self.mouse = pg.sprite.Group()
        temporList = []
        self.doggoPieces = slicer.slice("img/doggo.png", 20)
        for i in range(4):
            for x in range(5):
                y = ImageTile(self, IMAGEWIDTH*i, IMAGEHEIGHT*x)
                temporList.append(y)
        temporList[-1].kill()
        self.allSprites.remove(temporList[-1])
        self.lastPiece.add(temporList[-1])
        self.pointer = Pointer(self, self.mousePos)


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
        self.mousePos = pg.mouse.get_pos()
        hits = pg.sprite.spritecollide(self.pointer, self.imageTiles, False)
        rightClick = pg.mouse.get_pressed(3)
        if hits and rightClick[0]:
            hits[0].move()
        #     hits[0].moveX(IMAGEWIDTH, 0)
        # if hits and rightClick[2]:
        #     hits[0].moveY(0, IMAGEHEIGHT)


    def draw(self):
        self.screen.fill(BGCOLOR)
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
