import numpy as np
import time
from Objects.Rocket import Rocket
from Settings import Settings

class Simulation:

    def __init__(self, ships_params : dict, num_of_ships = 1) -> None:
        self.ships = []
        self.forces = np.array([[0], [0]], float)
        self.settings = Settings()
        self.gravity = np.array([[0],[self.settings.gravity]], float)
        for i in range (num_of_ships):
            self.ships.append(Rocket(ships_params["pos"], ships_params["mass"], ships_params["vel"], ships_params["acc"], ships_params["angle"]))

    def _apply_forces_to_ships (self):
        for i, ship in enumerate(self.ships):
            ship.apply_force(self.forces[i])
            ship.apply_thrust(np.array([[0],[self.settings.engine1]], float))
            if ship.pos[1][0] > 10:
                ship.apply_gravity(self.gravity)

    def _update_ships (self) -> None:
        for ship in self.ships:
            ship.update(self.d_time)

    def run (self, d_time) -> None:        
        self.d_time = d_time
        self._apply_forces_to_ships()
        self._update_ships()

