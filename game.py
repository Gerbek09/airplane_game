"""Основной игровой виджет — вся логика и отрисовка."""

import random
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from settings import (
    PLAYER_SHOOT_INTERVAL, ENEMY_SPAWN_INTERVAL_BASE,
    ENEMY_SPAWN_INTERVAL_MIN, SCORE_PER_LEVEL,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    COLOR_BG, COLOR_STAR, COLOR_HUD, COLOR_HUD_WARN,
    COLOR_GAMEOVER, COLOR_BUTTON, FRAME_DT,
    BONUS_DURATION,
)
from player import Player
from bullet import Bullet
from enemy import Enemy
from bonus import Bonus
from explosion import Explosion


class GameWidget(Widget):
    score = NumericProperty(0)
    level = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.game_over = False

        # Стартовое состояние
        self.player = None
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.bonuses = []
        self.explosions = []
        self.stars = []

        # Таймеры
        self.spawn_timer = 0
        self.game_time = 0
        self.update_event = None

        # Фон-звёзды
        self.init_stars()

        self.start_game()

    # ---------- Звёздный фон ----------
    def init_stars(self):
        self.stars = []
        for _ in range(60):
            self.stars.append({
                "x": random.uniform(0, Window.width),
                "y": random.uniform(0, Window.height),
                "speed": random.uniform(30, 150),
                "size": random.choice([1, 1, 2]),
                "alpha": random.uniform(0.3, 0.9),
            })

    def update_stars(self, dt):
        for s in self.stars:
            s["y"] -= s["speed"] * dt
            if s["y"] < 0:
                s["y"] = Window.height
                s["x"] = random.uniform(0, Window.width)

    # ---------- Игра ----------
    def start_game(self):
        self.canvas.clear()
        self.clear_widgets()

        self.player = Player(Window.width / 2 - 25, 100)
        self.bullets.clear()
        self.enemy_bullets.clear()
        self.enemies.clear()
        self.bonuses.clear()
        self.explosions.clear()

        self.score = 0
        self.level = 1
        self.spawn_timer = 0.5
        self.game_time = 0
        self.game_over = False

        # HUD
        self.score_label = Label(
            text="Очки: 0", pos=(20, Window.height - 50),
            font_size='22sp', color=COLOR_HUD,
        )
        self.lives_label = Label(
            text="❤️❤️❤️", pos=(Window.width - 140, Window.height - 50),
            font_size='22sp', color=COLOR_HUD_WARN,
        )
        self.level_label = Label(
            text="Уровень: 1",
            pos=(Window.width / 2 - 60, Window.height - 50),
            font_size='20sp', color=(0.9, 0.9, 0.4, 1),
        )
        self.bonus_label = Label(
            text="", pos=(20, Window.height - 85),
            font_size='18sp', color=(0.4, 1, 0.6, 1),
        )
        self.add_widget(self.score_label)
        self.add_widget(self.lives_label)
        self.add_widget(self.level_label)
        self.add_widget(self.bonus_label)

        if self.update_event:
            self.update_event.cancel()
        self.update_event = Clock.schedule_interval(self.update, FRAME_DT)

    def end_game(self):
        self.game_over = True
        if self.update_event:
            self.update_event.cancel()

        self.add_widget(Label(
            text="💥 ИГРА ОКОНЧЕНА",
            font_size='32sp', color=COLOR_GAMEOVER,
            pos=(Window.width / 2 - 140, Window.height / 2 + 60),
        ))
        self.add_widget(Label(
            text=f"Очки: {self.score}",
            font_size='28sp', color=COLOR_HUD,
            pos=(Window.width / 2 - 60, Window.height / 2),
        ))
        btn = Button(
            text="Играть снова",
            size_hint=(None, None), size=(200, 60),
            pos=(Window.width / 2 - 100, Window.height / 2 - 100),
            background_color=COLOR_BUTTON,
        )
        btn.bind(on_press=lambda *_: self.start_game())
        self.add_widget(btn)

    # ---------- Обновление кадра ----------
    def update(self, dt):
        if self.game_over:
            return

        self.game_time += dt
        self.update_stars(dt)
        self.player.update(dt)

        # Сложность: частота спавна растёт со временем и уровнем
        base = max(
            ENEMY_SPAWN_INTERVAL_MIN,
            ENEMY_SPAWN_INTERVAL_BASE - self.level * 0.06 - self.game_time * 0.003,
        )
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = base * random.uniform(0.8, 1.2)

        # Стрельба игрока
        if self.player.can_shoot():
            self.player_shoot()
            self.player.shoot_timer = PLAYER_SHOOT_INTERVAL

        # Обновление всех объектов
        for b in self.bullets:
            b.update(dt)
        for b in self.enemy_bullets:
            b.update(dt)
        for e in self.enemies:
            e.update(dt)
            if e.can_shoot():
                self.enemy_shoot(e)
        for b in self.bonuses:
            b.update(dt)
        for ex in self.explosions:
            ex.update(dt)

        # Столкновения
        self.check_collisions()

        # Чистка
        self.bullets = [b for b in self.bullets if b.alive]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]
        self.enemies = [e for e in self.enemies if e.alive]
        self.bonuses = [b for b in self.bonuses if b.alive]
        self.explosions = [e for e in self.explosions if e.alive]

        # HUD
        self.score_label.text = f"Очки: {self.score}"
        hearts = "❤️" * max(0, self.player.lives)
        self.lives_label.text = hearts if hearts else "🖤"
        self.level_label.text = f"Уровень: {self.level}"

        # Таймеры бонусов
        active = []
        if self.player.triple_timer > 0:
            active.append(f"3x {self.player.triple_timer:.1f}с")
        if self.player.shield_timer > 0:
            active.append(f"Щит {self.player.shield_timer:.1f}с")
        self.bonus_label.text = " | ".join(active)

        self.draw()

    # ---------- Стрельба ----------
    def player_shoot(self):
        cx = self.player.x + self.player.w / 2 - 3
        cy = self.player.y + self.player.h
        if self.player.triple_timer > 0:
            # Тройной выстрел — три пули веером
            self.bullets.append(Bullet(cx, cy, friendly=True))
            self.bullets.append(Bullet(cx - 14, cy - 6, friendly=True))
            self.bullets.append(Bullet(cx + 14, cy - 6, friendly=True))
        else:
            self.bullets.append(Bullet(cx, cy, friendly=True))

    def enemy_shoot(self, enemy):
        self.enemy_bullets.append(Bullet(
            enemy.x + enemy.w / 2 - 3, enemy.y, friendly=False,
        ))
        enemy.shoot_timer = random.uniform(2.0, 4.0)

    # ---------- Спавн ----------
    def spawn_enemy(self):
        x = random.uniform(10, Window.width - 60)
        kind = Enemy.pick_random_kind(self.level)
        self.enemies.append(Enemy(x, Window.height + 20, kind=kind))

    # ---------- Столкновения ----------
    @staticmethod
    def overlap(a, b):
        return (a.x < b.x + b.w and a.x + a.w > b.x and
                a.y < b.y + b.h and a.y + a.h > b.y)

    def check_collisions(self):
        # Пули игрока vs враги
        for bullet in self.bullets:
            if not bullet.alive:
                continue
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                if self.overlap(bullet, enemy):
                    bullet.alive = False
                    killed = enemy.hit()
                    if killed:
                        self.on_enemy_killed(enemy)
                    break

        # Вражеские пули vs игрок
        if self.player.alive:
            for bullet in self.enemy_bullets:
                if not bullet.alive:
                    continue
                if self.overlap(bullet, self.player):
                    bullet.alive = False
                    if self.player.take_hit():
                        if not self.player.alive:
                            self.end_game()

        # Враги vs игрок
        if self.player.alive:
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                if self.overlap(enemy, self.player):
                    enemy.alive = False
                    self.explosions.append(
                        Explosion(enemy.x + enemy.w / 2, enemy.y + enemy.h / 2)
                    )
                    if self.player.take_hit():
                        if not self.player.alive:
                            self.end_game()

        # Бонусы vs игрок
        if self.player.alive:
            for bonus in self.bonuses:
                if not bonus.alive:
                    continue
                if self.overlap(bonus, self.player):
                    bonus.alive = False
                    self.apply_bonus(bonus.kind)

    def on_enemy_killed(self, enemy):
        self.score += enemy.score_value
        cx = enemy.x + enemy.w / 2
        cy = enemy.y + enemy.h / 2

        # Взрыв
        self.explosions.append(Explosion(cx, cy, color=enemy.color))

        # Бонус
        drop = Bonus.maybe_spawn(cx - 16, cy - 16)
        if drop:
            self.bonuses.append(drop)

        # Уровень
        new_level = self.score // SCORE_PER_LEVEL + 1
        if new_level > self.level:
            self.level = new_level

    def apply_bonus(self, kind):
        if kind == "triple_shot":
            self.player.triple_timer = BONUS_DURATION["triple_shot"]
        elif kind == "shield":
            self.player.shield_timer = BONUS_DURATION["shield"]
        elif kind == "extra_life":
            self.player.lives = min(5, self.player.lives + 1)

    # ---------- Управление ----------
    def move_player(self, x, y):
        self.player.x = max(
            0, min(Window.width - self.player.w, x - self.player.w / 2)
        )
        self.player.y = max(
            0, min(Window.height - self.player.h, y - self.player.h / 2)
        )

    def on_touch_down(self, touch):
        if self.game_over:
            return super().on_touch_down(touch)
        # Смещение, чтобы палец не закрывал самолёт на телефоне
        self.move_player(touch.x, touch.y + 60)
        return True

    def on_touch_move(self, touch):
        if self.game_over or not self.player.alive:
            return
        self.move_player(touch.x, touch.y + 60)

    def on_key_down(self, window, key, *args):
        if self.game_over or not self.player:
            return
        step = 30
        if key in (276, 97):     # ← / A
            self.player.x = max(0, self.player.x - step)
        elif key in (275, 100):  # → / D
            self.player.x = min(Window.width - self.player.w, self.player.x + step)
        elif key in (273, 119):  # ↑ / W
            self.player.y = min(Window.height - self.player.h, self.player.y + step)
        elif key in (274, 115):  # ↓ / S
            self.player.y = max(0, self.player.y - step)

    # ---------- Отрисовка ----------
    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Фон
            Color(*COLOR_BG)
            Rectangle(pos=(0, 0), size=(Window.width, Window.height))

            # Звёзды
            for s in self.stars:
                Color(1, 1, 1, s["alpha"])
                Rectangle(
                    pos=(s["x"], s["y"]),
                    size=(s["size"], s["size"]),
                )

            # Объекты
            for bonus in self.bonuses:
                bonus.draw()
            for enemy in self.enemies:
                enemy.draw()
            for bullet in self.bullets:
                bullet.draw()
            for bullet in self.enemy_bullets:
                bullet.draw()
            if self.player.alive:
                self.player.draw()
            for exp in self.explosions:
                exp.draw()