"""Вражеские самолёты — три типа с разным поведением."""

import random
import math
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Triangle, Ellipse
from settings import ENEMY_TYPES, ENEMY_W, ENEMY_H


class Enemy:
    def __init__(self, x, y, kind="normal"):
        self.x = x
        self.y = y
        self.w = ENEMY_W
        self.h = ENEMY_H
        self.kind = kind
        self.alive = True
        self.shoot_timer = random.uniform(1.5, 3.5)
        self.zigzag_phase = random.uniform(0, math.pi * 2)

        # Ищем параметры типа
        for name, weight, hp, score, vmin, vmax, color in ENEMY_TYPES:
            if name == kind:
                self.hp = hp
                self.score_value = score
                self.speed = random.uniform(vmin, vmax)
                self.color = color
                break

        self.flash_timer = 0  # подсветка при попадании

    @staticmethod
    def pick_random_kind(level):
        """Спавним типы с весами. На высоких уровнях — больше 'tank' и 'fast'."""
        weights = []
        for name, w, *_ in ENEMY_TYPES:
            if name == "normal":
                weights.append(max(20, w - level * 5))
            elif name == "fast":
                weights.append(w + level * 3)
            elif name == "tank":
                weights.append(w + level * 2)
        return random.choices([t[0] for t in ENEMY_TYPES], weights=weights)[0]

    def update(self, dt):
        self.y -= self.speed * dt

        # "fast" летит зигзагом
        if self.kind == "fast":
            self.zigzag_phase += dt * 6
            self.x += math.sin(self.zigzag_phase) * 120 * dt
            self.x = max(0, min(Window.width - self.w, self.x))

        # Взрыв при выходе за низ
        if self.y < -self.h - 10:
            self.alive = False

        if self.flash_timer > 0:
            self.flash_timer -= dt

        self.shoot_timer -= dt

    def can_shoot(self):
        return self.shoot_timer <= 0 and self.y > 60 and self.kind != "fast"

    def hit(self):
        """Возвращает True, если враг уничтожен."""
        self.hp -= 1
        self.flash_timer = 0.08
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self):
        # Вспышка при попадании
        if self.flash_timer > 0:
            Color(1, 1, 1)
        else:
            Color(*self.color)

        x, y, w, h = self.x, self.y, self.w, self.h

        # Форма зависит от типа
        if self.kind == "tank":
            Rectangle(pos=(x, y), size=(w, h))
            Color(0, 0, 0, 0.4)
            Rectangle(pos=(x + 6, y + 6), size=(w - 12, h - 12))
            Color(1, 0.8, 0.2)
            Ellipse(pos=(x + w / 2 - 6, y + h / 2 - 6), size=(12, 12))
        else:
            # Треугольник вниз (нос направлен вниз)
            Triangle(points=[x + w / 2, y, x, y + h, x + w, y + h])
            # Крылья
            Color(*[c * 0.7 for c in self.color[:3]])
            Rectangle(pos=(x - 6, y + h * 0.6), size=(w + 12, 7))
            # Кабина
            Color(1, 1, 0.5)
            Ellipse(pos=(x + w / 2 - 5, y + h * 0.55), size=(10, 12))