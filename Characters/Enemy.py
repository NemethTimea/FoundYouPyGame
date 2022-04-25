import pygame
import os
import random

from Projectiles import Bullet

from consts import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, obstacles):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.shoot_cooldown = 0
        self.shoot_now = False
        self.health = 100
        self.max_health = 100
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        self.fired = 2000
        self.already_fired = False
        self.obstacles = obstacles

        animation_types = ['Idle', 'Run', "Jump", "Death"]
        for animation in animation_types:
            temp_list = []
            #count nr of files in the folder
            num_of_frames = len(os.listdir(f'img/Enemy/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/Enemy/{animation}/{i}.png').convert_alpha()
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
        for tile in self.obstacles:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # tourn around when hit the wall
                self.direction *= -1
                self.move_counter = 0
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

        self.rect.x += dx
        self.rect.y += dy

    def shoot(self, player):
        bullet = Bullet.Bullet(
            start_x=self.rect.centerx + (0.3 * self.rect.size[0] * self.direction), 
            start_y=self.rect.centery + (0.3 * self.rect.size[1]) - 16,
            destination_x=player.get_rect().x,
            destination_y=player.get_rect().y + 16)
        shot_sound.play()
        return bullet

    def can_shoot(self):
        FIRING_TIME = 2000
        if pygame.time.get_ticks() - self.fired < FIRING_TIME:
            self.already_fired = True
            return False
        else:
            self.fired = pygame.time.get_ticks()
            self.already_fired = False
            return True

    def ai(self, player):
        if self.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0) 
                self.idling = True
                self.idling_counter = 50
            #check if the ai in near the player
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot_now = True
            else:
                self.shoot_now = False
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    # pygame.draw.rect(SCREEN, RED, self.vision, 1)
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        if not player.alive:
            self.shoot_now = False

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
                self.kill()
            else:
                self.frame_index = 0

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

    def hit_by(self, projectile):
        self.health -= projectile.damage

    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)