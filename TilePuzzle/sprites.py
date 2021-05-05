import pygame as pg
from settings import *
import random as r


class ImageTile(pg.sprite.Sprite):
    choiceList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.imageTiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        pick = r.choice(ImageTile.choiceList)
        self.image = game.imageList[pick]
        self.positionName = game.imageNames[pick]
        ImageTile.choiceList.remove(pick)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.canMove = None

    def moveX(self, dx=0, dy=0):
        # MOVE RIGHT
        if not self.collide_with_wallsX(dx):
            self.x += dx
        elif not self.collide_with_wallsX(-dx):
            self.x += -dx
        print("CLICKED")

    def moveY(self, dx=0, dy=0):
        if self.collide_with_wallsY(dy):
            self.y += -dy
        elif self.collide_with_wallsY(-dy):
            self.y += dy

    def collide_with_wallsX(self, dx=0, dy=0):
        for tile in self.game.imageTiles:
            if tile.x == self.x + dx and tile.y == self.y + dy:
                return True
        return False

    def collide_with_wallsY(self, dy, dx=0):
        for tile in self.game.imageTiles:
            if tile.y == self.y + dy and tile.x == self.x + dx:
                return True
        return False

    def move(self):
        self.findOpen()
        print(self.canMove)
        if self.canMove == "right":
            self.x += IMAGEWIDTH
        elif self.canMove == "left":
            self.x -= IMAGEWIDTH
        elif self.canMove == "up":
            self.y -= IMAGEHEIGHT
        elif self.canMove == "down":
            self.y += IMAGEHEIGHT
        else:
            pass

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def findOpen(self):
        if self.y + IMAGEHEIGHT != tile.y:
            self.canMove = "down"
        elif self.y - IMAGEHEIGHT != tile.y:
            self.canMove = "up"
        elif self.x + IMAGEWIDTH != tile.x:
            self.canMove = "right"
        elif self.x - IMAGEWIDTH != tile.x:
            self.canMove = "left"
        else:
            self.canMove = None



class Pointer(pg.sprite.Sprite):
    def __init__(self, game, mousePos):
        self.groups = game.allSprites, game.mouse
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((25, 25))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = mousePos

    def update(self):
        self.rect.center = self.game.mousePos