from random import randint
import pygame
from pygame.sprite import Sprite


class Head:
    """
    Центр фейерверка, сам снаряд (самые яркие части).
    """

    def __init__(self, x, y, color, size, boom=False):
        """
        Получение параметров
        :param x: координата по Оси абциссх
        :param y: координата по Оси ординат
        :param color: цвет фейерверка
        :param size: размер шара
        :param boom: булевое значение взорвался/не взорвался
        """

        self.x = x  # текущее положение точки
        self.y = y  # текущее положение точки
        self.color = color  # цвет
        self.size = size
        self.boom = boom
        self.ttl = 0  # время жизни фейерверка
        self.ls_tail = []
        if self.boom:
            self.start_x = x  # стартовое положение точки
            self.start_y = y  # стартовое положение точки
            self.v0X = randint(-300, 300) / 20  # скорость по Х
            self.v0Y = randint(-300, 300) / 20  # скорость по Y
            distance = randint(5, 20)  # дистанция от центра
            mlen = (self.v0X ** 2 + self.v0Y ** 2) ** (
                0.5)  # Вычисляем диагональ треугольника вектора скорости до увеличения
            if mlen != 0:
                mlen = 1.0 / mlen
            # Используя теорему подобия вычисляем новые значения скоростей:
            self.v0X *= mlen * distance
            self.v0Y *= mlen * distance

    def update(self):
        """
        Смещение самой яркой части
        """
        for tail in self.ls_tail:
            tail.update()  # затухание

        if not self.boom:  # полет фейерверка вверх до взрыва
            self.y = self.y - 5
            self.ls_tail.append(Tail(self.x, self.y, self.color, self.size))  # добавили яркий хвост
        else:
            self.x += (self.v0X / 5)
            self.y += (self.v0Y / 5)
            self.ttl += 1
            if self.ttl > 15:  # количество кадров жизни фейерверка (шара)
                self.v0Y += 2
            if self.ttl < 40:
                self.ls_tail.append(Tail(self.x, self.y, self.color, self.size))

        self.ls_tail = list(filter(lambda x: sum(x.color) > 30, self.ls_tail))


class Tail:
    """
    Хвост снаряда фейерверка
    """

    def __init__(self, x, y, color, size):
        """
        Получение параметров
        :param x: координата по Оси абцисс
        :param y: координата по Оси ординат
        :param color: цвет частиц
        :param size: размер частиц
        """
        self.x = x  # текущее положение точки
        self.y = y  # текущее положение точки
        self.color = color  # цвет
        self.size = size
        self._DAMPING_FACTOR = 1.18  # коэффициент затухания (скорость)

    def update(self):
        """
        Затухание фейерверка
        """
        self.color = tuple(map(lambda x: x // self._DAMPING_FACTOR, self.color))


class Firework(Sprite):
    """
    Полноценный фейерверк
    """

    def __init__(self, workspace_game):
        """
        Получение параметров
        :param workspace_game: ссылка на рабочее пространство
        """
        super().__init__()
        self.screen = workspace_game.screen  # настройки экрана
        self.settings = workspace_game.settings  # настройки экрана
        self.x = randint(0, self.settings.screen_width)  # координаты
        self.y = self.settings.screen_height  # координаты
        self.height_firework = randint(0, self.settings.screen_height)  # высота полета фейерверка (взрыва)
        self.color = pygame.Color(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))  # цвет фейерверка
        self.boom = False  #
        self.ls_head = [Head(x=self.x, y=self.y, color=self.color, size=5)]  # список разлетающихся элементов фейерверка
        self.update()  # смещение фейеверка на экране
        self.blitme()  # отрисовка фейерверков

    def update(self):
        """
        Изменяет положение фейерверка в пространстве
        """

        for head in self.ls_head:
            head.update()
            if len(self.ls_head) == 1 and head.y <= self.height_firework:
                self.ls_head = [Head(x=self.x, y=self.height_firework, color=self.color, size=2, boom=True) for _ in
                                range(100)]
        self.ls_head = list(filter(lambda x: x.y < self.settings.screen_height, self.ls_head))  # удаляет "головы"

    def blitme(self):
        """
        Отрисовка всех частей фейерверков
        """

        firework_particles = []
        for head in self.ls_head:
            for tail in head.ls_tail:
                firework_particles.append(tail)
        for particles in firework_particles:
            pygame.draw.circle(self.screen, particles.color, [particles.x, particles.y], particles.size, 0)
