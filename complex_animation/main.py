import pygame
import sys
from random import randint
from settings import Settings
from firework import Firework


class Workspace:
    """
    Создание рабочего пространства (экрана).
    Отрисовка объектов и вывод на экран.
    """

    def __init__(self):
        """
        Создание экземпляра.
        """

        pygame.init()  # создаем рабочее пространство
        pygame.display.set_caption("FIREWORK")  # название рабочего пространства (заголовок)

        self.settings = Settings()  # создание экземпляра класса - подгрузка настроек экрана
        self.clock = pygame.time.Clock()  # определяешь функцию для работы с FPS

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # размер дисплея
        self.ls_firework = [Firework(self) for _ in range(3)]  # список запуска фейерверков

    def run(self):
        """
        Запуск работы всей программы (работы фейерверков)
        """
        while True:
            # Отслеживание событий клавиатуры и мыши.
            self.clock.tick(self.settings.FPS)  # ограничение отработки цикла (кол-ва раз) в секунду
            self._check_events()  # обработка всех событий (закрытие окна при условии)
            for firework in self.ls_firework:
                if len(firework.ls_head) == 0:
                    self.ls_firework.remove(firework)  # удаляем фейерверк из списка после затухания
                    count_firework = randint(1, 5)
                    if len(self.ls_firework) < count_firework:
                        for _ in range(count_firework - len(self.ls_firework)):
                            self.ls_firework.append(Firework(self))  # добавляем новый
                else:
                    firework.update()  # смещение координаты фейерверка
            self._update_screen()  # обновляет изображение на экране

    def _check_events(self):
        """
        Закрытие рабочего окна.
        Прекращение фейерверков.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """
        Обновляет изображения на экране и отображает новый экран.
        """

        self.screen.fill(self.settings.bg_color)  # черный фон
        for firework in self.ls_firework:
            firework.blitme()  # отрисовка фейерверка
        pygame.display.flip()  # выводит дисплей


if __name__ == '__main__':  # Создание экземпляра и запуск игры.
    workspace = Workspace()
    workspace.run()
