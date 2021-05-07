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
        self.game.imageTiles.remove(self)
        self.game.moveGroup.add(self)
        # MOVE DOWN CHECK
        self.rect.y += 20
        hits = pg.sprite.groupcollide(self.game.imageTiles, self.game.moveGroup, False, False)
        if hits:
            self.rect.y -= 20
            self.canMove = None

            # MOVE UP CHECK
            self.rect.y -= 20
            hits2 = pg.sprite.groupcollide(self.game.imageTiles, self.game.moveGroup, False, False)
            if hits2:
                self.rect.y += 20
                self.canMove = None

                # MOVE RIGHT CHECK
                self.rect.x += 20
                hits3 = pg.sprite.groupcollide(self.game.imageTiles, self.game.moveGroup, False, False)
                if hits3:
                    self.rect.x -= 20
                    self.canMove = None

                    # MOVE LEFT CHECK
                    self.rect.x -= 20
                    hits4 = pg.sprite.groupcollide(self.game.imageTiles, self.game.moveGroup, False, False)
                    if hits4:
                        self.rect.x += 20
                        self.canMove = None
                    else:
                        self.canMove = "left"
                        self.rect.x += 20
                else:
                    self.canMove = "right"
                    self.rect.x -= 20
            else:
                self.canMove = "up"
                self.rect.y += 20
        else:
            self.canMove = "down"
            self.rect.y -= 20
        self.game.moveGroup.remove(self)
        self.game.imageTiles.add(self)


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


class Wall(pg.sprite.Sprite):
    def __init__(self):
        super(Wall, self).__init__()
        self.image = pg.Surface((WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
