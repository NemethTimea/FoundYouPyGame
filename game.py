import pygame
import csv
from UI.ScreenFade import ScreenFade

import World
from consts import *
from helpers import *

pygame.init()
pygame.display.set_caption("Founder")

clock = pygame.time.Clock()

level = 1
start_game = False
start_intro = False
start_win = False

moving_left = False
moving_right = False
already_fired = False
rock = False
rock_thrown = False

intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)
win_fade = ScreenFade(3, YELLOW, 4)

#create empty tile list
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

world = World.World()
player, health_bar = world.process_data(world_data)
screen_scroll = 0
bg_scroll = 0

run = True
yes = 0
while run:
    clock.tick(FPS)
    if start_game == False:
        #draw menu
        SCREEN.fill(BG)
        if start_button.draw(SCREEN):
            start_game = True
            start_intro = True
        if exit_button.draw(SCREEN):
            run = False
    else:
        #update background 
        draw_bg(bg_scroll)
        #draw world map
        world.draw()
        health_bar.draw(player.health)
        draw_text(SCREEN,"ROCKS: ", FONT, WHITE, 10, 35)
        for x in range(player.rocks):
            if x > player.max_rocks - 1:
                draw_text(SCREEN, "(10+)", FONT, WHITE, 350, 35)
                break
            else:
                SCREEN.blit(ROCK_IMG, (95 + (x * 25), 40))

        draw_text(SCREEN,"ROSE: ", FONT, BLACK, 10, 100)
        for x in range(player.flowers):
            SCREEN.blit(ROSE, (90 + (x * 25), 100))

        player_group.update()

        bullet_group.update()
        rock_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        npc_group.update()

        bullet_group.draw(SCREEN)
        rock_group.draw(SCREEN)
        item_box_group.draw(SCREEN)
        decoration_group.draw(SCREEN)
        water_group.draw(SCREEN)
        exit_group.draw(SCREEN)

        for enemy in enemy_group:
            enemy.ai(player)
            if enemy.shoot_now and enemy.can_shoot() and enemy.alive:
                bullet_group.add(enemy.shoot(player))
            enemy.update()
            enemy.draw()

        #show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0
        
        if start_win == True:
            win_fade.direction = 2
            if win_fade.fade():
                SCREEN.blit(WIN, (0, 0))

        if player.alive:
            if rock and rock_thrown == False and player.rocks > 0:
                rock_group.add(player.throwRock())
                rock_thrown = True
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            world.setScreenScroll(screen_scroll)
            bg_scroll -= screen_scroll
            world.setBgScroll(bg_scroll)
            #check if player completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world.setBgScroll(bg_scroll)
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f"API/level{level}_data.csv", newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World.World()
                    # world_data = world.load_level(level)
                    player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0
            world.setScreenScroll(screen_scroll)
            if death_fade.fade():
                SCREEN.blit(GAME_OVER, (SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 200))
                exit_button = Button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 25, BUTTON_EXIT, 0.85)
                if exit_button.draw(SCREEN):
                    run = False
                if restart_button.draw(SCREEN):
                    death_fade.fade_counter = 0
                    start_intro = True
                    level = 1
                    bg_scroll = 0
                    world.setBgScroll(bg_scroll)
                    world_data = reset_level()
                    #loading level data and create world
                    with open(f"API/level{level}_data.csv", newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World.World()
                    player, health_bar = world.process_data(world_data)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_q:
                rock = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_sound.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_q:
                rock = False
                rock_thrown = False
    
    player_hit_by_bullets = pygame.sprite.groupcollide(player_group, bullet_group, False, True)
    if player_hit_by_bullets:
        for player, bullets in player_hit_by_bullets.items():
            for bullet in bullets:
                player.hit_by(bullet)

    player_picked_up_items = pygame.sprite.groupcollide(player_group, item_box_group, False, True)
    if player_picked_up_items:
        for player, items in player_picked_up_items.items():
            for item in items:
                player.pick_up(item)

    enemy_hit_by_rocks = pygame.sprite.groupcollide(enemy_group, rock_group, False, True)
    if enemy_hit_by_rocks:
        for enemy, rocks in enemy_hit_by_rocks.items():
            if enemy.alive and len(rocks) > 0:
                for rock in rocks:
                    enemy.hit_by(rock)

    player_collide_npc = pygame.sprite.groupcollide(player_group, npc_group, False, False)
    if player_collide_npc:
        for player, npcs in player_collide_npc.items():
            for npc in npcs:
                if type(npc).__name__ == 'Girl':
                    start_win = True
    pygame.display.update()

pygame.quit()

