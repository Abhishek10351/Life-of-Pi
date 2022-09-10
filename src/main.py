import arcade

from config import (ASSET_PATH, MUSIC_VOLUME, SCREEN_HEIGHT, SCREEN_TITLE,
                    SCREEN_WIDTH)
from window import Menu, Window, WinLooseMenu

if __name__ == '__main__':
    game = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = Menu(game)
    win_loose = WinLooseMenu(game)
    game.show_view(menu)
    music = arcade.Sound(str(ASSET_PATH / "music" / "frontier.ogg"))
    music.play(MUSIC_VOLUME, loop=True)
    arcade.run()
