import pygame
import os

from consts import *

class Girl(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, world) -> None:
        super().__init__()

        self.action = 0
        self.frame_index = 0
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        self.world = world

        animation_types = ["Idle"]
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/Girl/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/Girl/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        # print(self.animation_list)
        # print(self.animation_list[self.action])
        # print(self.animation_list[self.action][self.frame_index])

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # print(self.rect)
        self.flip = True

    def update(self):
        ANIMATION_COOLDOWN = 200
        # print(f"Update Girl, frame_index = {self.frame_index}")
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
        self.draw()

    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # print("Drawing Girl!")
