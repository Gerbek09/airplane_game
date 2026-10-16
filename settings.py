"""Все настройки игры в одном месте — легко крутить баланс."""

# ---------- Окно ----------
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800
FPS = 60
FRAME_DT = 1.0 / FPS

# ---------- Игрок ----------
PLAYER_W = 50
PLAYER_H = 50
PLAYER_START_LIVES = 3
PLAYER_SHOOT_INTERVAL = 0.22       # сек между выстрелами
PLAYER_INVULNERABLE_TIME = 1.5     # неуязвимость после попадания

# ---------- Пули ----------
BULLET_W = 6
BULLET_H = 16
BULLET_SPEED = 700                 # пикселей в секунду
ENEMY_BULLET_SPEED = 400

# ---------- Враги ----------
ENEMY_SPAWN_INTERVAL_BASE = 1.0    # базовая частота спавна
ENEMY_SPAWN_INTERVAL_MIN = 0.35    # быстрее — уже некуда
ENEMY_W = 44
ENEMY_H = 44

# Типы врагов: (имя, вес_спавна, hp, очки, скорость_мин, скорость_макс, цвет)
ENEMY_TYPES = [
    ("normal", 60, 1, 10, 180, 240, (0.9, 0.2, 0.2)),    # красный
    ("fast",   25, 1, 20, 300, 380, (1.0, 0.8, 0.2)),    # жёлтый
    ("tank",   15, 3, 30, 120, 160, (0.6, 0.2, 0.8)),    # фиолетовый
]

# ---------- Бонусы ----------
BONUS_W = 32
BONUS_H = 32
BONUS_FALL_SPEED = 150
BONUS_DROP_CHANCE = 0.20           # шанс выпадения с врага
BONUS_DURATION = {                 # длительность эффекта в секундах
    "triple_shot": 10.0,
    "shield": 6.0,
    "extra_life": 0.0,             # моментальный эффект
}
BONUS_TYPES = ["triple_shot", "shield", "extra_life"]

# ---------- Уровни сложности ----------
SCORE_PER_LEVEL = 200              # каждые N очков — новый уровень

# ---------- Цвета ----------
COLOR_BG = (0.04, 0.04, 0.12)
COLOR_STAR = (1, 1, 1, 0.7)
COLOR_PLAYER = (0.3, 0.7, 1)
COLOR_PLAYER_DARK = (0.15, 0.4, 0.8)
COLOR_SHIELD = (0.4, 1.0, 0.6, 0.6)
COLOR_BULLET_PLAYER = (1, 1, 0.3)
COLOR_BULLET_ENEMY = (1, 0.55, 0.15)
COLOR_HUD = (1, 1, 1, 1)
COLOR_HUD_WARN = (1, 0.3, 0.3, 1)
COLOR_GAMEOVER = (1, 0.3, 0.3, 1)
COLOR_BUTTON = (0.2, 0.7, 0.35, 1)

# ---------- Взрывы ----------
EXPLOSION_DURATION = 0.35
EXPLOSION_MAX_RADIUS = 45