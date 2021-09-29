import numpy as np
from .Engine import Engine

class Rocket:

    def __init__(self, settings, pos : np.ndarray, mass : float, vel : np.ndarray, acc : np.ndarray, angle : float  ) -> None:
        self.pos = pos
        self.acc = acc
        self.vel = vel
        self.mass = mass
        self.kinetic_energy = 0
        self.settings = settings

        self.torque = 0
        self.rotation_acc = 0
        self.rotational_speed = 0
        self.rotation_angle = angle

        self.fuel_percentage_left = 0.5 # 0 - 1
        self.fuel_mass : float = self.mass * self.settings.fuel_percentage * self.fuel_percentage_left
        self.ship_mass = (1 - self.settings.fuel_percentage) * self.mass
        
        self.static_forces = [self.settings.gravity]

        self.starting_mass = self.ship_mass + self.fuel_mass
        self.starting_fuel_mass = self.mass * self.settings.fuel_percentage 
        self.mass = self.starting_mass
        
        self.engines = [Engine(self, self.settings.engine1, 0, 5000, 90), Engine(self, self.settings.engine2, 90, 1000, 90), Engine(self, self.settings.engine2, -90, 1000, 90)]

    def update_mass (self):
        self.fuel_mass -= self.fuel_mass_burned

    def apply_static_forces(self):
        for static_force in self.static_forces:
            if self.pos[1][0] > 0:
                self.acc += static_force

    def apply_rotational_force (self):
        self.torque = self.rotation_force * self.distance_to_center_of_mass * 1000
        self.rotation_acc = self.torque / self.mass
        
        #print(f"T: {round(self.torque, 4)}, Angle: {round(self.rotation_angle, 4)} Engine angle {round(self.engines[0].angle, 2)}, Acc: {round(self.rotation_acc, 4)}, Vel: {round(self.rotational_speed, 4)}")

    def calc_kenergy (self):
        sum_v = (self.vel[0][0]**2 + self.vel[1][0]**2)**(1/2)
        self.kinetic_energy = self.mass * (sum_v**2) / 2

    def check_high (self):
        if self.pos[1][0] < 0:
            self.vel *= 0
            self.pos[1][0] = 0
    
    def update (self, d_time):
        for engine in self.engines:
            self.acc_engines, self.fuel_mass_burned, self.rotation_force, self.distance_to_center_of_mass = engine.update(d_time)
            # print(self.acc_engines)
            self.acc += self.acc_engines
            self.apply_rotational_force()
            self.update_mass()

        if self.fuel_mass < 0:
            for engine in self.engines:
                del (engine)
            self.engines.clear()
            self.acc = np.zeros((2, 1))
            self.rotation_acc = np.zeros((2, 1))

        self.rotational_speed += self.rotation_acc * d_time
        self.rotation_angle += self.rotational_speed * d_time

        self.vel += self.acc * d_time
        self.pos += self.vel * d_time

        self.acc = np.zeros((2, 1))

        self.check_high()

        self.mass = self.ship_mass + self.fuel_mass
        self.fuel_percentage_left = self.fuel_mass / self.starting_fuel_mass