from math import sqrt
# using typing because we need it to be compatible with 3.8 and 3.9 too.
from typing import List

import arcade

from config import TILE_TYPE_BUILD, ASSET_PATH


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


class Tile(arcade.Sprite):
    """Helper class for handling tiles."""
    def __init__(self, path: str, tile_type: str):
        super(Tile, self).__init__(filename=path)

        self.tile_type = tile_type
        self.isometric_x = 0
        self.isometric_y = 0
        
        if self.tile_type == 'geo':
            self.frame_textures = [
                arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "geotherm001_iso.png")),
                arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "geotherm002_iso.png")),
                arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "geotherm003_iso.png")),
                arcade.load_texture(str(ASSET_PATH / "sprites_iso" / "geotherm004_iso.png"))
            ]
            self.frame_ind = 0
    
    def update_frame(self):
        self.frame_ind += 1
        if self.frame_ind == 4:
            self.frame_ind = 0
        self.texture = self.frame_textures[self.frame_ind]
    
    def check_build(self, build_type: str, lst_neighbours):
        if build_type in TILE_TYPE_BUILD[self.tile_type]:
            return True
        elif "factory" in build_type:
            tile_type_neighbours = []
            for neighbour in lst_neighbours:
                if neighbour:
                    tile_type_neighbours.append(neighbour.tile_type)
                else:
                    tile_type_neighbours.append('')
            if "tank" in tile_type_neighbours:
                return True
        return False


class TileList(arcade.SpriteList):
    def __init__(self):
        super(TileList, self).__init__()

        self.tile_coords_dict = {}

    def append(self, sprite: Tile):
        """Inserts the tile at the end of the sprite list and Stores them in a dict as a value and their
         isometric coordinates as key.
        """
        super(TileList, self).append(sprite=sprite)
        self.tile_coords_dict[(sprite.isometric_x, sprite.isometric_y)] = sprite

    def get(self, isometric_x: int, isometric_y: int):
        return self.tile_coords_dict.get((isometric_x, isometric_y), None)

    def get_all_tile_type(self):
        return [obj.tile_type for obj in self]
 
    def replace(self, sprite: Tile, other: Tile):
        """Replaces tile."""
        other.isometric_x = sprite.isometric_x
        other.isometric_y = sprite.isometric_y
        other.center_x = sprite.center_x
        other.center_y = sprite.center_y
        self.remove(sprite)
        self.append(other)

    def get_neighbours(self, sprite: Tile) -> List[Tile]:
        """Returns a list containing the neighbours of tile in the format (N, NE, E, SE, S, SW, W, NW)"""
        north_tile = self.get(sprite.isometric_x, sprite.isometric_y + 1)
        north_east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y + 1)
        east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y)
        south_east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y - 1)
        south_tile = self.get(sprite.isometric_x, sprite.isometric_y - 1)
        south_west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y - 1)
        west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y)
        north_west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y + 1)

        # removed excessive error handling.
        # try:
        #     north_tile = self.get(sprite.isometric_x, sprite.isometric_y + 1).tile_type
        # except AttributeError:
        #     north_tile = ''
        # try:
        #     north_east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y + 1).tile_type
        # except AttributeError:
        #     north_east_tile = ''
        # try:
        #     east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y).tile_type
        # except AttributeError:
        #     east_tile = ''
        # try:
        #     south_east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y - 1).tile_type
        # except AttributeError:
        #     south_east_tile = ''
        # try:
        #     south_tile = self.get(sprite.isometric_x, sprite.isometric_y - 1).tile_type
        # except AttributeError:
        #     south_tile = ''
        # try:
        #     south_west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y - 1).tile_type
        # except AttributeError:
        #     south_west_tile = ''
        # try:
        #     west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y).tile_type
        # except AttributeError:
        #     west_tile = ''
        # try:
        #     north_west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y + 1).tile_type
        # except AttributeError:
        #     north_west_tile = ''
        return (north_tile, north_east_tile, east_tile, south_east_tile,
                south_tile, south_west_tile, west_tile, north_west_tile)
