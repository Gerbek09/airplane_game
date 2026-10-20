[app]
title = AirBattle
package.name = airbattle
package.domain = org.gerbek
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# КРИТИЧНО: Фиксируем Python 3.11, чтобы не тянуло 3.14
# Убрали pyjnius из списка, чтобы p4a собрал его сам через свой рецепт
requirements = python3==3.11.5, hostpython3==3.11.5, kivy==2.3.1

orientation = portrait
fullscreen = 1
presplash.color = 0,0,0,1

[buildozer]
log_level = 2
warn_on_root = 1

# --- Android ---
android.api = 31
android.minapi = 21
android.ndk = 23b
# Оставляем только 64-битную архитектуру, чтобы сэкономить память и время
android.archs = arm64-v8a
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# --- Python for Android ---
p4a.branch = master
p4a.bootstrap = sdl2

# КРИТИЧНО: Заставляем p4a использовать старый pip, который не ломает open_rich_spinner
android.pip = pip==23.3.2
p4a.pip_version = 23.3.2
