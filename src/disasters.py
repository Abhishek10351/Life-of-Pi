# disaster.py: manages disasters and other natural hazaards

import random

import arcade
import arcade.gui

from config import ASSET_PATH, PARTY_TIME, SCREEN_HEIGHT, SCREEN_WIDTH
from utils import isometric2rect

DUSTSTORM_TIME_TICS = 10*60
DUST_HAZE = 180
WINDSPEED = 5

ASTEROID_TIME_TICS = 250
ASTEROID_VERT_START = 1000

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
        
        self.particles = None
        
        self.wind_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "wind001.ogg"))
        self.sfx_player = None
        
        self.texture = arcade.load_texture(str(ASSET_PATH / "sprites" / "particle001.png"))
    
    def start(self):
        self.active = True
        self.timeout = DUSTSTORM_TIME_TICS
        self.sfx_player = arcade.play_sound(self.wind_sound, looping=True)
        self.init_particles()
    
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
            return
        
        self.update_particles()
        
        # TODO: check buildings and destroy them
        
        if self.timeout > 0:
            self.timeout -= 1
    
    def draw(self):
        if self.timeout > 0:
            
            cx = self.parent.parent.screen_center_x
            cy = self.parent.parent.screen_center_y
            
            left = cx
            right = cx + self.window_width
            top = cy + self.window_height
            bottom = cy
            
            # Draw haze over map
            if self.timeout < (DUSTSTORM_TIME_TICS / 4):
                haze = DUST_HAZE*4*(self.timeout/DUSTSTORM_TIME_TICS)
            elif self.timeout < (3 * DUSTSTORM_TIME_TICS / 4):
                haze = DUST_HAZE
            else:
                haze = DUST_HAZE*4*((DUSTSTORM_TIME_TICS-self.timeout)/DUSTSTORM_TIME_TICS)
            
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
        
        self.alarm_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "alert.ogg"))
        self.explode_sound = arcade.load_sound(str(ASSET_PATH / "sfx" / "explode_bigger.ogg"))
        self.sfx_player = None
        
        self.texture = arcade.load_texture(str(ASSET_PATH / "sprites" / "particle001.png"))
    
    def start(self):
        self.active = True
        self.timeout = ASTEROID_TIME_TICS
        self.sfx_player = arcade.play_sound(self.alarm_sound, looping=True)
        self.target_x = self.parent.parent.screen_center_x+self.window_width/2
        self.target_y = self.parent.parent.screen_center_y+self.window_height/4
        self.pos_x = self.target_x
        self.pos_y = self.target_y+ASTEROID_VERT_START

    def update(self):
        if not self.active:
            return
        
        if self.timeout == 0:
            self.active = False
            arcade.stop_sound(self.sfx_player)
            self.sfx_player = arcade.play_sound(self.explode_sound)
            return
        
        # TODO: Update meteor path
        self.pos_y -= ASTEROID_VERT_START/ASTEROID_TIME_TICS
        
        if self.timeout > 0:
            self.timeout -= 1
    
    def draw(self):
        if self.timeout > 10:
            # draw asteroid
            arcade.draw_lrwh_rectangle_textured(self.pos_x,self.pos_y,10,10,self.texture)
    
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
            

# Disasters: controls things like the build menu
class Disasters:
    def __init__(self, parent):
        self.parent = parent

        self.window_width = self.parent.main_window.width
        self.window_height = self.parent.main_window.height
        
        self.dust_storm = DustStorm(self)
        self.asteroid_strike = AsteroidStrike(self)
        
        self.tic = 0

    def setup(self):
        self.dust_storm = DustStorm(self)
        self.asteroid_strike = AsteroidStrike(self)
    
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
    
    def draw(self):
        self.dust_storm.draw()
        self.asteroid_strike.draw()
    
    def draw_special(self):
        self.asteroid_strike.draw_flash()
        
        
    
    