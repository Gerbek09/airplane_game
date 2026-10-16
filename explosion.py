"""Анимация взрыва — расходящиеся круги."""

from kivy.graphics import Color, Line
from settings import EXPLOSION_DURATION, EXPLOSION_MAX_RADIUS


class Explosion:
    def __init__(self, x, y, color=(1, 0.6, 0.1)):
        self.x = x
        self.y = y
        self.t = 0
        self.duration = EXPLOSION_DURATION
        self.max_radius = EXPLOSION_MAX_RADIUS
        self.color = color
        self.alive = True

    def update(self, dt):
        self.t += dt
        if self.t >= self.duration:
            self.alive = False

    def draw(self):
        progress = min(1.0, self.t / self.duration)
        radius = self.max_radius * progress
        alpha = 1 - progress

        # Внешнее кольцо
        Color(*self.color, alpha * 0.8)
        Line(circle=(self.x, self.y, radius), width=3)

        # Внутреннее кольцо
        Color(1, 1, 0.6, alpha * 0.6)
        Line(circle=(self.x, self.y, radius * 0.6), width=2)