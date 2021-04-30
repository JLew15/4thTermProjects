import pygame as pg
import random
from settings import *
from sprites import *
from os import path

# Character and Level sprites by Kenney.nl
# Happy Tune by http://opengameart.org/users/syncopika
# Yippee by http://opengameart.org/users/snabisch


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.fontName = pg.font.match_font(FONT_NAME)
        self.loadData()

    def loadData(self):
        self.directory = path.dirname(__file__)
        imgDirectory = path.join(self.directory, 'img')
        with open(path.join(self.directory, HSFILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(imgDirectory, SPRITESHEET))
        self.audDirectory = path.join(self.directory, 'aud')
        self.jumpSound = pg.mixer.Sound(path.join(self.audDirectory, 'Jump33.wav'))
        self.boostSound = pg.mixer.Sound(path.join(self.audDirectory, 'Boost16.wav'))

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def new(self):
        self.score = 0
        self.allSprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobTimer = 0
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        pg.mixer.music.load(path.join(self.audDirectory, 'Happy Tune.ogg'))
        self.run()

    def update(self):
        self.allSprites.update()

        now = pg.time.get_ticks()
        if now - self.mobTimer > MOB_FREQUENCY + choice([-1000, -500, 0, 500, 1000]):
            self.mobTimer = now
            Mob(self)

        mobHits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mobHits:
            self.playing = False

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 4)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 4)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 4)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        powHits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in powHits:
            if pow.type == 'boost':
                self.boostSound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.allSprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH-width), random.randrange(-75, -30))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jumpCut()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.allSprites.draw(g.screen)
        self.drawText(str(self.score), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()

    def showStartScreen(self):
        pg.mixer.music.load(path.join(self.audDirectory, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.drawText("Jumpy Jump", 48, WHITE, WIDTH/2, HEIGHT/4)
        self.drawText("Arrows to move, space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.drawText("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3 / 4)
        self.drawText("High Score: " + str(self.highscore), 22, WHITE, WIDTH/2, 15)
        pg.display.flip()
        self.waitForKey()
        pg.mixer.music.fadeout(500)


    def showGOScreen(self):
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.audDirectory, 'Yippee.ogg'))
        pg.mixer.music.play(loops=-1)
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
        pg.mixer.fadeout(500)

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
