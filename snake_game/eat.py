
from pygame.sprite import Sprite


class Eat(Sprite):
    """
    Еда змейки
    """
    def __init__(self, color, x, y):
        """
        Получение параметров
        :param color: цвет
        :param x: координата по Оси абцисс
        :param y: координата по Оси ординат
        """
        super().__init__()
        self.color = color
        self.x = x
        self.y = y

