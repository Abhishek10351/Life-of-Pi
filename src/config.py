import math
import pathlib

from arcade import color

# Dimensions and title
SCREEN_TITLE = "Marrrs Explorer"
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

# Map size
MAP_SIZE_X = 10
MAP_SIZE_Y = 10

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
                              'Ener': 100,
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

TANK_STORAGE = {'tank': 100,
                'ener_tank': 100,
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
                    'tank',
                    'ener_tank',
                    'bases',
                    'asteroid_defence',
                    'stormshield']

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
                            'tank': 1, 
                            'ener_tank': 1,  
                            'bases': 0,
                            'asteroid_defence': 5,
                            'stormshield': 5}

ENER_PER_BUILDING = {'h2o_liquid_generator': 2 / 60,
                    'h2o_ice_generator': 1 / 60,
                    'h2o_vapor_generator': 5 / 60,
                    'co2_generator': 1 / 60,
                    'fe_generator': 1 / 60,
                    'co2_breaker_factory': 2 / 60,
                    'h2o_breaker_factory': 2 / 60, 
                    'poly_factory': 1 / 60, 
                    'garden': 1 / 60,  
                    'bases': 1 / 60,
                    'asteroid_defence': 2 / 60,
                    'stormshield': 2 / 60}

RESSOURCE_TO_BUILD = {'base': {'H2O': 0, 'CO2': 0, 'H': 0,'C': 0,'Fe': 20,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['bases']},
                        'garden': {'H2O': 30, 'CO2': 10, 'H': 0,'C': 0,'Fe': 0,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['garden']},
                        'solar': {'H2O': 0, 'CO2': 0, 'H': 10,'C': 10,'Fe': 10,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['solar_pannel']},
                        'geo': {'H2O': 30, 'CO2': 10, 'H': 10,'C': 20,'Fe': 30,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['geothermal_generator']},
                        'battery': {'H2O': 0, 'CO2': 0, 'H': 10,'C': 10,'Fe': 10,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['ener_tank']},
                        'iceextract': {'H2O': 10, 'CO2': 0, 'H': 10,'C': 10,'Fe': 20,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['h2o_ice_generator']},
                        'co2extract': {'H2O': 10, 'CO2': 0, 'H': 10,'C': 10,'Fe': 20,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['co2_generator']},
                        'fe_mining': {'H2O': 10, 'CO2': 10, 'H': 0,'C': 0,'Fe': 20,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['fe_generator']},
                        'factory_co2': {'H2O': 0, 'CO2': 0, 'H': 0,'C': 0,'Fe': 20,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['co2_breaker_factory']},
                        'factory_h2o': {'H2O': 0, 'CO2': 0, 'H': 0,'C': 0,'Fe': 20,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['h2o_breaker_factory']},
                        'factory_poly':{'H2O': 10, 'CO2': 10, 'H': 10,'C': 20,'Fe': 30,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['poly_factory']},
                        'tank': {'H2O': 0, 'CO2': 0, 'H': 0,'C': 0,'Fe': 10,'Poly': 0, 'Crew':CREW_MEMBER_TO_OPERATE['h2o_tank']},
                        'asteroid_defence': {'H2O': 0, 'CO2': 0, 'H': 0,'C': 0,'Fe': 20,'Poly': 10, 'Crew':CREW_MEMBER_TO_OPERATE['asteroid_defence']},
                        'stormshield': {'H2O': 0, 'CO2': 0, 'H': 0,'C': 0,'Fe': 20,'Poly': 10, 'Crew':CREW_MEMBER_TO_OPERATE['stormshield']}}
        
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

# Tile build dict

TILE_TYPE_BUILD = {"crater": (),
                   "fe_crater": "fe_mining",
                   "geyser": "co2extract",
                   "ice": ("iceextract", "factory_h2o"),
                   "land": ("base", "garden", "solar", "tank", "battery","asteroid_defence","stormshield"),
                   "volcano": "geo"
                   }

FOOD_CONSUMPTION_PER_MEMBER_CREW = 2 / 60
CREW_PER_BASES = 5
PARTY_TIME = 600
