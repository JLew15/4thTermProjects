import pygame as pg

vec = pg.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Tile Based"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_SPEED = 300
PLAYERHEALTH = 100
PLAYERROTSPEED = 200
PLAYERIMAGE = 'manBlue_gun.png'
PLAYERHITRECT = pg.Rect(0, 0, 35, 35)
BARRELOFFSET = vec(30, 10)

BULLETIMAGE = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bulletSpeed': 500,
                     'bulletLifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bulletSize': 'lg',
                     'bulletCount': 1}
WEAPONS['shotgun'] = {'bulletSpeed': 400,
                      'bulletLifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bulletSize': 'sm',
                      'bulletCount': 12}

MOBIMAGE = 'zombie1_hold.png'
MOBSPEEDS = [150, 100, 75, 125]
MOBHITRECT = pg.Rect(0, 0, 30, 30)
MOBHEALTH = 100
MOBDAMAGE = 10
MOBKNOCKBACK = 20
AVOIDRADIUS = 50
DETECTRADIUS = 400

MUZZLEFLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png', 'whitePuff18.png']
SPLAT = 'splat green.png'
FLASHDURATION = 50
DAMAGEALPHA = [i for i in range(0, 255, 55)]

WALLLAYER = 1
PLAYERLAYER = 2
BULLETLAYER = 3
MOBLAYER = 2
EFFECTSLAYER = 4
ITEMSLAYER = 1

ITEMIMAGES = {'health': 'health_pack.png',
              'shotgun': 'obj_shotgun.png'}
HEALTHPACKAMOUNT = 20
BOBRANGE = 10
BOBSPEED = 0.3

BGMUSIC = 'espionage.ogg'
PLAYERHITSOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIEMOANSOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav', 'zombie-roar-3.wav',
                    'zombie-roar-4.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIEHITSOUNDS = ['splat-15.wav']
WEAPONSOUNDS = {'pistol': ['pistol.wav'],
                'shotgun': ['shotgun.wav']}
EFFECTSSOUNDS = {'levelStart': 'level_start.wav',
                 'healthUp': 'health_pack.wav',
                 'gunPickup': 'gun_pickup.wav'}
