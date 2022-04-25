import pygame
from consts import *

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update with new health
        self.health = health

        #calc health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(SCREEN, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(SCREEN, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(SCREEN, GREEN , (self.x, self.y, 150 * ratio, 20))