import numpy as np
import time
from Objects.Rocket import Rocket
from Objects.Wind import WindMenager
from Settings import Settings

class Simulation:

    def __init__(self, ships_params : dict, num_of_ships = 1) -> None:
        self.ships = []
        self.forces = np.array([[0], [0]], float)
        self.settings = Settings()
        self.wind = WindMenager(self.settings)
        self.wind.calc_speed()
        for i in range (num_of_ships):
            self.ships.append(Rocket(self.settings, self.wind, ships_params[i]["pos"], ships_params[i]["mass"], ships_params[i]["vel"], ships_params[i]["acc"], ships_params[i]["angle"]))

    # def _apply_forces_to_ships (self):
    #     for ship in self.ships:
    #         ship.apply_static_forces()
    #         if ship.pos[1][0] < 0:
    #             ship.vel *= 0
    #             ship.pos[1][0] = 0

    def _update_ships (self) -> None:
        for ship in self.ships:
            ship.apply_static_forces()
            ship.update(self.d_time)

    def run (self, d_time) -> None:
        self.d_time = d_time
        # self._apply_forces_to_ships()
        self._update_ships()

