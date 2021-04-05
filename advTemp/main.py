import pygame as pg
import random as r
from settings import *
from sprites import *


class Game(object):
    def __init__(self):
        self.running = True

    def new(self):
        pass

    def run(self):
        pass

    def events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def startScreen(self):
        pass

    def gameOver(self):
        pass

    def options(self):
        pass


g = Game()
g.startScreen()

while g.running:
    g.new()
    g.gameOver()

pg.quit()
