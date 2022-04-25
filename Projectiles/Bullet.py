import pygame, math

import World

from consts import *

class Bullet(pygame.sprite.Sprite):
    def __init__(
            self,
            start_x,
            start_y,
            destination_x,
            destination_y
    ):
        pygame.sprite.Sprite.__init__(self)
        self.damage = 5
        self.speed = 10
        self.image = BULLET_IMG
        self.rect = self.image.get_rect()
        # self.rect.center = (start_x, start_y)
        self.rect.x = start_x
        self.rect.y = start_y
        self.current_x = start_x
        self.current_y = start_y
        
        x_diff = destination_x - start_x
        y_diff = destination_y - start_y
        angle = math.atan2(y_diff, x_diff)
        
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

    def update(self):
        #bullet move
        self.current_x += self.change_x
        self.current_y += self.change_y
        
        self.rect.x = int(self.current_x)
        self.rect.y = int(self.current_y)
        
        #check if bullet gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        #check for collision with level
        for tile in World.World.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
