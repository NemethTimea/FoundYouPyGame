import pygame
from enum import Enum

from UI import Button

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND1 = pygame.image.load("img/Background/bg1.png").convert_alpha()
BACKGROUND2 = pygame.image.load("img/Background/bg2.png").convert_alpha()
MOUNTAIN = pygame.image.load("img/Background/mountain.png").convert_alpha()
SKY = pygame.image.load("img/Background/sky.png").convert_alpha()
GAME_OVER = pygame.image.load("img/Background/gameover.png").convert_alpha()
WIN = pygame.image.load("img/Background/win.png").convert_alpha()
BOUCKET = pygame.image.load("img/Objects/boucket.png").convert_alpha()

FPS = 60
SEC = 1500000
ROWS = 16
COLS = 150
#game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
TILE_SIZE = 40
# TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 26

BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PINK = (235, 65, 54)
YELLOW = (255, 255, 0)

# sound and musics

pygame.mixer.init()
# pygame.mixer.music.load('music/music2.mp3')
# pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play(-1, 0.0, 5000)

jump_sound = pygame.mixer.Sound('music/jump.wav')
jump_sound.set_volume(0.5)
shot_sound = pygame.mixer.Sound('music/shot.wav')
shot_sound.set_volume(0.5)
rock_sound = pygame.mixer.Sound('music/grenade.wav')
rock_sound.set_volume(0.5)

pygame.font.init()
FONT = pygame.font.SysFont('Futura', 30)

BUTTON_START = pygame.image.load('img/Buttons/start.png').convert_alpha()
BUTTON_EXIT = pygame.image.load('img/Buttons/exit.png').convert_alpha()
BUTTON_RESTART = pygame.image.load('img/Buttons/restart.png').convert_alpha()

BULLET_IMG = pygame.image.load('img/Objects/0.png').convert_alpha()
ROCK_IMG = pygame.image.load('img/Objects/1.PNG').convert_alpha()

# Item for collect
ROCK_COLL = pygame.image.load('img/Objects/rock_collect.png').convert_alpha()
HEALTH_COLL = pygame.image.load('img/Objects/heart.png').convert_alpha()
ROSE = pygame.image.load('img/Objects/rose.png').convert_alpha()
BLUE_F = pygame.image.load('img/Objects/blue.png').convert_alpha()
PINK_F = pygame.image.load('img/Objects/pinck.png').convert_alpha()
YELLOW_F = pygame.image.load('img/Objects/yellow.png').convert_alpha()

MAX_LEVELS = 2

bullet_group = pygame.sprite.Group()
rock_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
npc_group = pygame.sprite.Group()

start_button = Button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT //2 - 150, BUTTON_START, 1)
exit_button = Button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT //2 + 50, BUTTON_EXIT, 1)
restart_button = Button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2 - 50, BUTTON_RESTART, 2)


#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"img/Tile/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

ITEM_TYPES = Enum("ItemsType", "Rock Health Rose BlueFlower PinkFlower YellowFlower")

ITEMS = {
    ITEM_TYPES.Rock : ROCK_COLL,
    ITEM_TYPES.Health : HEALTH_COLL,
    ITEM_TYPES.Rose : ROSE,
    ITEM_TYPES.BlueFlower : BLUE_F,
    ITEM_TYPES.PinkFlower : PINK_F,
    ITEM_TYPES.YellowFlower : YELLOW_F
}

