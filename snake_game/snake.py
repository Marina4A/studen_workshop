from random import randint
import pygame
from eat import Eat
from pygame.sprite import Sprite

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Snake(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.rect = ai_game.rect
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self._set_start_position()
        self.tail = [Eat(self.color, self.x, self.y)]
        self.max_lenght = 1
        self.speed_x, self.speed_y = 0, 0
        self.up()

    def get_ls_coord(self):
        res_ls_coord = []
        for tail in self.tail:
            res_ls_coord.append((tail.x, tail.y))
        return res_ls_coord

    def _set_start_position(self):
        x0, y0, w, h = self.rect
        w, h = w - 2, h - 2
        x = (w // self.settings.size) // 2
        y = (h // self.settings.size) // 2
        self.x = x * self.settings.size + x0 + 1
        self.y = y * self.settings.size + y0 + 1

    def left(self):
        if self.speed_x == 0:
            self.speed_x = -1 * self.settings.size
            self.speed_y = 0

    def right(self):
        if self.speed_x == 0:
            self.speed_x = self.settings.size
            self.speed_y = 0

    def down(self):
        if self.speed_y == 0:
            self.speed_x = 0
            self.speed_y = self.settings.size

    def up(self):
        if self.speed_y == 0:
            self.speed_x = 0
            self.speed_y = -1 * self.settings.size

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        x0, y0 = self.rect.x, self.rect.y
        x1, y1 = self.rect.bottomright
        if self.x <= x0:
            self.x = x1 - self.settings.size - 1
        elif self.x > x1 - self.settings.size - 1:
            self.x = x0 + 1

        if self.y <= y0:
            self.y = y1 - self.settings.size - 1
        elif self.y > y1 - self.settings.size - 1:
            self.y = y0 + 1

        self.tail.append(Eat(self.color, self.x, self.y))
        if len(self.tail) > self.max_lenght:
            self.tail.pop(0)

    def blitme(self):
        for tail in self.tail:
            rect = pygame.Rect((tail.x, tail.y, self.settings.size, self.settings.size))
            pygame.draw.rect(surface=self.screen, color=tail.color, rect=rect)
