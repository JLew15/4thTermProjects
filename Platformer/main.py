import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Jumpy Jump")
        self.clock = pg.time.Clock()
        self.running = True
        self.fontName = pg.font.match_font(FONT_NAME)
        self.loadData()

    def loadData(self):
        self.directory = path.dirname(__file__)
        with open(path.join(self.directory, HSFILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def new(self):
        self.score = 0
        self.allSprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.allSprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.allSprites.add(p)
            self.platforms.add(p)
        self.run()

    def update(self):
        self.allSprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if self.player.rect.top <= HEIGHT /4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.allSprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH-width), random.randrange(-75, -30), width, 20)
            self.platforms.add(p)
            self.allSprites.add(p)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.allSprites.draw(g.screen)
        self.drawText(str(self.score), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()

    def showStartScreen(self):
        self.screen.fill(BGCOLOR)
        self.drawText("Jumpy Jump", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.drawText("Arrows to move, space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.drawText("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3 / 4)
        self.drawText("High Score: " + str(self.highscore), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.waitForKey()


    def showGOScreen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.drawText("Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.drawText("NEW HIGH SCORE!", 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.directory, HSFILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.drawText("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        pg.display.flip()
        self.waitForKey()

    def drawText(self, text, size, color, x, y):
        font = pg.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGOScreen()

pg.quit()
