# disaster.py: manages disasters and other natural hazaards

import random
import math

import arcade
import arcade.gui

from config import ASSET_PATH, PARTY_TIME, SCREEN_HEIGHT, SCREEN_WIDTH
from utils import Tile, TileList, rect2isometric, isometric2rect

DUSTSTORM_TIME_TICS = 10*60
DUST_HAZE = 180
WINDSPEED = 5

ASTEROID_TIME_TICS = 250
ASTEROID_VERT_START = 1000
ASTEROID_BLAST_RADIUS = 200

BUILD_LIST = ['base','garden','solar','geo','battery','iceextract','co2extract',
            'fe_mining','factory_co2','factory_h2o', 'factory_poly','tank',
            'asteroid_defence','stormshield']

SHIELD_RADIUS = 200
LASER_RADIUS = 300

class Particle(object):
    
    def __init__(self, x, y, texture):
        self.texture = texture
        self.center_x = x
        self.center_y = y
    
    def update(self, left, right, top, bottom):
        self.center_x += WINDSPEED
        self.center_y += WINDSPEED
        if self.center_x > right:
            self.center_x = left
            self.center_y = bottom + random.random()*(top-bottom)
        elif self.center_y > top:
            self.center_x = left + random.random()*(right-left)
            self.center_y = bottom
    
    def draw(self,left,right,top,bottom,alpha):
        x = self.center_x
        y = self.center_y
        #arcade.draw_lrtb_rectangle_filled(x,x+5,y+5,y,(230, 200, 200, alpha))
        arcade.draw_lrwh_rectangle_textured(x,y,10,10,self.texture,alpha=alpha)

# DustStorm
class DustStorm():
    def __init__(self, parent):
        self.parent = parent

        self.window_width = self.parent.window_width
        self.window_height = self.parent.window_width
        
        self.active = False
        self.timeout = 0
        self.shields_list = []
        self.unprotected_list = []
        self.targets = []
        
        self.particles = None
        
        self.wind_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "wind001.ogg"))
        self.explode_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "explode_bigger.ogg"))
        self.sfx_player = None
        
        self.texture = arcade.load_texture(str(ASSET_PATH / "sprites" / "particle001.png"))
        self.texture_shield = arcade.load_texture(str(ASSET_PATH / "sprites" / "shield.png"))
        self.texture_icon2 = arcade.load_texture(str(ASSET_PATH / "sprites" / "box002.png"))
    
    def start(self):
        self.active = True
        self.timeout = DUSTSTORM_TIME_TICS
        self.sfx_player = arcade.play_sound(self.wind_sound, looping=True)
        self.init_particles()
        
        # Find target buildings that could destroyed (not protected by shields)
        self.get_unprotected_buildings()
        
        # choose one at random to destroy (for now)
        if len(self.unprotected_list) > 0:
            ind = random.randint(0,len(self.unprotected_list)-1)
            self.targets = [self.unprotected_list[ind]]
        else:
            self.targets = []
    
    def get_unprotected_buildings(self):
        self.shields_list = []
        for tile in self.parent.parent.tile_sprite_list:
            if tile.tile_type in ['stormshield']: # TODO: replace with storm shield generator
                self.shields_list.append(tile)
        
        self.unprotected_list = []
        for tile in self.parent.parent.tile_sprite_list:
            if tile.tile_type in BUILD_LIST:
                protected = False
                for shield in self.shields_list:
                    dist = math.sqrt( (shield.center_x - tile.center_x) ** 2 + (shield.center_y - tile.center_y) ** 2 )
                    if dist <= SHIELD_RADIUS:
                        protected = True
                        break
                if not protected:
                    self.unprotected_list.append(tile)
    
    def init_particles(self):
        cx = self.parent.parent.screen_center_x
        cy = self.parent.parent.screen_center_y
        self.particles = []
        for i in range(20):
            x = cx + random.random()*self.window_width
            y = cy + random.random()*self.window_height
            self.particles.append(Particle(x, y, self.texture))
    
    def update_particles(self):
        cx = self.parent.parent.screen_center_x
        cy = self.parent.parent.screen_center_y
        left = cx
        right = cx + self.window_width
        top = cy + self.window_height
        bottom = cy
        for p in self.particles:
            p.update(left, right, top, bottom)
    
    def update(self):
        if not self.active:
            return
        
        if self.timeout == 0:
            self.active = False
            arcade.stop_sound(self.sfx_player)
            self.particles = None
            self.shields_list = []
            self.unprotected_list = []
            self.targets = []
            return
        
        self.update_particles()
        
        # Destroy target building (mid-dust storm)
        if self.timeout == int(DUSTSTORM_TIME_TICS/2):
            if len(self.targets) > 0:
                arcade.play_sound(self.explode_sound)
                self.parent.destroy_buildings(self.targets)
        
        if self.timeout > 0:
            self.timeout -= 1
    
    def draw_shields(self):
        if self.timeout > 0:
            haze = self.get_haze()/8+25*math.fabs(math.sin(0.05*self.timeout))
            for shield in self.shields_list:
                arcade.draw_lrwh_rectangle_textured(shield.center_x-450/2,shield.center_y-450/2,
                    450,450,self.texture_shield,alpha=haze)
    
    def check_warnings(self):
        if self.timeout > (DUSTSTORM_TIME_TICS/2):
            self.parent.set_warnings(self.unprotected_list)
    
    def get_haze(self):
        if self.timeout < (DUSTSTORM_TIME_TICS / 4):
            haze = DUST_HAZE*4*(self.timeout/DUSTSTORM_TIME_TICS)
        elif self.timeout < (3 * DUSTSTORM_TIME_TICS / 4):
            haze = DUST_HAZE
        else:
            haze = DUST_HAZE*4*((DUSTSTORM_TIME_TICS-self.timeout)/DUSTSTORM_TIME_TICS)
        
        return haze
    
    def draw(self):
        if self.timeout > 0:
            
            cx = self.parent.parent.screen_center_x
            cy = self.parent.parent.screen_center_y
            
            left = cx
            right = cx + self.window_width
            top = cy + self.window_height
            bottom = cy
            
            # Draw haze over map
            haze = self.get_haze()
            arcade.draw_lrtb_rectangle_filled(left,right,top,bottom,
                (204, 160, 127, haze))
            
            # draw flying particles
            for p in self.particles:
                p.draw(left,right,top,bottom,haze)
                

# AsteroidStrike
class AsteroidStrike():
    def __init__(self, parent):
        self.parent = parent

        self.window_width = self.parent.window_width
        self.window_height = self.parent.window_width
        
        self.active = False
        self.timeout = 0
        self.lasers_in_range = []
        self.unprotected_list = []
        
        self.alarm_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "alert.ogg"))
        self.explode_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "explode_bigger.ogg"))
        self.laser_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "laser.ogg"))
        self.sfx_player = None
        
        self.texture = arcade.load_texture(str(ASSET_PATH / "sprites" / "asteroid001.png"))
    
    def check_for_defence(self):
        lasers_in_range = []
        for tile in self.parent.parent.tile_sprite_list:
            if tile.tile_type in ['asteroid_defence']:
                dist = math.sqrt( (self.target_x - tile.center_x) ** 2 + (self.target_y - tile.center_y) ** 2 )
                if dist <= LASER_RADIUS:
                    lasers_in_range.append(tile)
        return lasers_in_range
    
    def start(self):
        self.active = True
        self.timeout = ASTEROID_TIME_TICS
        self.sfx_player = arcade.play_sound(self.alarm_sound, looping=True)
        self.target_x = self.parent.parent.screen_center_x+self.window_width/2
        self.target_y = self.parent.parent.screen_center_y+self.window_height/4
        self.pos_x = self.target_x
        self.pos_y = self.target_y+ASTEROID_VERT_START
        self.lasers_in_range = self.check_for_defence()
        if len(self.lasers_in_range) == 0:
            self.unprotected_list = self.parent.find_buildings_in_range(self.target_x,
                self.target_y,r=ASTEROID_BLAST_RADIUS)

    def update(self):
        if not self.active:
            return
        
        if self.timeout == 0:
            arcade.stop_sound(self.sfx_player)
            if len(self.lasers_in_range) == 0:
                arcade.play_sound(self.explode_sound)
                targets = self.parent.find_buildings_in_range(self.pos_x,self.pos_y,r=ASTEROID_BLAST_RADIUS)
                if len(targets) > 0:
                    self.parent.destroy_buildings(targets)
            self.active = False
            self.lasers_in_range = []
            return
        
        # TODO: Update meteor path
        self.pos_y -= ASTEROID_VERT_START/ASTEROID_TIME_TICS
        if len(self.lasers_in_range) > 0 and self.timeout == int(3 * ASTEROID_TIME_TICS/4):
            arcade.play_sound(self.laser_sound)
        if len(self.lasers_in_range) > 0 and self.timeout == int(ASTEROID_TIME_TICS/4):
            self.timeout = 0
        
        if self.timeout > 0:
            self.timeout -= 1
    
    def check_warnings(self):
        if self.timeout > 0:
            self.parent.set_warnings(self.unprotected_list)
    
    def draw(self):
        if self.timeout > 10:
            # draw asteroid
            arcade.draw_lrwh_rectangle_textured(self.pos_x,self.pos_y,50,50,self.texture)
    
    def draw_laser(self):
        if self.timeout > 0 and self.timeout < 3 * ASTEROID_TIME_TICS / 4:
            for laser in self.lasers_in_range:
                arcade.draw_line(laser.center_x, laser.center_y, self.pos_x+25, 
                    self.pos_y+25, (0,128,255,200), 2)
    
    def draw_flash(self):
        if self.timeout > 0:
            cx = self.parent.parent.screen_center_x
            cy = self.parent.parent.screen_center_y
            left = cx
            right = cx + self.window_width
            top = cy + self.window_height
            bottom = cy
            
            # Draw flash over map
            if self.timeout < 10:
                haze = 255*self.timeout/10
                arcade.draw_lrtb_rectangle_filled(left,right,top,bottom,
                    (255, 255, 255, haze))
            elif self.timeout < 20:
                haze = 255*(20-self.timeout)/10
                arcade.draw_lrtb_rectangle_filled(left,right,top,bottom,
                    (255, 255, 255, haze))
            
class DestroyedLocs():
    def __init__(self):
        self.data = []
        self.texture = arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "destroyed_iso.png"))
    
    def add(self,x,y):
        self.data.append([x,y,255])
    
    def update(self):
        for d in self.data:
            if d[2] > 0:
                d[2] -= 1
        keep = []
        for d in self.data:
            if d[2] > 0:
                keep.append(d)
        self.data = keep
    
    def draw(self):
        for d in self.data:
            arcade.draw_lrwh_rectangle_textured(d[0]-116/2,d[1]-82/2,116,82,self.texture,alpha=d[2])
                

# Disasters: controls things like the build menu
class Disasters:
    def __init__(self, parent):
        self.parent = parent

        self.window_width = self.parent.main_window.width
        self.window_height = self.parent.main_window.height
        
        self.texture_warn = arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "warning_iso.png"))
        
        self.setup()
        
    def setup(self):
        self.dust_storm = DustStorm(self)
        self.asteroid_strike = AsteroidStrike(self)
        self.warnings = []
        self.destroyed_locs = DestroyedLocs()
        self.tic = 0
    
    def find_buildings_in_range(self,x,y,r=None):
        
        in_range_list = []
        for tile in self.parent.tile_sprite_list:
            if tile.tile_type in BUILD_LIST:
                dist = math.sqrt( (x - tile.center_x) ** 2 + (y - tile.center_y) ** 2 )
                if r == None or dist <= r:
                    in_range_list.append(tile)
        
        return in_range_list
    
    def destroy_buildings(self, targets):
        
        for target in targets:
            
            # remove target from tiles, replace with empty ground
            if target.tile_type == 'iceextract':
                new_tile = Tile(str(ASSET_PATH / "tiles" / 'ice_iso.png'),"ice")
            elif target.tile_type == 'co2extract':
                new_tile = Tile(str(ASSET_PATH / "tiles" / 'geyser_iso.png'),"geyser")
            elif target.tile_type == 'fe_mining':
                new_tile = Tile(str(ASSET_PATH / "tiles" / 'fe_crater_iso.png'),"fe_crater")
            else:
                new_tile = Tile(str(ASSET_PATH / "tiles" / 'land_iso.png'),"land")
            
            # replace tiles
            self.parent.tile_sprite_list.replace(target, new_tile)
            
            # Do something to update selected tile in Game ???
            # self.selected_tile ...
            
            # Do stuff to update resource manager ???
            # self.ressource_manager.something ... ???
            self.parent.ressource_manager.destroy_building(targets)
            
            # track for GUI display
            self.destroyed_locs.add(target.center_x,target.center_y)
    
    def new_dust_storm(self):
        if not self.dust_storm.active:
            self.dust_storm.start()
    
    def new_asteroid_strike(self):
        if not self.asteroid_strike.active:
            self.asteroid_strike.start()
    
    def update(self):
        self.tic += 1
        self.dust_storm.update()
        self.asteroid_strike.update()
        self.destroyed_locs.update()
    
    def set_warnings(self, warnings):
        self.warnings = warnings
    
    def draw_warnings(self):
        for building in self.warnings:
            arcade.draw_lrwh_rectangle_textured(building.center_x-116/2,building.center_y-82/2,
                116,82,self.texture_warn,alpha=255*math.fabs(math.sin(0.05*self.tic)))
    
    def draw(self):
        self.dust_storm.draw()
        self.asteroid_strike.draw()
    
    # drawing things outside of the ambient light
    def draw_special(self):
        self.dust_storm.draw_shields()
        self.asteroid_strike.draw_flash()
        self.asteroid_strike.draw_laser()
        
        self.dust_storm.check_warnings()
        self.draw_warnings()
        self.warnings = []
        self.asteroid_strike.check_warnings()
        self.draw_warnings()
        self.warnings = []
        
        self.destroyed_locs.draw()
        
        
    
    