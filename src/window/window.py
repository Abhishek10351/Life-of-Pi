import arcade


class Window(arcade.Window):
    """Main application class."""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.mouse_x = 0
        self.mouse_y = 0

        arcade.set_background_color(arcade.color.ANTI_FLASH_WHITE)
