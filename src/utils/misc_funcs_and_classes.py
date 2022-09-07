from math import sqrt
# using typing because we need it to be compatible with 3.8 and 3.9 too.
from typing import List

import arcade

from config import TILE_TYPE_BUILD, MAP_SIZE_X, MAP_SIZE_Y


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

    def check_build(self, build_type: str, tile_sprite_list, lst_neighbours):
        if build_type in TILE_TYPE_BUILD[self.tile_type]:
            return True
        elif build_type == "factory_poly":
            print(lst_neighbours)
            if "tank" in lst_neighbours:
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
        try:
            north_tile = self.get(sprite.isometric_x, sprite.isometric_y + 1).tile_type
        except AttributeError:
            north_tile = ''
        try:
            north_east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y + 1).tile_type
        except AttributeError:
            north_east_tile = ''
        try:
            east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y).tile_type
        except AttributeError:
            east_tile = ''
        try:
            south_east_tile = self.get(sprite.isometric_x + 1, sprite.isometric_y - 1).tile_type
        except AttributeError:
            south_east_tile = ''
        try:
            south_tile = self.get(sprite.isometric_x, sprite.isometric_y - 1).tile_type
        except AttributeError:
            south_tile = ''
        try:
            south_west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y - 1).tile_type
        except AttributeError:
            south_west_tile = ''
        try:
            west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y).tile_type
        except AttributeError:
            west_tile = ''
        try:
            north_west_tile = self.get(sprite.isometric_x - 1, sprite.isometric_y + 1).tile_type
        except AttributeError:
            north_west_tile = ''
        return (north_tile, north_east_tile, east_tile, south_east_tile,
                south_tile, south_west_tile, west_tile, north_west_tile)
