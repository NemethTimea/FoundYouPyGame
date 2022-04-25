import pygame

import World

from UI import ScreenFade

from consts import *
from helpers import *




class Game():
    def __init__(self) -> None:
        self.intro_fade = ScreenFade.ScreenFade(1, BLACK, 4)
        self.death_fade = ScreenFade.ScreenFade(2, PINK, 4)
        self.win_fade = ScreenFade.ScreenFade(2, YELLOW, 4)

        self.start_intro = False
        self.start_win = False

        self.level = 1
        self.world = World.World()
        self.world_data = self.world.load_level(self.level)
        self.player, self.health_bar = self.world.process_data(self.world_data)

        self.screen_scroll = 0
        self.bg_scroll = 0

        self.moving_left = False
        self.moving_right = False
        self.already_fired = False
        self.throw_rock = False
        self.rock_thrown = False
        
        self.intro_started = 0

    def start(self):
        self.start_intro = True

    def update(self):
        if self.intro_started == 2:
            self.__draw_screen()
            self.__update_groups()
            self.__draw_groups()
            self.__handle_enemies()

    def handle_game(self):
        if self.intro_started == 2:
            if self.player.alive:
                self.__handle_player_alive()
            else:
                self.__handle_player_dead()
            
    def handle_fades(self):
        if self.start_intro == True:
            self.intro_started = 1
            if self.intro_fade.fade():
                self.start_intro = False
                self.intro_fade.fade_counter = 0
                self.intro_started = 2
        
        if self.start_win == True:
            self.player.can_move = False
            if self.win_fade.fade():
                SCREEN.blit(WIN, (SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 200))
                SCREEN.blit(BOUQUET, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 25))

    def handle_collides(self):
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
                        self.start_win = True

    def __handle_player_alive(self):
        if self.throw_rock and self.rock_thrown == False and self.player.rocks > 0:
            rock_group.add(self.player.throwRock())
            self.rock_thrown = True
        if self.player.in_air:
            self.player.update_action(2)
        elif self.moving_left or self.moving_right:
            self.player.update_action(1)
        else:
            self.player.update_action(0)
        self.screen_scroll, level_complete = self.player.move(self.moving_left, self.moving_right)
        self.world.setScreenScroll(self.screen_scroll)
        self.bg_scroll -= self.screen_scroll
        self.world.setBgScroll(self.bg_scroll)
        #check if player completed the level
        if level_complete:
            self.start_intro = True
            self.intro_started = 0
            self.level += 1
            self.bg_scroll = 0
            self.world.setBgScroll(self.bg_scroll)
            reset_world(self.world)
            if self.level <= MAX_LEVELS:
                self.world_data = self.world.load_level(self.level)
                self.player, self.health_bar = self.world.process_data(self.world_data)

    def __handle_player_dead(self):
        self.screen_scroll = 0
        self.world.setScreenScroll(self.screen_scroll)
        if self.death_fade.fade():
            SCREEN.blit(GAME_OVER, (SCREEN_WIDTH // 2 - 350, SCREEN_HEIGHT // 2 - 200))
            exit_button = Button.Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 25, BUTTON_EXIT, 0.85)
            if exit_button.draw(SCREEN):
                return False
            if restart_button.draw(SCREEN):
                self.death_fade.fade_counter = 0
                self.start_intro = True
                level = 1
                self.bg_scroll = 0
                self.world.setBgScroll(self.bg_scroll)
                reset_world(self.world)
                self.world_data = self.world.load_level(level)
                self.player, self.health_bar = self.world.process_data(self.world_data)

    def __update_groups(self):
        player_group.update()
        bullet_group.update()
        rock_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        npc_group.update()

    def __draw_groups(self):
        bullet_group.draw(SCREEN)
        rock_group.draw(SCREEN)
        item_box_group.draw(SCREEN)
        decoration_group.draw(SCREEN)
        water_group.draw(SCREEN)
        exit_group.draw(SCREEN)

    def __draw_screen(self):
        #update background 
        draw_bg(self.bg_scroll)
        #draw world map
        self.world.draw()
        self.health_bar.draw(self.player.health)
        draw_text(SCREEN, "ROCKS: ", FONT, WHITE, 10, 35)
        for x in range(self.player.rocks):
            if x > self.player.max_rocks - 1:
                draw_text(SCREEN, "(10+)", FONT, WHITE, 350, 35)
                break
            else:
                SCREEN.blit(ROCK_IMG, (95 + (x * 25), 40))

        draw_text(SCREEN,"ROSE: ", FONT, BLACK, 10, 100)
        for x in range(self.player.flowers):
            SCREEN.blit(ROSE, (90 + (x * 25), 100))

    def __handle_enemies(self):
        for enemy in enemy_group:
            enemy.ai(self.player)
            if enemy.shoot_now and enemy.can_shoot() and enemy.alive:
                bullet_group.add(enemy.shoot(self.player))
            enemy.update()
            enemy.draw()
