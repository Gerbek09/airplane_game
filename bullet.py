"""Пули — и игрока, и врагов."""

from kivy.core.window import Window
from settings import (
    BULLET_W, BULLET_H, BULLET_SPEED, ENEMY_BULLET_SPEED,
    COLOR_BULLET_PLAYER, COLOR_BULLET_ENEMY,
)
from kivy.graphics import Color, Rectangle


class Bullet:
    def __init__(self, x, y, friendly=True):
        self.x = x
        self.y = y
        self.w = BULLET_W
        self.h = BULLET_H
        self.friendly = friendly
        self.alive = True

    def update(self, dt):
        if self.friendly:
            self.y += BULLET_SPEED * dt
            if self.y > Window.height + 20:
                self.alive = False
        else:
            self.y -= ENEMY_BULLET_SPEED * dt
            if self.y < -20:
                self.alive = False

    def draw(self):
        Color(*(COLOR_BULLET_PLAYER if self.friendly else COLOR_BULLET_ENEMY))
        Rectangle(pos=(self.x, self.y), size=(self.w, self.h))