# gfx_isometric: testing out isometric rendering
from math import sqrt

import arcade

from config import ASSET_PATH

# Load textures
gfx_textures = {'base': arcade.load_texture(str(ASSET_PATH / "sprites" / "base_80.png")),
                'solar': arcade.load_texture(str(ASSET_PATH / "sprites" / "solargen_80.png")),
                'ice': arcade.load_texture(str(ASSET_PATH / "sprites" / "ice_80.png")),
                'land': arcade.load_texture(str(ASSET_PATH / "tiles" / "land.png"))}

"""
example_structures = [
    ['base',0,0],
    ['base',1,0],
    ['solar',2,0],
    ['ice',3,0],
    ['ice',3,3],
    ['base',2,3]
]
"""

example_structures = [
    ['ice', 0, 0],
    ['ice', 1, 0],
    ['ice', 2, 0],
    ['ice', 0, 1],
    ['base', 1, 1],
    ['ice', 2, 1],
    ['ice', 0, 2],
    ['ice', 1, 2],
    ['ice', 2, 2]
]


# rect2isometric: converts to isometric
def rect2isometric(x, y):
    """Rotates the axis by 45 degrees and then compresses the y axis by a factor of sqrt(2)."""
    iso_x_45 = x * (sqrt(2) / 2) + y * (sqrt(2) / 2)
    iso_y_45 = -x * (sqrt(2) / 2) + y * (sqrt(2) / 2)
    compress_iso_y_45 = -iso_y_45 / sqrt(2)
    return iso_x_45, compress_iso_y_45


def draw_grids(size=80, offset=(0, 0)):
    arcade.start_render()
    for ix in range(-10, 10):
        for iy in range(-10, 10):
            (p1x, p1y) = rect2isometric(size * ix + offset[0], size * iy + offset[1])
            (p2x, p2y) = rect2isometric(size * (ix + 1) + offset[0], size * iy + offset[1])
            (p3x, p3y) = rect2isometric(size * (ix + 1) + offset[0], size * (iy + 1) + offset[1])
            (p4x, p4y) = rect2isometric(size * ix + offset[0], size * (iy + 1) + offset[1])
            arcade.draw_line(p1x, p1y, p2x, p2y, arcade.color.GREEN, 2)
            arcade.draw_line(p2x, p2y, p3x, p3y, arcade.color.GREEN, 2)
            arcade.draw_line(p3x, p3y, p4x, p4y, arcade.color.GREEN, 2)
            arcade.draw_line(p4x, p4y, p1x, p1y, arcade.color.GREEN, 2)


class Structure(arcade.Sprite):
    def __init__(self, parent, tile_type='base', tile_x=0, tile_y=0):
        super().__init__()
        self.parent = parent
        self.texture = gfx_textures[tile_type]
        self.tile_x = tile_x
        self.tile_y = tile_y

        # calculate screen position based on tile x,y

        # rectangular:
        # self.center_x = 80*self.tile_x-40
        # self.center_y = 80*self.tile_y-40

        # isometric:
        (self.center_x, self.center_y) = rect2isometric(80 * self.tile_x + 40, 80 * self.tile_y + 40)


class StructuresSpriteList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        # change it to -40 to 40 for i and -30 to 30 to j.
        for i in range(-10, 10):
            for j in range(-10, 10):
                tile_type = "land"
                if i == 0 and j == 0:
                    tile_type = "base"
                self.append(Structure(self, tile_type=tile_type, tile_x=i, tile_y=j))
