import math
import pathlib

from arcade import color

# Dimensions and title
SCREEN_TITLE = "Marrrs Explorer"
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

# Arcade style dicts
STYLE_GOLDEN_TANOI = {"font_name": "Dilo World", "font_color": (255, 207, 112), "bg_color": (0, 140, 176),
                      "border_color": (0, 60, 75)}
STYLE_DANGER = {
    "font_color": color.WHITE,
    "border_width": 2,
    "bg_color": (217, 4, 41),
    "bg_color_pressed": (255, 166, 158),
    "border_color_pressed": (255, 166, 158)

}

STYLE_PRIMARY = {
    "font_color": color.WHITE,
    "border_width": 2,
    "bg_color": (52, 152, 219),
    "bg_color_pressed": (41, 128, 185),
    "border_color_pressed": (41, 128, 185)
}

# Paths
PATH = pathlib.Path(__file__).resolve().parent.parent
ASSET_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"
SRC_PATH = pathlib.Path(__file__).resolve().parent.parent / "src"

# Camera
CAMERA_MOVEMENT_SPEED = 5
VIEWPORT_ANGLE = math.pi / 4
INVERT_MOUSE = True

# Initial ressource

RESSOURCES_LIST = ['H2O', 'CO2', 'C', 'H', 'O2', 'Fe', 'Poly', 'Ener', 'Money', 'Food']
INITIAL_RESSOURCES_LEVEL_0 = {'H2O': 100,
                              'CO2': 100,
                              'C': 100,
                              'H': 100,
                              'O2': 100,
                              'Fe': 100,
                              'Poly': 0,
                              'Ener': 0,
                              'Money': 0,
                              'Food' : 100,
                              'Crew' : 1}

# Initial storage without improvement
INITIAL_MAXIMAL_RESSOURCES_LEVEL_0 = {'H2O': 1000,
                                      'CO2': 1000,
                                      'C': 1000,
                                      'H': 1000,
                                      'O2': 1000,
                                      'Fe': 1000,
                                      'Poly': 1000,
                                      'Ener': 1000,
                                      'Money': 100000,
                                      'Food': 1000,
                                      'Crew':1}

RESSOURCE_GENERATION = {'h2o_liquid_generator': 2 / 60,
                        'h2o_ice_generator': 1 / 60,
                        'h2o_vapor_generator': 3 / 60,
                        'co2_generator': 2 / 60,
                        'fe_generator': 3 / 60,
                        'co2_breaker_factory': 1 / 60,
                        'h2o_breaker_factory': 1 / 60,
                        'poly_factory': 0.5 / 60,
                        'solar_pannel': 2 / 60,
                        'geothermal_generator': 5 / 60,
                        'garden': 2 / 60}

TANK_STORAGE = {'h2o_tank': 100,
                'co2_tank': 100,
                'c_tank': 100,
                'h_tank': 100,
                'o2_tank': 100,
                'fe_tank': 100,
                'poly_tank': 100,
                'ener_tank': 100,
                'food_tank': 100,
                'bases' : 5}

BUILDING_LIST =    ['h2o_liquid_generator',
                    'h2o_ice_generator',
                    'h2o_vapor_generator',
                    'co2_generator',
                    'fe_generator',
                    'co2_breaker_factory',
                    'h2o_breaker_factory',
                    'poly_factory',
                    'solar_pannel',
                    'geothermal_generator',
                    'garden',
                    'h2o_tank',
                    'co2_tank',
                    'c_tank',
                    'h_tank',
                    'o2_tank',
                    'fe_tank',
                    'poly_tank',
                    'ener_tank',
                    'food_tank',
                    'bases']

CREW_MEMBER_TO_OPERATE = {'h2o_liquid_generator': 2,
                            'h2o_ice_generator': 1,
                            'h2o_vapor_generator': 3,
                            'co2_generator': 2,
                            'fe_generator': 1,
                            'co2_breaker_factory': 3,
                            'h2o_breaker_factory': 2, 
                            'poly_factory': 2, 
                            'solar_pannel': 1, 
                            'geothermal_generator': 5, 
                            'garden': 1, 
                            'h2o_tank': 1, 
                            'co2_tank': 1,
                            'c_tank': 1, 
                            'h_tank': 1, 
                            'o2_tank': 1, 
                            'fe_tank': 1, 
                            'poly_tank': 1,
                            'ener_tank': 1, 
                            'food_tank': 1, 
                            'bases': 0}

ENER_PER_BUILDING = {'h2o_liquid_generator': 2 / 60,
                    'h2o_ice_generator': 1 / 60,
                    'h2o_vapor_generator': 5 / 60,
                    'co2_generator': 1 / 60,
                    'fe_generator': 1 / 60,
                    'co2_breaker_factory': 2 / 60,
                    'h2o_breaker_factory': 2 / 60, 
                    'poly_factory': 1 / 60, 
                    'garden': 1 / 60,  
                    'bases': 1 / 60}
        
# Resource density

IRON_RICH_TILE = 0.5
VOLCANO = 0.1
CARBON_DIOXIDE_GEYSERS = 0.4
ICY_TILE = 1.0
CRATER = 33.0
LAND = 100 - (IRON_RICH_TILE + VOLCANO + CARBON_DIOXIDE_GEYSERS + ICY_TILE + CRATER)

# Total day time in second

DAY_TOTAL_TIME = 240
BRIGHTNESS_TIME = [0, DAY_TOTAL_TIME / 5.6, DAY_TOTAL_TIME / 4, DAY_TOTAL_TIME / 2,
                   DAY_TOTAL_TIME / 1.4, DAY_TOTAL_TIME / 1.3, DAY_TOTAL_TIME]
BRIGHTNESS_VALUE = [0.25, 0.4, 0.7, 1, 0.6, 0.3, 0.25]

O2_CONSUMPTION = 2 / 60
FOOD_CONSUMPTION_PER_MEMBER_CREW = 2 / 60
CREW_PER_BASES = 5
PARTY_TIME = 600