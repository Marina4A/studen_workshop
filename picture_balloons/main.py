import math
import numpy as np
from PIL import Image
import pygame
import sys

from settings import Settings
from balls import Balls


class Animation:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FIREWORK")

        self.settings = Settings()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self._gen_balls()

    def run(self):
        """Запуск основного цикла игры."""
        while True:
            # Отслеживание событий клавиатуры и мыши.
            self.clock.tick(self.settings.FPS)
            self._check_events()
            self._chek_mouse()
            for balls in self.ls_balls:
                balls.update()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # elif event.type == pygame.KEYUP:
            #     self._check_keyup_events(event)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        pass

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        for balls in self.ls_balls:
            balls.blitme()
        pygame.display.flip()

    def _gen_balls(self):
        self.ls_balls = []
        center_y = self.settings.screen_height // 2
        center_x = self.settings.screen_width // 2
        img = Image.open('test.jpg')
        size_x, size_y = img.size
        h = 50
        if size_x > h:
            size_x = h
            size_y = int(size_y * h / size_x)
            img = img.resize((size_x, size_y))
        if size_y > h:
            size_y = h
            size_x = int(size_x * h / size_y)
            img = img.resize((size_x, size_y))
        arr = np.asarray(img, dtype='uint8')
        first_x = center_x - size_x//2 * 10
        first_y = center_y - size_y//2 * 10
        for index_y, line in enumerate(arr):
            for index_x, pixel in enumerate(line):
                self.ls_balls.append(Balls(self, x=first_x+index_x * 10, y=first_y+index_y * 10, color=pixel))

    def _chek_mouse(self):
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        for ball in self.ls_balls:
            pril = Mouse_x - ball.x
            prot = Mouse_y - ball.y
            rast = math.sqrt(pril ** 2 + prot ** 2)
            r = 100
            if rast < r:
                if rast == 0:
                    rast = r
                cos = pril / rast
                ugol = math.acos(cos)
                if prot > 0:
                    ball.x = int(Mouse_x - r * math.cos(ugol))
                    ball.y = int(Mouse_y - r * math.sin(ugol))
                else:
                    ball.x = int(Mouse_x - r * math.cos(ugol))
                    ball.y = int(Mouse_y + r * math.sin(ugol))


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = Animation()
    ai.run()
