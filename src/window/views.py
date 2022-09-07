import datetime
import math
import random
import time

import arcade
import arcade.gui
from arcade.experimental.lights import LightLayer
from scipy import interpolate

from config import (ASSET_PATH, BRIGHTNESS_TIME, BRIGHTNESS_VALUE,
                    CAMERA_MOVEMENT_SPEED, CARBON_DIOXIDE_GEYSERS, CRATER,
                    DAY_TOTAL_TIME, ICY_TILE, INVERT_MOUSE, IRON_RICH_TILE,
                    LAND, STYLE_GOLDEN_TANOI, VOLCANO)
from ressource_manager import RessourceManager

from sidebar import SideBar

arcade.load_font(str(ASSET_PATH / "fonts" / "Dilo World.ttf"))


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
        how_to_play_button.on_click = self._on_click_how_to_play_button

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

    def _on_click_how_to_play_button(self, _: arcade.gui.UIOnClickEvent):
        message_box = arcade.gui.UIMessageBox(
            width=400,
            height=300,
            message_text="Hey Player, Welcome to Marrrs Explorer."
                         "You were travelling on space and after your rocket fuel finished you got stranded on Mars, "
                         "A.K.A (The Red Planet). Now you have to wait for people from to rescue you and take you"
                         "back to Earth. Until then you have to collect money, minerals and other"
                         "stuff and use them properly to stay alive.",
            callback=self._how_to_play_callback)

        self.v_box_message.add(message_box)
        self.manager.clear()
        self.manager.add(arcade.gui.UIAnchorWidget(child=self.v_box_message))

    def _how_to_play_callback(self, _: arcade.gui.UIOnClickEvent):
        self.manager.clear()
        self.manager.add(arcade.gui.UIAnchorWidget(child=self.v_box))

    def on_draw(self) -> None:
        """Called when this view should draw."""
        self.clear()

        self.manager.draw()

    def _on_click_play_button(self, _: arcade.gui.UIOnClickEvent) -> None:
        game = Game(self.main_window)
        self.main_window.show_view(game)

    def _on_click_exit_button(self, _: arcade.gui.UIOnClickEvent) -> None:
        self.main_window.close()
        arcade.exit()

    def on_hide_view(self):
        self.manager.disable()


def rect2isometric(x, y):
    """Rotates the axis by 45 degrees and then compresses the y axis by a factor of sqrt(2)."""
    iso_x_45 = x * (math.sqrt(2) / 2) + y * (math.sqrt(2) / 2)
    iso_y_45 = -x * (math.sqrt(2) / 2) + y * (math.sqrt(2) / 2)
    compress_iso_y_45 = -iso_y_45 / math.sqrt(2)
    return iso_x_45, compress_iso_y_45


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

        self.light_layer = None
        self.time = time.time()

        self.ressource_manager = RessourceManager()

        self.selected_tile = None
        self.screen_center_x = 0
        self.screen_center_y = 0
        
        self.sidebar = SideBar(self)

    def on_show_view(self):
        """Called when the current is switched to this view."""
        self.setup()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.game_scene = arcade.Scene()
        self.game_scene.add_sprite_list("Tiles")
        self.game_scene.add_sprite_list("Selected Tile")

        self.camera = arcade.Camera(
            self.main_window.width, self.main_window.height)

        # for i in range(-775, 800, 50):
        #    for j in range(-575, 600, 50):
        for i in range(-10, 10, 1):
            for j in range(-10, 10, 1):
                file_name = random.choices(["crater_iso.png", "fe_crater_iso.png", "geyser_iso.png",
                                            "ice_iso.png", "land_iso.png", "volcano_iso.png", ],
                                           [CRATER, IRON_RICH_TILE, CARBON_DIOXIDE_GEYSERS, ICY_TILE, LAND, VOLCANO])[0]
                tile = arcade.Sprite(str(ASSET_PATH / "tiles" / file_name))
                # tile.center_x = i * math.cos(rotation_from_axis) + j * math.sin(rotation_from_axis)
                # tile.center_y = j * math.cos(rotation_from_axis) - i * math.sin(rotation_from_axis)
                (tile.center_x, tile.center_y) = rect2isometric(80 * i + 40, 80 * j + 40)

                self.game_scene.add_sprite("Tiles", tile)
        self.camera_sprite = arcade.Sprite(
            str(ASSET_PATH / "utils" / "camera.png"))
        # this can be renamed to player sprite, if player sprite is decided to be made.
        self.camera_sprite = arcade.Sprite(
            str(ASSET_PATH / "utils" / "camera.png"))
        self.camera_sprite.center_x = 400
        self.camera_sprite.center_y = 300
        self.game_scene.add_sprite("Camera", self.camera_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.camera_sprite, gravity_constant=0)

        self.light_layer = LightLayer(self.main_window.width, self.main_window.height)
        
        self.sidebar.setup_sidebar()
    
    def on_draw(self):
        """Render the screen."""
        self.clear()

        self.camera.use()
        self.game_scene.draw()
        if self.main_window.mouse_left_is_pressed:
            pass

        with self.light_layer:
            self.game_scene.draw()
        self.light_layer.draw(ambient_color=self.get_daytime_brightness())
        
        self.sidebar.draw() # side bar outside of light layer

    def get_daytime_brightness(self):
        """Generate the brightness value to render of the screen"""
        time_delta = datetime.timedelta(seconds=time.time() - self.time).total_seconds()
        brightness = interpolate.interp1d(BRIGHTNESS_TIME, BRIGHTNESS_VALUE)(time_delta % DAY_TOTAL_TIME)
        return (brightness * 255,) * 3

    def on_key_press(self, key, _):
        """Called whenever a key is pressed."""
        # using change because if it is changed to player physics engine is required.
        if key in (arcade.key.UP, arcade.key.W):
            self.camera_sprite.change_y = CAMERA_MOVEMENT_SPEED
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.camera_sprite.change_y = -CAMERA_MOVEMENT_SPEED
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.camera_sprite.change_x = -CAMERA_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.camera_sprite.change_x = CAMERA_MOVEMENT_SPEED
        elif key == arcade.key.B: # for now, B button used to toggle build menu on/off
            self.sidebar.switch_build()

    def on_key_release(self, key, _):
        """Called when the user releases a key."""
        if key in (arcade.key.UP, arcade.key.W):
            self.camera_sprite.change_y = 0
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.camera_sprite.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.camera_sprite.change_x = 0
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.camera_sprite.change_x = 0

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int):
        """Called when the mouse is dragged."""
        if INVERT_MOUSE:
            self.camera_sprite.center_x -= dx
            self.camera_sprite.center_y -= dy
        else:
            self.camera_sprite.center_x += dx
            self.camera_sprite.center_y += dy

    def on_mouse_motion(self, x, y, dx, dy):
        self.main_window.mouse_x = x
        self.main_window.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.main_window.mouse_left_is_pressed = True
            actual_x = x + self.screen_center_x
            actual_y = y + self.screen_center_y
            print(self.camera_sprite.center_x, self.camera_sprite.center_y)
            rect = arcade.get_sprites_at_point((actual_x, actual_y), self.game_scene.get_sprite_list("Tiles"))
            if rect:
                rect = rect[0]
                self.selected_tile = arcade.Sprite(str(ASSET_PATH / "sprites_iso" / "select001_iso.png"))
                self.selected_tile.center_x = rect.center_x
                self.selected_tile.center_y = rect.center_y
                self.game_scene.remove_sprite_list_by_name("Selected Tile")
                self.game_scene.add_sprite_list("Selected Tile")
                self.game_scene.add_sprite("Selected Tile", self.selected_tile)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.main_window.mouse_left_is_pressed = False

    def center_camera_to_camera(self):
        """Centers camera to the camera sprite."""
        self.screen_center_x = self.camera_sprite.center_x - \
                          (self.camera.viewport_width / 2)
        self.screen_center_y = self.camera_sprite.center_y - \
                          (self.camera.viewport_height / 2)

        camera_centered = self.screen_center_x, self.screen_center_y
        self.camera.move_to(camera_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""
        self.physics_engine.update()
        # Position the camera
        self.center_camera_to_camera()
        
        self.sidebar.update()
