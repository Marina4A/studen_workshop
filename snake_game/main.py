import random
import pygame
import sys
from settings import Settings
from snake import Snake


class Workspace:
    """
    Рабочее пространство
    """

    def __init__(self):
        pygame.init()  # создание рабочего пространства (дисплей)
        self.settings = Settings()  # настройки дисплея
        self.clock = pygame.time.Clock()  # ограничение FPS
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self._gen_frame()
        self._restart()

    def run(self):
        """Запуск основного цикла игры."""
        while True:
            self.clock.tick(self.settings.FPS)  # ограничение выполнения цикла в секунду
            self._check_events()  # обработка событий: нажатия клавиш, закрытия диспелея
            if self.status:
                self.snake.update()  # перемещение змейки
                if self._check_dtp():
                    self.status = False
                self._check_eat()
            self._gen_frame()
            self._update_screen()  # отрисовка

    def _check_dtp(self):
        coords = self.snake.x, self.snake.y
        if coords in self.snake.get_ls_coord()[:-1]:
            return True

    def _check_eat(self):
        if (self.snake.x, self.snake.y) == self.food:
            self._create_food()
            self.snake.max_lenght += 1
            pygame.display.set_caption(str(self.snake.max_lenght-1))  # имя дисцплея

    def _restart(self):
        self.snake = Snake(self)  # создание объекта "змейка"
        self._create_food()
        self.status = True
        pygame.display.set_caption('0')

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     mouse_pos = pygame.mouse.get_pos()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == 1073741906:
            self.snake.up()
        elif event.key == 1073741903:
            self.snake.right()
        elif event.key == 1073741905:
            self.snake.down()
        elif event.key == 1073741904:
            self.snake.left()
        elif event.key == 32:
            self._restart()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        pass

    def _gen_frame(self):
        '''Определяет границы игры'''
        h = self.settings.screen_height // self.settings.size - 2
        if h % 2 == 0:
            h -= 1
        frame_y = h * self.settings.size

        w = self.settings.screen_width // self.settings.size - 2
        if w % 2 == 0:
            w -= 1
        frame_x = w * self.settings.size

        y0 = (self.settings.screen_height - frame_y) // 2
        x0 = (self.settings.screen_width - frame_x) // 2
        self.rect = pygame.Rect((x0, y0, frame_x + 2, frame_y + 2))

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        self._draw_frame()
        self._draw_food()
        self.snake.blitme()
        pygame.display.flip()

    def _create_food(self):
        '''Определяет координаты новой еды'''
        x0, y0 = self.rect.x + 1, self.rect.y + 1
        x1, y1 = map(lambda x: x - self.settings.size, self.rect.bottomright)
        res_ls_coords = []
        for line in range(x0, x1, self.settings.size):
            for row in range(y0, y1, self.settings.size):
                res_ls_coords.append((line, row))
        self.food = random.choice(tuple(set(res_ls_coords) - set(self.snake.get_ls_coord())))

    def _draw_food(self):
        '''Отрисовывает еду'''
        pygame.draw.rect(self.screen, (100, 100, 100), (*self.food, self.settings.size, self.settings.size))

    def _draw_frame(self):
        '''Отрисовыаем поле игры'''
        pygame.draw.rect(rect=self.rect, color=(255, 255, 255), surface=self.screen, width=1)


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    workspace = Workspace()
    workspace.run()
