from Textures.Decoration import Decoration
from Textures.Water import Water
from Textures import Item
from UI.Exit import Exit
from UI import HealthBar
from Characters import Player, Enemy, Girl
from consts import *

import csv

class World():
    obstacle_list = []
    def __init__(self):
        self.screen_scroll = 0
        self.bg_scroll = 0

    def load_level(self, level: int):
        world_data = []
        for _ in range(ROWS):
            r = [-1] * COLS
            world_data.append(r)

        #loadin level data and create world
        with open(f"API/level{level}_data.csv", newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        return world_data


    def process_data(self, data):
        self.level_length = len(data[0])
        player = None
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                     # earth
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    # water
                    elif tile >= 9 and tile <= 10:
                        water = Water(img= img, x= x * TILE_SIZE, y= y * TILE_SIZE)
                        water_group.add(water)
                    # decoration
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img= img, x= x * TILE_SIZE, y= y * TILE_SIZE)
                        decoration_group.add(decoration)
                    # player
                    elif tile == 15:
                        player = Player.Player(x= x * TILE_SIZE, y= y * TILE_SIZE, scale=1, speed=5, nr_of_bullet=20, rocks=10, world= self)
                        player_group.add(player)
                        health_bar = HealthBar.HealthBar(10, 10, player.health, player.health)
                    # enemy
                    elif tile == 16:
                        enemy = Enemy.Enemy(x= x * TILE_SIZE, y= y * TILE_SIZE, scale=0.95, speed=2, obstacles=self.obstacle_list)
                        enemy_group.add(enemy)
                    # rose
                    elif tile == 17:
                        item_box = Item.Item(ITEM_TYPES.Rose, x= x * TILE_SIZE, y= y * TILE_SIZE)
                        item_box_group.add(item_box)
                    # rock
                    elif tile == 18:
                        item_box = Item.Item(ITEM_TYPES.Rock, x= x * TILE_SIZE, y= y * TILE_SIZE)                  
                        item_box_group.add(item_box)
                    #health
                    elif tile == 19:
                        item_box = Item.Item(ITEM_TYPES.Health, x= x * TILE_SIZE, y= y * TILE_SIZE)                   
                        item_box_group.add(item_box)
                    # exit
                    elif tile == 20:
                        exit = Exit(img= img, x= x * TILE_SIZE, y= y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 25:
                        girl = Girl.Girl(x=x*TILE_SIZE, y=y*TILE_SIZE + 5, scale=1, world=self)
                        npc_group.add(girl)
                    else:
                        pass
        return player, health_bar

    def setScreenScroll(self, screen_scroll):
        self.screen_scroll = screen_scroll
        for enemy in enemy_group:
            enemy.rect.x += self.screen_scroll
        for item in item_box_group:
            item.rect.x += self.screen_scroll
        for dec in decoration_group:
            dec.rect.x += self.screen_scroll
        for water in water_group:
            water.rect.x += self.screen_scroll
        for exit in exit_group:
            exit.rect.x += self.screen_scroll
        for girl in npc_group:
            girl.rect.x += self.screen_scroll
            
    def setBgScroll(self, bg_scroll):
        self.bg_scroll = bg_scroll

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += self.screen_scroll
            SCREEN.blit(tile[0], tile[1])
