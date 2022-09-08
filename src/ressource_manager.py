from operator import ge
from config import (INITIAL_MAXIMAL_RESSOURCES_LEVEL_0,

                    INITIAL_RESSOURCES_LEVEL_0, RESSOURCE_GENERATION,
                    TANK_STORAGE, O2_CONSUMPTION, FOOD_CONSUMPTION_PER_MEMBER_CREW,
                    CREW_PER_BASES, CREW_MEMBER_TO_OPERATE, RESSOURCES_LIST, ENER_PER_BUILDING)


class RessourceManager:
    """Manage the ressources owned by the player and the maximum amount of ressources that can be stored.
    Ressource is french of resource.

    Number of tanks, factories etc needs to be update by the Game class at each refresh
    """

    def __init__(self):
        # Setting up initial ressources and storage amount
        # pylint: disable=C0103
        INITIAL_RESSOURCES = INITIAL_RESSOURCES_LEVEL_0
        INITIAL_MAXIMUM_RESSOURCES = INITIAL_MAXIMAL_RESSOURCES_LEVEL_0

        self.initial_h2o = INITIAL_RESSOURCES['H2O']
        self.initial_co2 = INITIAL_RESSOURCES['CO2']
        self.initial_c = INITIAL_RESSOURCES['C']
        self.initial_h = INITIAL_RESSOURCES['H']
        self.initial_o2 = INITIAL_RESSOURCES['O2']
        self.initial_fe = INITIAL_RESSOURCES['Fe']
        self.initial_poly = INITIAL_RESSOURCES['Poly']
        self.initial_energy = INITIAL_RESSOURCES['Ener']
        self.initial_money = INITIAL_RESSOURCES['Money']
        self.initial_food = INITIAL_RESSOURCES['Food']
        self.initial_crew = INITIAL_RESSOURCES['Crew']

        self.initial_maximum_h2o = INITIAL_MAXIMUM_RESSOURCES['H2O']
        self.initial_maximum_co2 = INITIAL_MAXIMUM_RESSOURCES['CO2']
        self.initial_maximum_c = INITIAL_MAXIMUM_RESSOURCES['C']
        self.initial_maximum_h = INITIAL_MAXIMUM_RESSOURCES['H']
        self.initial_maximum_o2 = INITIAL_MAXIMUM_RESSOURCES['O2']
        self.initial_maximum_fe = INITIAL_MAXIMUM_RESSOURCES['Fe']
        self.initial_maximum_poly = INITIAL_MAXIMUM_RESSOURCES['Poly']
        self.initial_maximum_energy = INITIAL_MAXIMUM_RESSOURCES['Ener']
        self.initial_maximum_money = INITIAL_MAXIMUM_RESSOURCES['Money']
        self.initial_maximum_food = INITIAL_MAXIMUM_RESSOURCES['Food']
        self.initial_maximum_crew = INITIAL_MAXIMUM_RESSOURCES['Crew']
        
        self.possible_tile_type = {'base':['bases'],
                                'garden':['garden'],
                                'solar':['solar_pannel'],
                                'geo':['geothermal_generator'],
                                'battery':['ener_tank'],
                                'iceextract':['h2o_ice_generator'],
                                'co2extract':['co2_generator'],
                                'fe_mining':['fe_generator'],
                                'factory_co2':['co2_breaker_factory'],
                                'factory_h2o':['h2o_breaker_factory'],
                                'factory_poly':['poly_factory'],
                                'tank':['tank'],
                                'asteroid_defence':['asteroid_defence'],
                                'stormshield':['stormshield']}

        self.current_ressource = {'H2O': self.initial_h2o,
                                  'CO2': self.initial_co2,
                                  'C': self.initial_c,
                                  'H': self.initial_h,
                                  'O2': self.initial_o2,
                                  'Fe': self.initial_fe,
                                  'Poly': self.initial_poly,
                                  'Ener': self.initial_energy,
                                  'Money': self.initial_money,
                                  'Food': self.initial_food,
                                  'Total_crew': self.initial_crew,
                                  'Crew' : self.initial_crew}

        self.maximum_ressource = {'H2O': self.initial_maximum_h2o,
                                  'CO2': self.initial_maximum_co2,
                                  'C': self.initial_maximum_c,
                                  'H': self.initial_maximum_h,
                                  'O2': self.initial_maximum_o2,
                                  'Fe': self.initial_maximum_fe,
                                  'Poly': self.initial_maximum_poly,
                                  'Ener': self.initial_maximum_energy,
                                  'Money': self.initial_maximum_money,
                                  'Food': self.initial_maximum_food,
                                  'Crew': self.initial_maximum_crew}

        self.h2o_liquid_generator = 0
        self.h2o_ice_generator = 0
        self.h2o_vapor_generator = 0
        self.co2_generator = 0
        self.fe_generator = 0
        self.co2_breaker_factory = 0
        self.h2o_breaker_factory = 0
        self.poly_factory = 0
        self.solar_pannel = 0
        self.geothermal_generator = 0
        self.garden = 0

        self.tank = 0
        self.ener_tank = 0
        self.bases = 0
        
        self.asteroid_defence = 0
        self.stormshield = 0
        
        #if energy comes down to 0, will be turn to False and factories wont work anymore until energy comes back to 0
        self.enable_factory = True

    def update(self, tile_sprite_list) -> None:
        """
        Update the amount of stored ressource when called
        """
        if self.enable_factory:
            self.update_h2o()
            self.update_co2()
            self.update_fe()
            self.update_polymer()
        self.update_energy()
        self.update_money()
        self.update_food()
        self.update_crew()
        self.o2_consumption()
        self.update_storage_capacity()

        self._check_maximum_overpass()

    def update_building(self, build_type) -> None:
        for building in self.possible_tile_type[build_type]:
            setattr(self, building, getattr(self, building) + 1)
        
    def destroy_building(self, targets) -> None:
        for target in targets:
            for building in self.possible_tile_type[target.tile_type]:
                setattr(self, building, getattr(self, building) - 1)
            
    
    def check_for_resource(self, resource_to_build) -> bool:
        for key, item in resource_to_build.items():
            if self.current_ressource[key] < item:
                return False
        return True

    def consume_resource_to_build(self, resource_to_build) -> None:
        for key, item in resource_to_build.items():
            self.current_ressource[key] -= item
    
    def o2_consumption(self) -> None:
        """Function that simulate the O2 consumption"""
        self.current_ressource['O2'] -= O2_CONSUMPTION

    def update_food(self) -> None:
        """Function that simulate the food production and consumption"""
        self.current_ressource['Food'] -= FOOD_CONSUMPTION_PER_MEMBER_CREW * self.current_ressource['Total_crew']
        if self.enable_factory:
            self.current_ressource['Food'] += self.garden * RESSOURCE_GENERATION['garden']
        
    def update_crew(self) -> None:
        #You have a total crew of 1 (yourself) when you don't have bases
        self.maximum_ressource['Crew'] =  1 + (CREW_PER_BASES * self.bases)
        self.current_ressource['Total_crew'] = 1 + (CREW_PER_BASES * self.bases)
        self.current_ressource['Crew'] = self.current_ressource['Total_crew']
        for key, item in CREW_MEMBER_TO_OPERATE.items():
            self.current_ressource['Crew'] -= getattr(self, key) * item
    
    def _check_maximum_overpass(self) -> None:
        for key in RESSOURCES_LIST:
            if self.current_ressource[key] > self.maximum_ressource[key]:
                self.current_ressource[key] = self.maximum_ressource[key]

    def update_storage_capacity(self) -> None:
        """Updates the resource capacity for each of the resource."""
        self.maximum_ressource['H2O'] = self.initial_maximum_h2o + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['CO2'] = self.initial_maximum_co2 + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['C'] = self.initial_maximum_c + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['H'] = self.initial_maximum_h + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['O2'] = self.initial_maximum_o2 + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['Fe'] = self.initial_maximum_fe + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['Poly'] = self.initial_maximum_poly + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['Food'] = self.initial_maximum_food + self.tank * TANK_STORAGE['tank']
        self.maximum_ressource['Ener'] = self.initial_maximum_energy + self.ener_tank * TANK_STORAGE['ener_tank']

    def update_h2o(self) -> None:
        """
        Update H2O ressource
        """
        add_h2o = self.h2o_liquid_generator * RESSOURCE_GENERATION['h2o_liquid_generator'] \
            + self.h2o_ice_generator * RESSOURCE_GENERATION['h2o_ice_generator'] \
            + self.h2o_vapor_generator * RESSOURCE_GENERATION['h2o_vapor_generator']
        self.current_ressource['H2O'] += add_h2o
        if self.current_ressource['H2O'] - RESSOURCE_GENERATION['h2o_breaker_factory'] * self.h2o_breaker_factory >= 0:
            self.current_ressource['H2O'] -= RESSOURCE_GENERATION['h2o_breaker_factory'] * self.h2o_breaker_factory
            self.current_ressource['O2'] += RESSOURCE_GENERATION['h2o_breaker_factory'] * self.h2o_breaker_factory / 2
            self.current_ressource['H'] += RESSOURCE_GENERATION['h2o_breaker_factory'] * self.h2o_breaker_factory * 2
        else:
            self.current_ressource['O2'] += self.current_ressource['H2O'] / 2
            self.current_ressource['H'] += self.current_ressource['H2O'] * 2
            self.current_ressource['H2O'] = 0

    def update_co2(self) -> None:
        """
        Update CO2 ressource
        """
        self.current_ressource['CO2'] += RESSOURCE_GENERATION['co2_generator'] * self.co2_generator
        if self.current_ressource['CO2'] - RESSOURCE_GENERATION['co2_breaker_factory'] * self.co2_breaker_factory >= 0:
            self.current_ressource['CO2'] -= RESSOURCE_GENERATION['co2_breaker_factory'] * self.co2_breaker_factory
            self.current_ressource['O2'] += RESSOURCE_GENERATION['co2_breaker_factory'] * self.co2_breaker_factory
            self.current_ressource['C'] += RESSOURCE_GENERATION['co2_breaker_factory'] * self.co2_breaker_factory
        else:
            self.current_ressource['O2'] += self.current_ressource['CO2']
            self.current_ressource['C'] += self.current_ressource['CO2']
            self.current_ressource['CO2'] = 0

    def update_fe(self) -> None:
        """
        Update Fe ressource
        """
        self.current_ressource['Fe'] += RESSOURCE_GENERATION['fe_generator'] * self.fe_generator

    def update_polymer(self) -> None:
        """
        Update Poly ressource
        """
        if self.current_ressource['C'] - RESSOURCE_GENERATION['poly_factory'] * self.poly_factory >= 0 and \
                self.current_ressource['H'] - RESSOURCE_GENERATION['poly_factory'] * self.poly_factory >= 0:
            self.current_ressource['Poly'] += RESSOURCE_GENERATION['poly_factory'] * self.poly_factory
            self.current_ressource['C'] -= RESSOURCE_GENERATION['poly_factory'] * self.poly_factory
            self.current_ressource['H'] -= RESSOURCE_GENERATION['poly_factory'] * self.poly_factory
        elif self.current_ressource['C'] - RESSOURCE_GENERATION['poly_factory'] * self.poly_factory >= 0:
            self.current_ressource['Poly'] += self.current_ressource['H']
            self.current_ressource['C'] -= self.current_ressource['H']
            self.current_ressource['H'] -= 0
        elif self.current_ressource['H'] - RESSOURCE_GENERATION['poly_factory'] * self.poly_factory >= 0:
            self.current_ressource['Poly'] += self.current_ressource['C']
            self.current_ressource['H'] -= self.current_ressource['C']
            self.current_ressource['C'] -= 0

    def update_energy(self) -> None:
        """
        Update Energy ressource
        """

        self.current_ressource['Ener'] += RESSOURCE_GENERATION['solar_pannel'] * self.solar_pannel \
                                          + RESSOURCE_GENERATION['geothermal_generator'] * self.geothermal_generator
        if self.enable_factory:
            for key, item in ENER_PER_BUILDING.items():
                self.current_ressource['Ener'] -= getattr(self, key) * item
        if self.current_ressource['Ener'] < 0:
            self.enable_factory = False
            self.current_ressource['Ener'] = 0

    def update_money(self) -> None:
        """
        Update money ressource
        """


if __name__ == '__main__':
    rm = RessourceManager()
    print(rm.current_ressource)
    for i in range(15):
        rm.update()
        print(rm.current_ressource)
        print('\n')
