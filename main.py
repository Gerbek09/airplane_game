"""Точка входа — запускает игру."""

from kivy.app import App
from kivy.core.window import Window
from game import GameWidget
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class AirBattleApp(App):
    def build(self):
        self.title = "Воздушный бой 2.0"
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        Window.clearcolor = (0, 0, 0, 1)

        game = GameWidget()
        # Клавиатура (для ПК)
        Window.bind(on_key_down=game.on_key_down)
        return game


if __name__ == "__main__":
    AirBattleApp().run()