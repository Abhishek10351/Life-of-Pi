import arcade
import arcade.gui

from config import ASSET_PATH, STYLE_GOLDEN_TANOI, CAMERA_MOVEMENT_SPEED
from ressource_manager import RessourceManager

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

        self.game_scene: arcade.Scene = None
        self.tile_sprite_list: arcade.SpriteList = None

        self.camera_sprite = None
        self.physics_engine = None
        self.camera: arcade.Camera = None
        
        self.ressource_manager = RessourceManager()
                                  

    def on_show_view(self):
        """Called when the current is switched to this view."""
        self.setup()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.game_scene = arcade.Scene()
        self.game_scene.add_sprite_list("Tiles")

        self.camera = arcade.Camera(self.main_window.width, self.main_window.height)

        for i in range(25, 800, 50):
            for j in range(25, 600, 50):
                tile = arcade.Sprite(str(ASSET_PATH / "tiles" / "land.png"))
                tile.center_x = i
                tile.center_y = j
                self.game_scene.add_sprite("Tiles", tile)

        self.camera_sprite = arcade.Sprite(str(ASSET_PATH / "utils" / "camera.png"))
        self.camera_sprite.center_x = 400
        self.camera_sprite.center_y = 300
        self.game_scene.add_sprite("Camera", self.camera_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.camera_sprite, gravity_constant=0)

    def on_draw(self):
        """Render the screen."""
        self.clear()

        self.camera.use()

        self.game_scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.camera_sprite.change_y = CAMERA_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.camera_sprite.change_y = -CAMERA_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.camera_sprite.change_x = -CAMERA_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.camera_sprite.change_x = CAMERA_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.camera_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.camera_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.camera_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.camera_sprite.change_x = 0

    def center_camera_to_camera(self):
        screen_center_x = self.camera_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.camera_sprite.center_y - (self.camera.viewport_height / 2)

        camera_centered = screen_center_x, screen_center_y
        self.camera.move_to(camera_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""
        self.physics_engine.update()
        # Position the camera
        self.center_camera_to_camera()
