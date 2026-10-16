"""Бонусы, которые падают сверху."""

import random
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, Line
from settings import (
    BONUS_W, BONUS_H, BONUS_FALL_SPEED, BONUS_DROP_CHANCE, BONUS_TYPES,
)

BONUS_COLORS = {
    "triple_shot": (1, 0.5, 0.1),   # оранжевый
    "shield":      (0.3, 0.9, 1),   # голубой
    "extra_life":  (1, 0.3, 0.5),   # розовый
}

BONUS_LABELS = {
    "triple_shot": "3x",
    "shield":      "S",
    "extra_life":  "♥",
}


class Bonus:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.w = BONUS_W
        self.h = BONUS_H
        self.kind = kind
        self.alive = True

    @staticmethod
    def maybe_spawn(x, y):
        """С шансом BONUS_DROP_CHANCE создаёт случайный бонус."""
        if random.random() > BONUS_DROP_CHANCE:
            return None
        kind = random.choice(BONUS_TYPES)
        return Bonus(x, y, kind)

    def update(self, dt):
        self.y -= BONUS_FALL_SPEED * dt
        if self.y < -self.h - 10:
            self.alive = False

    def draw(self):
        color = BONUS_COLORS[self.kind]
        x, y, w, h = self.x, self.y, self.w, self.h

        # Круг с обводкой
        Color(*color)
        Ellipse(pos=(x, y), size=(w, h))

        Color(1, 1, 1, 0.9)
        Line(circle=(x + w / 2, y + h / 2, w / 2 - 2), width=1.5)

        # Буква-подсказка
        Color(1, 1, 1)
        label = BONUS_LABELS[self.kind]
        # Простая "буква" — рисуем палочками
        cx, cy = x + w / 2, y + h / 2
        if label == "3x":
            Rectangle(pos=(cx - 8, cy - 2), size=(16, 4))
            Rectangle(pos=(cx - 2, cy - 8), size=(4, 16))
        elif label == "S":
            Rectangle(pos=(cx - 6, cy - 6), size=(12, 3))
            Rectangle(pos=(cx - 6, cy - 6), size=(3, 12))
            Rectangle(pos=(cx - 6, cy + 3), size=(12, 3))
        elif label == "♥":
            Rectangle(pos=(cx - 6, cy - 2), size=(5, 5))
            Rectangle(pos=(cx + 1, cy - 2), size=(5, 5))
            Rectangle(pos=(cx - 4, cy + 3), size=(8, 4))