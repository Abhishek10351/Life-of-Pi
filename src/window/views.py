import math

import arcade
import arcade.gui


from config import ASSET_PATH, CAMERA_MOVEMENT_SPEED, INVERT_MOUSE, STYLE_GOLDEN_TANOI, VIEWPORT_ANGLE
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
        self.v_box_message = None

        self.manager = None

    def on_show_view(self) -> None:
        """Called when the current is switched to this view."""
        self.setup()

    def setup(self) -> None:
        """Set up the game variables. Call to re-start the game."""
        self.v_box = arcade.gui.UIBoxLayout(space_between=30)
        self.v_box_message = arcade.gui.UIBoxLayout()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        play_button = arcade.gui.UIFlatButton(
            text="Play", width=200, style=STYLE_GOLDEN_TANOI)
        play_button.on_click = self._on_click_play_button
        how_to_play_button = arcade.gui.UIFlatButton(
            text="How to Play", width=200, style=STYLE_GOLDEN_TANOI)
        how_to_play_button.on_click = self.on_click_open
        exit_button = arcade.gui.UIFlatButton(
            text="Exit", width=200, style=STYLE_GOLDEN_TANOI)
        exit_button.on_click = self._on_click_exit_button

        self.v_box.add(play_button)
        self.v_box.add(how_to_play_button)
        self.v_box.add(exit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=self.v_box
            )
        )

    def on_click_open(self, event):
        message_box = arcade.gui.UIMessageBox(
            width=400,
            height=300,
            message_text=
            """Hey Player, Welcome to Marrrs Explorer.
    You were travelling on space and after your rocket fuel finished you got stranded on Mars,
    A.K.A (The Red Planet). Now you have to wait for people from to rescue you and take you back to Earth.
    Until then you have to collect money, minerals and other stuff and use them properly to stay alive.
                """

        )
        self.v_box_message.add(message_box)
        self.manager.add(arcade.gui.UIAnchorWidget(child=self.v_box_message))

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

    def on_hide_view(self):
        self.manager.disable()


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

        self.camera = arcade.Camera(
            self.main_window.width, self.main_window.height)

        rotation_from_axis = VIEWPORT_ANGLE

        for i in range(16, 800, 32):
            for j in range(14, 600, 28):
                tile = arcade.Sprite(str(ASSET_PATH / "tiles" / "land.png"))
                tile.center_x = i*math.cos(rotation_from_axis) + j*math.sin(rotation_from_axis)
                tile.center_y = j*math.cos(rotation_from_axis) - i*math.sin(rotation_from_axis)
                self.game_scene.add_sprite("Tiles", tile)

<<<<<<< HEAD
        self.camera_sprite = arcade.Sprite(
            str(ASSET_PATH / "utils" / "camera.png"))
=======
        # this can be renamed to player sprite, if player sprite is decided to be made.
        self.camera_sprite = arcade.Sprite(str(ASSET_PATH / "utils" / "camera.png"))
>>>>>>> 6278d6372112a0efbb69a7fb1f8974764ae4b868
        self.camera_sprite.center_x = 400
        self.camera_sprite.center_y = 300
        self.game_scene.add_sprite("Camera", self.camera_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.camera_sprite, gravity_constant=0)

    def on_draw(self):
        """Render the screen."""
        self.clear()

        self.camera.use()
        self.game_scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        # using change because if it is changed to player physics engine is required.
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

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int):
        """Called when the mouse is dragged."""
        if INVERT_MOUSE:
            self.camera_sprite.center_x -= dx
            self.camera_sprite.center_y -= dy
        else:
            self.camera_sprite.center_x += dx
            self.camera_sprite.center_y += dy

    def center_camera_to_camera(self):
        screen_center_x = self.camera_sprite.center_x - \
            (self.camera.viewport_width / 2)
        screen_center_y = self.camera_sprite.center_y - \
            (self.camera.viewport_height / 2)
        """Centers camera to the camera sprite."""
        screen_center_x = self.camera_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.camera_sprite.center_y - (self.camera.viewport_height / 2)

        camera_centered = screen_center_x, screen_center_y
        self.camera.move_to(camera_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""
        self.physics_engine.update()
        # Position the camera
        self.center_camera_to_camera()
