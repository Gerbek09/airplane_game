[app]

title = AirBattle
package.name = airbattle
package.domain = org.gerbek

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3, kivy==https://github.com/kivy/kivy/archive/refs/tags/2.3.1.zip

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
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.accept_sdk_license = True

# --- Python for Android ---
p4a.bootstrap = sdl2
# --- Принудительный Python 3.11 ---
