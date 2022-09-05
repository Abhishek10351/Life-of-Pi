from config import (INITIAL_MAXIMAL_RESSOURCES_LEVEL_0,
                    INITIAL_RESSOURCES_LEVEL_0, RESSOURCE_GENERATION,
                    TANK_STORAGE)


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

        self.initial_maximum_h2o = INITIAL_MAXIMUM_RESSOURCES['H2O']
        self.initial_maximum_co2 = INITIAL_MAXIMUM_RESSOURCES['CO2']
        self.initial_maximum_c = INITIAL_MAXIMUM_RESSOURCES['C']
        self.initial_maximum_h = INITIAL_MAXIMUM_RESSOURCES['H']
        self.initial_maximum_o2 = INITIAL_MAXIMUM_RESSOURCES['O2']
        self.initial_maximum_fe = INITIAL_MAXIMUM_RESSOURCES['Fe']
        self.initial_maximum_poly = INITIAL_MAXIMUM_RESSOURCES['Poly']
        self.initial_maximum_energy = INITIAL_MAXIMUM_RESSOURCES['Ener']
        self.initial_maximum_money = INITIAL_MAXIMUM_RESSOURCES['Money']

        self.current_ressource = {'H2O': self.initial_h2o,
                                  'CO2': self.initial_co2,
                                  'C': self.initial_c,
                                  'H': self.initial_h,
                                  'O2': self.initial_o2,
                                  'Fe': self.initial_fe,
                                  'Poly': self.initial_poly,
                                  'Ener': self.initial_energy,
                                  'Money': self.initial_money}

        self.maximum_ressource = {'H2O': self.initial_maximum_h2o,
                                  'CO2': self.initial_maximum_co2,
                                  'C': self.initial_maximum_c,
                                  'H': self.initial_maximum_h,
                                  'O2': self.initial_maximum_o2,
                                  'Fe': self.initial_maximum_fe,
                                  'Poly': self.initial_maximum_poly,
                                  'Ener': self.initial_maximum_energy,
                                  'Money': self.initial_maximum_money}

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

        self.h2o_tank = 0
        self.co2_tank = 0
        self.c_tank = 0
        self.h_tank = 0
        self.o2_tank = 0
        self.fe_tank = 0
        self.poly_tank = 0
        self.ener_tank = 0

    def update(self) -> None:
        """
        Update the amount of stored ressource when called
        """
        self.update_h2o()
        self.update_co2()
        self.update_fe()
        self.update_polymer()
        self.update_energy()
        self.update_money()
        self.update_storage_capacity()

        self._check_maximum_overpass()

    def _check_maximum_overpass(self) -> None:
        for key in self.current_ressource.keys():
            if self.current_ressource[key] > self.maximum_ressource[key]:
                self.current_ressource[key] = self.maximum_ressource[key]

    def update_storage_capacity(self) -> None:
        """Updates the resource capacity for each of the resource."""
        self.maximum_ressource['H2O'] = self.initial_maximum_h2o + self.h2o_tank * TANK_STORAGE['h2o_tank']
        self.maximum_ressource['CO2'] = self.initial_maximum_co2 + self.co2_tank * TANK_STORAGE['co2_tank']
        self.maximum_ressource['C'] = self.initial_maximum_c + self.c_tank * TANK_STORAGE['c_tank']
        self.maximum_ressource['H'] = self.initial_maximum_h + self.h_tank * TANK_STORAGE['h_tank']
        self.maximum_ressource['O2'] = self.initial_maximum_o2 + self.o2_tank * TANK_STORAGE['o2_tank']
        self.maximum_ressource['Fe'] = self.initial_maximum_fe + self.fe_tank * TANK_STORAGE['fe_tank']
        self.maximum_ressource['Poly'] = self.initial_maximum_poly + self.poly_tank * TANK_STORAGE['poly_tank']
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
