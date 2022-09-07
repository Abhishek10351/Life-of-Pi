# build_sidebar.py: controls and display for sidebar for building etc.

from math import *

import arcade

from config import (ASSET_PATH, BRIGHTNESS_TIME, BRIGHTNESS_VALUE,
                    CAMERA_MOVEMENT_SPEED, DAY_TOTAL_TIME, INVERT_MOUSE,
                    STYLE_GOLDEN_TANOI, VIEWPORT_ANGLE)

DESCR_TEXT_HEIGHT = 240

# SideBar: controls things like the build menu
class SideBar(object):
    def __init__(self, parent):
        self.parent = parent
        
        self.build = 0
        self.last_select = None
        self.current_select = None
    
    def setup_sidebar(self):
        self.sb_manager = arcade.gui.UIManager()
        self.sb_manager.enable()
        
        # Descriptions
        self.build_descriptions = {}
        
        self.build_descriptions['base'] = "Habitation Pod: houses \ncrew members"
        self.build_descriptions['garden'] = "Garden Pod: provide food for crew"
        self.build_descriptions['solar'] = "Solar Generator: \ngenerates energy"
        self.build_descriptions['geo'] = "Geo-Thermal Generator: \ngenerates energy"
        self.build_descriptions['battery'] = "Battery: needed to store energy"
        self.build_descriptions['iceextract'] = "H2O Ice Extractor: collects H2O \nfrom ice sources"
        self.build_descriptions['co2extract'] = "CO2 Extractor: collects CO2 \nfrom geysers"
        self.build_descriptions['fe_mining'] = "Fe/Iron Mining Operation: \ncollects Fe from crater deposits"
        self.build_descriptions['factory_co2'] = "CO Factory: generate C and O \nfrom CO2"
        self.build_descriptions['factory_h2o'] = "HO Factory: generate H and O \nfrom H2O"
        self.build_descriptions['factory_poly'] = "Polymer Factory: generates \npolymers from C and H"
        self.build_descriptions['tank'] = "Tank: used to store chemicals."
        
        # Button data
        buttons = [
            ['base',20,20,'box001.png','box002.png'],
            ['garden',80,20,'box001.png','box002.png'],
            ['solar',20,80,'box001.png','box002.png'],
            ['geo',80,80,'box001.png','box002.png'],
            ['battery',140,80,'box001.png','box002.png'],
            ['iceextract',20,140,'box001.png','box002.png'],
            ['co2extract',80,140,'box001.png','box002.png'],
            ['fe_mining',140,140,'box001.png','box002.png'],
            ['factory_co2',20,200,'box001.png','box002.png'],
            ['factory_h2o',80,200,'box001.png','box002.png'],
            ['factory_poly',140,200,'box001.png','box002.png'],
            ['tank',20,260,'box001.png','box002.png'],
        ]
        
        # Create the buttons
        self.buildbuttons = {}
        for (i,b) in enumerate(buttons):
            texture = arcade.load_texture(str(ASSET_PATH / "sprites" / b[3]))
            texture_hover = arcade.load_texture(str(ASSET_PATH / "sprites" / b[4]))
            button = arcade.gui.UITextureButton(texture=texture, texture_hovered=texture_hover)
            button.on_click = self._on_click_build_button
            self.buildbuttons[b[0]] = button
            anchor = arcade.gui.UIAnchorWidget(
                    anchor_x="left",
                    anchor_y="top",
                    align_x=b[1],
                    align_y=-b[2]-30,
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
        
        self.build_label1 = arcade.gui.UILabel(0,0,font_size=14,
            text_color=(0,100,0),text="Press B for Build Options")
        anchor = arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                align_x=15,
                align_y=-15,
                child=self.build_label1)
        self.build_label1.anchor = anchor
        self.sb_manager.add(anchor)
        
        self.build_label2 = arcade.gui.UILabel(0,0,font_size=14,
            text_color=(0,200,0),text="Build Options (B to close)")
        anchor = arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                align_x=15,
                align_y=-15,
                child=self.build_label2)
        self.build_label2.anchor = anchor
                
        self.build = 0
        self.last_select = None
        
        """
        Buildlist:
        
        base, garden pod
        solar gen, geo thermal, storage battery
        ice extractor, Co2 extractor, fe mining
        factory: co2, h20, poly
        storage tanks: many
        """
    
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
        type = None
        for key in self.buildbuttons:
            if self.buildbuttons[key].hovered:
                type = key
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
                #self.sb_manager.remove(self.buildbuttons[key].anchor_label)
            self.last_select = None
            self.current_select = None
    
    def update(self):
        self.check_button_hover()
    
    def draw_build_text(self):
        if not self.current_select == None:
            text_lines = self.build_descriptions[self.current_select].split('\n')
            for (i,line) in enumerate(text_lines):
                h = DESCR_TEXT_HEIGHT-18*i
                arcade.draw_text(line, 15, h, arcade.color.GREEN, font_size=12, 
                    anchor_x="left", anchor_y="center")
                #font_name=resources.font_path['text']
    
    def draw(self):
        self.sb_manager.draw() 
        self.draw_build_text()
    
