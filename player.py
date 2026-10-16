"""Самолёт игрока — движение, стрельба, щит, жизни."""

from kivy.graphics import Color, Rectangle, Triangle, Ellipse, Line
from settings import (
    PLAYER_W, PLAYER_H, PLAYER_START_LIVES, PLAYER_INVULNERABLE_TIME,
    COLOR_PLAYER, COLOR_PLAYER_DARK, COLOR_SHIELD,
)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_W
        self.h = PLAYER_H
        self.lives = PLAYER_START_LIVES
        self.alive = True

        # Таймеры
        self.shoot_timer = 0
        self.invuln_timer = 0      # неуязвимость после попадания
        self.triple_timer = 0      # бонус тройного выстрела
        self.shield_timer = 0      # бонус щита
        self.flash_timer = 0

    def update(self, dt):
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        if self.invuln_timer > 0:
            self.invuln_timer -= dt
        if self.triple_timer > 0:
            self.triple_timer -= dt
        if self.shield_timer > 0:
            self.shield_timer -= dt
        if self.flash_timer > 0:
            self.flash_timer -= dt

    def can_shoot(self):
        return self.shoot_timer <= 0 and self.alive

    def has_shield(self):
        return self.shield_timer > 0

    def is_invulnerable(self):
        return self.invuln_timer > 0 or self.has_shield()

    def take_hit(self):
        """Возвращает True, если игрок потерял жизнь."""
        if self.is_invulnerable():
            return False
        self.lives -= 1
        self.invuln_timer = PLAYER_INVULNERABLE_TIME
        self.flash_timer = 0.3
        if self.lives <= 0:
            self.alive = False
        return True

    def draw(self):
        # Мерцание в момент неуязвимости
        if self.invuln_timer > 0 and int(self.invuln_timer * 10) % 2 == 0:
            return

        x, y, w, h = self.x, self.y, self.w, self.h

        # Основной корпус
        if self.flash_timer > 0:
            Color(1, 0.5, 0.5)
        else:
            Color(*COLOR_PLAYER)
        Triangle(points=[x + w / 2, y + h, x, y, x + w, y])

        # Крылья
        Color(*COLOR_PLAYER_DARK)
        Rectangle(pos=(x - 6, y + h * 0.25), size=(w + 12, 8))

        # Кабина
        Color(1, 1, 1)
        Ellipse(pos=(x + w / 2 - 5, y + h * 0.35), size=(10, 12))

        # Хвост
        Color(*COLOR_PLAYER_DARK)
        Rectangle(pos=(x + w / 2 - 8, y - 3), size=(16, 8))

        # Щит
        if self.has_shield():
            Color(*COLOR_SHIELD)
            Line(circle=(x + w / 2, y + h / 2, w * 0.8), width=3)
            Color(*COLOR_SHIELD[:3], 0.2)
            Ellipse(pos=(x - 10, y - 10), size=(w + 20, h + 20))