import pygame
import os

from Projectiles import Rock

from consts import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, nr_of_bullet, rocks, world):
        super(Player, self).__init__()
        self.alive = True
        self.speed = speed
        self.nr_of_bullet = nr_of_bullet
        self.start_nr_of_bullet = nr_of_bullet
        self.shoot_cooldown = 0
        self.rocks = rocks
        self.max_rocks = rocks
        self.flowers = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.world = world
        self.can_move = True

        animation_types = ['Idle', 'Run', "Jump", "Death"]
        for animation in animation_types:
            temp_list = []
            #count nr of files in the folder
            num_of_frames = len(os.listdir(f'img/Boy/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/Boy/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        screen_sc = 0
        level_complete = False
        if self.can_move:

            dx = 0
            dy = 0

            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1
            if self.jump == True and self.in_air == False:
                self.vel_y = -11
                self.jump = False
                self.in_air = True

            #gravity
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

            #check for collision
            for tile in self.world.obstacle_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in the y dir
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground, jump
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    # check if above the ground, falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom

            #player collide with water
            if pygame.sprite.spritecollide(self, water_group, False):
                self.health = 0

            #collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                level_complete = True

            #player fall 
            if self.rect.bottom > SCREEN_HEIGHT:
                self.health = 0

            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

            self.rect.x += dx
            self.rect.y += dy
            #update scroll base on player pos
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and self.world.bg_scroll < (self.world.level_length * TILE_SIZE) - SCREEN_WIDTH) or (self.rect.left < SCROLL_THRESH and self.world.bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_sc = -dx
        return screen_sc, level_complete

    def throwRock(self):
        rock = Rock.Rock(
            self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), \
            self.rect.centery, self.direction, self)
        self.rocks -= 1
        rock_sound.play()
        return rock

    def update_animation(self):
        if self.can_move == False:
            self.action = 0
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.rect = pygame.Rect(0, 0, 0, 0)
                self.kill()
            else:
                self.frame_index = 0
                self.draw()
        else:
            self.draw()

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3) # running death action

    def pick_up(self, item):
        if item.item_type == ITEM_TYPES.Health:
            self.health += 25
            if self.health > self.max_health:
                self.health = self.max_health
        elif item.item_type == ITEM_TYPES.Rock:
            self.rocks += 5
        elif item.item_type == ITEM_TYPES.Rose:
            self.flowers += 1

    def hit_by(self, projectile):
        self.health -= projectile.damage

    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(screen, RED, self.rect, 1)
    
    def get_rect(self):
        return self.rect
