import math
import random
from math import sin, cos
from random import randint

import pygame
from pygame.sprite import Sprite


class Balls(Sprite):

    def __init__(self, ai_game, x, y, color):
        super().__init__()
        """Инициализирует корабль и задает его начальную позицию."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.color = color

    def update(self):
        if abs(self.x - self.start_x) > self.settings.speed:
            if self.x > self.start_x:
                self.x -= self.settings.speed
            elif self.x < self.start_x:
                self.x += self.settings.speed
        else:
            self.x = self.start_x

        if abs(self.y - self.start_y) > self.settings.speed:
            if self.y > self.start_y:
                self.y -= self.settings.speed
            elif self.y < self.start_y:
                self.y += self.settings.speed
        else:
            self.y = self.start_y

    def blitme(self):
        pygame.draw.circle(self.screen, self.color, [self.x, self.y], self.settings.size, 0)
