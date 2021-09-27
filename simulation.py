import numpy as np
import time
from .Objects.Rocket import Rocket
from Settings import Settings

class Simulation:

    def __init__(self, ships_params : dict, num_of_ships = 1) -> None:
        self.ships = []
        self.forces = np.zeros()
        self.settings = Settings()
        for i in range (num_of_ships):
            self.ships.append(Rocket(ships_params["pos"], ships_params["mass"], ships_params["vel"], ships_params["acc"], ships_params["angle"]))

        self.run()

    def _apply_forces_to_ships (self, forces):
        for i, ship in enumerate(self.ships):
            ship.apply_force(forces[i])

    def _update_ships (self) -> None:
        for ship in self.ships:
            ship.update()

    def run (self) -> None:

        self.start_time = time.time()
        
        while 1:
            d_time = time.time() - self.start_time
            self._apply_forces_to_ships()
            self._update_ships(d_time)

