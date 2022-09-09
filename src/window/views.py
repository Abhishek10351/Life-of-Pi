import datetime
import random
import time

import arcade
import arcade.gui
from arcade.experimental.lights import LightLayer
from scipy import interpolate

from config import (ASSET_PATH, BRIGHTNESS_TIME, BRIGHTNESS_VALUE,
                    CAMERA_MOVEMENT_SPEED, CARBON_DIOXIDE_GEYSERS, CRATER,
                    DAY_TOTAL_TIME, DISASTER_PROBA, ICY_TILE, INVERT_MOUSE,
                    IRON_RICH_TILE, LAND, MAP_SIZE_X, MAP_SIZE_Y, PARTY_TIME,
                    RESSOURCE_TO_BUILD, STYLE_GOLDEN_TANOI, VOLCANO)
from disasters import Disasters
from ressource_manager import RessourceManager
from sidebar import SideBar
from utils import Tile, TileList, rect2isometric

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


class Game(arcade.View):
    """
    Main game logic goes here.

    :param main_window: Main window in which it showed.
    """

    def __init__(self, main_window: arcade.Window):
        super().__init__(main_window)
        self.main_window = main_window

        self.game_scene: arcade.Scene = None
        self.tile_sprite_list: TileList = None

        self.camera_sprite = None
        self.physics_engine = None
        self.camera: arcade.Camera = None

        self.light_layer = None
        self.time = time.time()
        self.time_delta = 0

        self.ressource_manager = RessourceManager()

        self.selected_tile = None
        self.screen_center_x = 0
        self.screen_center_y = 0

        self.sidebar = SideBar(self)

        self.disasters = Disasters(self)

        self.manager = None
        self.v_box: arcade.gui.UIBoxLayout = None
        self.console_active = False

        self.debugging_console = None
        self.debugging_console_tex_inp = None
        self.debugging_console_tex_out = None
        self.debugging_console_tex = None

    def on_show_view(self):
        """Called when the current is switched to this view."""
        self.setup()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        self.debugging_console = arcade.gui.UIInputText(text=">", width=self.main_window.width, height=25)
        tex = arcade.texture.Texture("tex creator")
        self.debugging_console_tex_inp = tex.create_filled(color=(100, 0, 0, 150), name="debug console in",
                                                           size=(self.main_window.width, 25))
        self.debugging_console_tex_out = tex.create_filled(color=(0, 100, 0, 150), name="debug console out",
                                                           size=(self.main_window.width, 25))
        self.debugging_console_tex = self.debugging_console.with_background(self.debugging_console_tex_inp)
        self.v_box.add(self.debugging_console_tex)

        self.manager.add(arcade.gui.UIAnchorWidget(child=self.v_box, anchor_y="bottom"))
        self.manager.enable()

        self.game_scene = arcade.Scene()
        self.tile_sprite_list = TileList()

        self.camera = arcade.Camera(self.main_window.width, self.main_window.height)

        for i in range(-MAP_SIZE_X, MAP_SIZE_X, 1):
            for j in range(-MAP_SIZE_Y, MAP_SIZE_Y, 1):
                tile_type = random.choices(["crater", "fe_crater", "geyser",
                                            "ice", "land", "volcano", ],
                                           [CRATER, IRON_RICH_TILE, CARBON_DIOXIDE_GEYSERS, ICY_TILE, LAND, VOLCANO])[0]
                if tile_type == 'crater':
                    filename = tile_type + str(random.randint(1,5)) + "_iso.png"
                else:
                    filename = tile_type + "_iso.png"
                tile = Tile(str(ASSET_PATH / "tiles" / filename), tile_type)
                (tile.isometric_x, tile.isometric_y) = (i, j)
                (tile.center_x, tile.center_y) = rect2isometric(80 * i + 40, 80 * j + 40)
                self.tile_sprite_list.append(tile)
        print(len(self.tile_sprite_list))
        # self.game_scene.add_sprite_list("Tiles", self.tile_sprite_list)
        self.game_scene.add_sprite_list("Selected Tile")

        self.camera_sprite = arcade.Sprite(str(ASSET_PATH / "utils" / "camera.png"))
        # this can be renamed to player sprite, if player sprite is decided to be made.
        self.camera_sprite = arcade.Sprite(str(ASSET_PATH / "utils" / "camera.png"))
        self.camera_sprite.center_x = 400
        self.camera_sprite.center_y = 300
        self.game_scene.add_sprite("Camera", self.camera_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.camera_sprite, gravity_constant=0)

        self.light_layer = LightLayer(self.main_window.width, self.main_window.height)

        self.sidebar.setup_sidebar()
        self.disasters.setup()

    def try_to_build(self, build_type):
        build_type_to_file_name = {"fe_mining": "fe_mining_iso.png",
                                   "co2extract": "co2_generator_iso.png",
                                   "iceextract": "ice_generator_iso.png",
                                   "factory_h2o": "factory_h2o_iso.png",
                                   "base": "base_iso.png",
                                   "garden": "garden_iso.png",
                                   "solar": "solargen_iso.png",
                                   "tank": "tank_iso.png",
                                   "battery": "battery_iso.png",
                                   "geo": "geotherm001_iso.png",
                                   "factory_poly": "factory_poly_iso.png",
                                   "asteroid_defence": "asteroid_defence_iso.png",
                                   "stormshield": "stormshield_iso.png", }
        if self.selected_tile.check_build(build_type, self.tile_sprite_list.get_neighbours(self.selected_tile)) \
                and self.ressource_manager.check_for_resource(RESSOURCE_TO_BUILD[build_type]):
            prev_tile = self.selected_tile
            self.selected_tile = Tile(str(ASSET_PATH / "sprites_iso" / build_type_to_file_name[build_type]),
                                      build_type)
            self.tile_sprite_list.replace(prev_tile, self.selected_tile)
            self.ressource_manager.consume_resource_to_build(RESSOURCE_TO_BUILD[build_type])
            self.ressource_manager.update_building(build_type)
            return True
        return False

    def on_draw(self):
        """Render the screen."""
        self.clear()

        self.camera.use()
        # self.tile_sprite_list.draw()
        # self.game_scene.draw()
        if self.main_window.mouse_left_is_pressed:
            pass

        with self.light_layer:
            self.tile_sprite_list.draw()
            self.game_scene.draw()
            self.disasters.draw()

        self.light_layer.draw(ambient_color=self.get_daytime_brightness())

        self.disasters.draw_special()  # drawing outside ambient light layer

        self.sidebar.draw()  # side bar outside of light layer

        if self.console_active:
            self.manager.draw()

    def get_daytime_brightness(self):
        """Generate the brightness value to render of the screen"""
        self.time_delta = datetime.timedelta(seconds=time.time() - self.time).total_seconds()
        brightness = interpolate.interp1d(BRIGHTNESS_TIME, BRIGHTNESS_VALUE)(self.time_delta % DAY_TOTAL_TIME)
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
        elif key == arcade.key.B:  # for now, B button used to toggle build menu on/off
            self.sidebar.switch_build()
        elif key == arcade.key.R:  # for now, R button used to toggle resources view on/off
            self.sidebar.switch_resview()
        elif key == arcade.key.C:  # for now, C button used to cancel build selection in sidebar
            self.sidebar.CheckforBuild(None)  # Tell sidebar to cancel potential build
        elif key == arcade.key.P:  # used for testing disasters
            self.disasters.new_dust_storm()
        elif key == arcade.key.O:  # used for testing asteroid strike
            self.disasters.new_asteroid_strike()
        elif key == arcade.key.F4:
            self.manager.enable()
            if self.console_active:
                self.manager.disable()
            self.console_active = not self.console_active
        elif key == arcade.key.ENTER:
            if not self.console_active:
                return
            if self.debugging_console.text[1:] in ('clear', 'cls'):
                self.v_box.clear()
                self.debugging_console = arcade.gui.UIInputText(text=">", width=self.main_window.width, height=25)
                self.debugging_console_tex = self.debugging_console.with_background(self.debugging_console_tex_inp)
                self.v_box.add(self.debugging_console_tex)
            else:
                out = arcade.gui.UILabel(text=str(eval(f"{self.debugging_console.text[1:]}")),
                                         width=self.main_window.width, height=25, text_color=(255, 255, 255))
                out_tex = out.with_background(self.debugging_console_tex_out)
                self.v_box.remove(self.debugging_console_tex)
                prev = arcade.gui.UILabel(text=self.debugging_console.text,
                                          width=self.main_window.width, height=25, text_color=(0, 0, 0))
                prev_tex = prev.with_background(self.debugging_console_tex_inp)
                self.v_box.add(prev_tex)
                self.v_box.add(out_tex)
                self.debugging_console = arcade.gui.UIInputText(text=">", width=self.main_window.width, height=25)
                self.debugging_console_tex = self.debugging_console.with_background(self.debugging_console_tex_inp)
                self.v_box.add(self.debugging_console_tex)

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
            rect = arcade.get_sprites_at_point((actual_x, actual_y), self.tile_sprite_list)
            if rect:
                rect = rect[0]
                self.selected_tile = rect
                selected_tile = arcade.Sprite(str(ASSET_PATH / "sprites_iso" / "select001_iso.png"))
                selected_tile.center_x = rect.center_x
                selected_tile.center_y = rect.center_y
                self.game_scene.remove_sprite_list_by_name("Selected Tile")
                self.game_scene.add_sprite_list("Selected Tile")
                self.game_scene.add_sprite("Selected Tile", selected_tile)

            self.sidebar.DisplayTile([actual_x, actual_y])
            self.sidebar.CheckforBuild([actual_x, actual_y])  # also check if trying to build

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

    def check_win_loose(self):
        if self.ressource_manager.current_ressource['O2'] < 0 or self.ressource_manager.current_ressource['Food'] < 0:
            print(self.ressource_manager.current_ressource)
            winloose = WinLooseMenu(self.main_window, 'Game Over !')
            self.main_window.show_view(winloose)
        if self.time_delta > PARTY_TIME:
            winloose = WinLooseMenu(self.main_window, 'You Win !')
            self.main_window.show_view(winloose)

    def generate_disaster(self):
        """Randomly generate disasters"""
        if self.time_delta > 60:
            rand = random.randint(0, 1 / DISASTER_PROBA)
            if rand == 0:
                self.disasters.new_dust_storm()
            elif rand == 1:
                self.disasters.new_asteroid_strike()

    def on_update(self, delta_time):
        """Movement and game logic"""
        self.physics_engine.update()
        # Position the camera
        self.center_camera_to_camera()

        self.disasters.update()
        self.sidebar.update()

        self.ressource_manager.update()
        self.generate_disaster()

        self.check_win_loose()


class WinLooseMenu(arcade.View):
    """
    Menu view.

    :param main_window: Main window in which the view is shown.
    """

    def __init__(self, main_window: arcade.Window, win_loose=''):
        super().__init__(main_window)
        self.main_window = main_window

        self.v_box = None

        self.manager = None

        self.win_loose_message = win_loose

    def on_show_view(self) -> None:
        """Called when the current is switched to this view."""
        self.setup()

    def setup(self) -> None:
        """Set up the game variables. Call to re-start the game."""
        self.v_box = arcade.gui.UIBoxLayout(space_between=30)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        win_loose_button = arcade.gui.UIFlatButton(
            text=self.win_loose_message, width=200, style=STYLE_GOLDEN_TANOI)

        restart_button = arcade.gui.UIFlatButton(
            text="Restart", width=200, style=STYLE_GOLDEN_TANOI)
        restart_button.on_click = self._on_click_restart_button

        exit_button = arcade.gui.UIFlatButton(
            text="Exit", width=200, style=STYLE_GOLDEN_TANOI)
        exit_button.on_click = self._on_click_exit_button

        self.v_box.add(win_loose_button)
        self.v_box.add(restart_button)
        self.v_box.add(exit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                child=self.v_box
            )
        )

    def on_draw(self) -> None:
        """Called when this view should draw."""
        self.clear()

        self.manager.draw()

    def _on_click_restart_button(self, _: arcade.gui.UIOnClickEvent) -> None:
        game = Game(self.main_window)
        self.main_window.show_view(game)

    def _on_click_exit_button(self, _: arcade.gui.UIOnClickEvent) -> None:
        self.main_window.close()
        arcade.exit()

    def on_hide_view(self):
        self.manager.disable()
