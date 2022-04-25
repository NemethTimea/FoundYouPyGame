import pygame
import World

from consts import *
from helpers import *

class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner):
        pygame.sprite.Sprite.__init__(self)
        self.damage = 25
        self.speed = 7
        self.owner = owner
        self.image = ROCK_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = 100
        self.vel_y = -8
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y
        #check for collision with level
        for tile in World.World.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
             #check for collision in the y dir
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                self.kill()
                #check if below the ground, thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        #update rock position
        self.rect.x += dx
        self.rect.y += dy

