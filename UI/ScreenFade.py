from turtle import color
import pygame
from consts import *

class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.update_time = pygame.time.get_ticks()
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(SCREEN, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2 , SCREEN_HEIGHT))
            pygame.draw.rect(SCREEN, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(SCREEN, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(SCREEN, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        elif self.direction == 2:
            pygame.draw.rect(SCREEN, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        # print(self.fade_counter)

        return fade_complete