import arcade
import arcade.gui

from config import ASSET_PATH, STYLE_GOLDEN_TANOI

arcade.load_font(str(ASSET_PATH / "fonts" / "DiloWorld-mLJLv.ttf"))


class Menu(arcade.View):
    """
    Menu view.

    :param main_window: Main window in which the view is shown.
    """

    def __init__(self, main_window: arcade.Window):
        super().__init__(main_window)
        self.main_window = main_window

        self.v_box = None
        self.v_box_heading = None

        self.manager = None

    def on_show_view(self) -> None:
        """Called when the current is switched to this view."""
        self.setup()

    def setup(self) -> None:
        """Set up the game variables. Call to re-start the game."""
        self.v_box = arcade.gui.UIBoxLayout(space_between=30)
        self.v_box_heading = arcade.gui.UIBoxLayout()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        play_button = arcade.gui.UIFlatButton(text="Play", width=200, style=STYLE_GOLDEN_TANOI)
        play_button.on_click = self._on_click_play_button
        create_lobby_button = arcade.gui.UIFlatButton(text="Exit", width=200, style=STYLE_GOLDEN_TANOI)
        create_lobby_button.on_click = self._on_click_exit_button

        self.v_box.add(play_button)
        self.v_box.add(create_lobby_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=self.v_box
            )
        )

    def on_draw(self) -> None:
        """Called when this view should draw."""
        self.clear()

        self.manager.draw()

    def _on_click_play_button(self, _: arcade.gui.UIOnClickEvent) -> None:
        game = Game(self.main_window)
        self.main_window.show_view(game)

    def _on_click_exit_button(self,  _: arcade.gui.UIOnClickEvent) -> None:
        self.main_window.close()
        arcade.exit()


class Game(arcade.View):
    """
    Main game logic goes here.

    :param main_window: Main window in which it showed.
    """
    def __init__(self, main_window: arcade.Window):
        super().__init__(main_window)
        self.main_window = main_window

    def on_draw(self):
        self.clear()
