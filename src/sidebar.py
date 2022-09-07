# build_sidebar.py: controls and display for sidebar for building etc.

from math import sqrt

import arcade
import arcade.gui

from config import ASSET_PATH, PARTY_TIME, SCREEN_HEIGHT, SCREEN_WIDTH

DESCR_TEXT_HEIGHT = 240
RES_TEXT_HEIGHT = 180
BUILDTEXTHEIGHT = 15


def rect2isometric(x, y):
    """Rotates the axis by 45 degrees and then compresses the y axis by a factor of sqrt(2)."""
    iso_x_45 = x * (sqrt(2) / 2) + y * (sqrt(2) / 2)
    iso_y_45 = -x * (sqrt(2) / 2) + y * (sqrt(2) / 2)
    compress_iso_y_45 = -iso_y_45 / sqrt(2)
    return iso_x_45, compress_iso_y_45


def isometric2rect(iso_x_45, compress_iso_y_45):
    """Un-compresses the y axis by a factor of sqrt(2) and then rotates the axis by 45 degrees"""
    iso_y_45 = -compress_iso_y_45 * sqrt(2)
    x = iso_x_45 * (sqrt(2) / 2) - iso_y_45 * (sqrt(2) / 2)
    y = iso_x_45 * (sqrt(2) / 2) + iso_y_45 * (sqrt(2) / 2)
    return x, y


# SideBar: controls things like the build menu
class SideBar:
    def __init__(self, parent):
        self.res_view = None
        self.res_label2 = None
        self.res_label1 = None
        self.msg_to = None

        self.build_result = None
        self.build_label1 = None
        self.build_label2 = None

        self.buildbuttons = None
        self.buildicons_textures = None
        self.parent = parent

        self.window_width = self.parent.main_window.width
        self.window_height = self.parent.main_window.height

        self.build = 0
        self.last_select = None
        self.current_select = None
        self.trybuild = None

        self.tic = 0

        self.sb_manager: arcade.gui.UIManager = None

        self.build_descriptions = None

    def setup_sidebar(self):
        self.sb_manager = arcade.gui.UIManager()
        self.sb_manager.enable()

        # Descriptions
        self.build_descriptions = {'base': "Habitation Pod: houses \ncrew members",
                                   'garden': "Garden Pod: provide food for crew",
                                   'solar': "Solar Generator: \ngenerates energy",
                                   'geo': "Geo-Thermal Generator: \ngenerates energy",
                                   'battery': "Battery: needed to store energy",
                                   'iceextract': "H2O Ice Extractor: collects H2O \nfrom ice sources",
                                   'co2extract': "CO2 Extractor: collects CO2 \nfrom geysers",
                                   'fe_mining': "Fe/Iron Mining Operation: \ncollects Fe from crater deposits",
                                   'factory_co2': "CO Factory: generate C and O \nfrom CO2",
                                   'factory_h2o': "HO Factory: generate H and O \nfrom H2O",
                                   'factory_poly': "Polymer Factory: generates \npolymers from C and H",
                                   'tank': "Tank: used to store chemicals."}

        # Button data
        buttons = [
            ['base', 20, 20, 'base_off.png', 'base_on.png'],
            ['garden', 80, 20, 'garden_off.png', 'garden_on.png'],
            ['solar', 20, 80, 'solar_off.png', 'solar_on.png'],
            ['geo', 80, 80, 'geo_off.png', 'geo_on.png'],
            ['battery', 140, 80, 'battery_off.png', 'battery_on.png'],
            ['iceextract', 20, 140, 'extractor_off.png', 'extractor_on.png'],
            ['co2extract', 80, 140, 'extractor_off.png', 'extractor_on.png'],
            ['fe_mining', 140, 140, 'mining_off.png', 'mining_on.png'],
            ['factory_co2', 20, 200, 'factory_co2_off.png', 'factory_co2_on.png'],
            ['factory_h2o', 80, 200, 'factory_h2o_off.png', 'factory_h2o_on.png'],
            ['factory_poly', 140, 200, 'factory_poly_off.png', 'factory_poly_on.png'],
            ['tank', 20, 260, 'tank_off.png', 'tank_on.png'],
        ]

        # Create the buttons
        self.buildbuttons = {}
        for (i, b) in enumerate(buttons):
            texture = arcade.load_texture(str(ASSET_PATH / "sidebar" / b[3]))
            texture_hover = arcade.load_texture(str(ASSET_PATH / "sidebar" / b[4]))
            button = arcade.gui.UITextureButton(texture=texture, texture_hovered=texture_hover)
            button.on_click = self._on_click_build_button
            self.buildbuttons[b[0]] = button
            anchor = arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                align_x=b[1],
                align_y=-b[2] - 30,
                child=button)
            self.buildbuttons[b[0]].anchor = anchor
            """
            label = arcade.gui.UILabel(0,0,font_size=14,text_color=(0,200,0),
                text=self.build_descriptions[b[0]])
            anchor_label = arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                align_x=15,
                align_y=-350,
                child=label)
            self.buildbuttons[b[0]].anchor_label = anchor_label
            self.sb_manager.add(anchor)
            """

        self.build_label1 = arcade.gui.UILabel(0, 0, font_size=14,
                                               text_color=(0, 100, 0), text="Press B for Build Options")
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="top",
            align_x=15,
            align_y=-15,
            child=self.build_label1)
        self.build_label1.anchor = anchor
        self.sb_manager.add(anchor)

        self.build_label2 = arcade.gui.UILabel(0, 0, font_size=14,
                                               text_color=(0, 200, 0), text="Build Options (B to close)")
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="top",
            align_x=15,
            align_y=-15,
            child=self.build_label2)
        self.build_label2.anchor = anchor

        self.build = 0
        self.last_select = None

        self.trybuild = None
        self.build_result = False
        self.msg_to = 0

        self.buildicons_textures = {'base': arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "base_iso.png")),
                                    'garden': arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "foodpod_iso.png")),
                                    'solar': arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "solargen_iso.png")),
                                    'geo': arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "geotherm001_iso.png")),
                                    'battery': arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "battery_iso.png")),
                                    'iceextract': arcade.load_texture(
                                        str(ASSET_PATH / "sprites_iso" / "generator_iso.png")),
                                    'co2extract': arcade.load_texture(
                                        str(ASSET_PATH / "sprites_iso" / "generator_iso.png")),
                                    'fe_mining': arcade.load_texture(
                                        str(ASSET_PATH / "sprites_iso" / "mininggear_iso.png")),
                                    'factory_co2': arcade.load_texture(
                                        str(ASSET_PATH / "sprites_iso" / "factory_co2_iso.png")),
                                    'factory_h2o': arcade.load_texture(
                                        str(ASSET_PATH / "sprites_iso" / "factory_h2o_iso.png")),
                                    'factory_poly': arcade.load_texture(
                                        str(ASSET_PATH / "sprites_iso" / "factory_poly_iso.png")),
                                    'tank': arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "tank_iso.png"))}

        """
        Buildlist:

        base, garden pod
        solar gen, geo thermal, storage battery
        ice extractor, Co2 extractor, fe mining
        factory: co2, h20, poly
        storage tanks: many
        """

        self.res_label1 = arcade.gui.UILabel(0, 0, font_size=14,
                                             text_color=(0, 100, 0), text="Press R to see resources")
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="bottom",
            align_x=15,
            align_y=15,
            child=self.res_label1)
        self.res_label1.anchor = anchor
        self.sb_manager.add(anchor)

        self.res_label2 = arcade.gui.UILabel(0, 0, font_size=14,
                                             text_color=(0, 200, 0), text="Resources (R to close)")
        anchor = arcade.gui.UIAnchorWidget(
            anchor_x="left",
            anchor_y="bottom",
            align_x=15,
            align_y=15,
            child=self.res_label2)
        self.res_label2.anchor = anchor

        self.res_view = 0

    def check_button_hover(self):
        if self.build == 0:
            self.current_select = None
            return
        found = None
        for key in self.buildbuttons:
            if self.buildbuttons[key].hovered:
                found = key
                break

        self.current_select = found

        """
        if not found == self.last_select and self.build == 1:
            if not self.last_select == None:
                self.sb_manager.remove(self.buildbuttons[self.last_select].anchor_label)
            if not found == None:
                self.sb_manager.add(self.buildbuttons[found].anchor_label)
            self.last_select = found
        """

    def _on_click_build_button(self, _: arcade.gui.UIOnClickEvent) -> None:
        for key in self.buildbuttons:
            if self.buildbuttons[key].hovered:
                self.trybuild = key
                break

    def switch_build(self):
        if self.build == 0:
            self.build = 1
            self.sb_manager.remove(self.build_label1.anchor)
            self.sb_manager.add(self.build_label2.anchor)
            for key in self.buildbuttons:
                self.sb_manager.add(self.buildbuttons[key].anchor)
        else:
            self.build = 0
            self.sb_manager.remove(self.build_label2.anchor)
            self.sb_manager.add(self.build_label1.anchor)
            for key in self.buildbuttons:
                self.sb_manager.remove(self.buildbuttons[key].anchor)
                self.buildbuttons[key].hovered = False
                # self.sb_manager.remove(self.buildbuttons[key].anchor_label)
            self.last_select = None
            self.current_select = None

    def switch_resview(self):
        if self.res_view == 0:
            self.res_view = 1
            self.sb_manager.remove(self.res_label1.anchor)
            self.sb_manager.add(self.res_label2.anchor)
            # bring up res window
        else:
            self.res_view = 0
            self.sb_manager.remove(self.res_label2.anchor)
            self.sb_manager.add(self.res_label1.anchor)
            # pull down res window

    def update(self):
        self.tic += 1
        if self.msg_to > 0:
            self.msg_to -= 1
        self.check_button_hover()

        """
        # hack to play with resources (for testing)
        if self.tic % 10 == 0:
            key = ['Ener','Fe','H2O','CO2','C','H','O2','Poly'][random.randint(0,7)]
            self.parent.ressource_manager.current_ressource[key] += 100
        """

    # Gets called by mouse click from parent View
    def CheckforBuild(self, coords):
        if coords is None or self.trybuild is None:
            self.trybuild = None
            self.msg_to = 0
            return

        # get tile coords
        (x, y) = isometric2rect(coords[0], coords[1])
        tile_x = int(x / 80)
        tile_y = int(y / 80)
        print('building at:', tile_x, tile_y, self.trybuild)
        result = self.parent.try_to_build(self.trybuild, tile_x, tile_y)
        if result:
            self.build_result = True
            self.trybuild = None
            self.msg_to = 90
        else:
            self.build_result = False
            self.trybuild = None
            self.msg_to = 120

    def draw_build_text(self):
        if self.current_select is not None:
            text_lines = self.build_descriptions[self.current_select].split('\n')
            for (i, line) in enumerate(text_lines):
                h = DESCR_TEXT_HEIGHT - 18 * i
                arcade.draw_text(line, 15, h, arcade.color.GREEN, font_size=12,
                                 anchor_x="left", anchor_y="center")
                # font_name=resources.font_path['text']

    def draw_build_structure(self):
        if self.trybuild is not None:
            x = self.parent.main_window.mouse_x
            y = self.parent.main_window.mouse_y
            arcade.draw_lrwh_rectangle_textured(x - 116 / 2, y - 82 / 2, 116, 82,
                                                self.buildicons_textures[self.trybuild], alpha=100)

    def draw_build_message(self):
        if self.trybuild is not None:
            arcade.draw_text('click to location to build (C to cancel)', self.window_width / 2,
                             self.window_height - BUILDTEXTHEIGHT, arcade.color.GREEN, font_size=12,
                             anchor_x="center", anchor_y="center")
        elif self.msg_to > 0:
            if self.build_result:
                arcade.draw_text('structure built!', self.window_width / 2,
                                 self.window_height - BUILDTEXTHEIGHT, arcade.color.GREEN, font_size=12,
                                 anchor_x="center", anchor_y="center")
            else:
                arcade.draw_text("can't build structure here!", self.window_width / 2,
                                 self.window_height - BUILDTEXTHEIGHT, arcade.color.RED, font_size=12,
                                 anchor_x="center", anchor_y="center")

    def draw_res_disp(self):
        if self.res_view == 0:
            return
        text_lines = [
            'Energy:',
            'Iron (Fe):',
            'H2O:',
            'CO2:',
            'C:',
            'H:',
            'O2:',
            'Polymers:'
        ]
        for (i, line) in enumerate(text_lines):
            h = RES_TEXT_HEIGHT - 18 * i
            arcade.draw_text(line, 90, h, arcade.color.GREEN, font_size=12,
                             anchor_x="right", anchor_y="center")
        keys = ['Ener', 'Fe', 'H2O', 'CO2', 'C', 'H', 'O2', 'Poly']

        for (i, key) in enumerate(keys):
            h = RES_TEXT_HEIGHT - 18 * i
            have = self.parent.ressource_manager.current_ressource[key]
            max_cap = self.parent.ressource_manager.maximum_ressource[key]
            line = '(%d / %d)' % (have, max_cap)
            if max_cap == 0:
                text_col = arcade.color.GRAY
            elif (have / max_cap) < 0.33:
                text_col = arcade.color.GREEN
            elif (have / max_cap) < 0.66:
                text_col = arcade.color.YELLOW
            else:
                text_col = arcade.color.RED
            if have >= max_cap:
                line += ' Full! Build more '
                if key in ['Fe', 'H2O', 'CO2', 'C', 'H', 'O2', 'Poly']:
                    line += 'storage tanks'
                elif key in ['Ener']:
                    line += 'batteries'
            arcade.draw_text(line, 100, h, text_col, font_size=12,
                             anchor_x="left", anchor_y="center")

    def draw_time_left(self):
        arcade.draw_text('Time before rescue : %i s' % round(PARTY_TIME - self.parent.time_delta),
                         (SCREEN_WIDTH / 2) - 105, SCREEN_HEIGHT - 20, arcade.color.GREEN, font_size=12)
    
    # used to display some information about the current tile selected by
    # player from Main View
    def DisplayTile(self, coords):
        # get tile coords
        (x, y) = isometric2rect(coords[0], coords[1])
        tile_x = int(x / 80)  # noqa: F841
        tile_y = int(y / 80)  # noqa: F841
        # TODO: interpret whats here (tilemap?), display message

    def draw(self):
        self.sb_manager.draw()
        self.draw_build_text()
        self.draw_res_disp()
        self.draw_time_left()
        self.draw_build_message()
        self.draw_build_structure()
