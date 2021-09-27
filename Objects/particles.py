from re import S
from typing import Match
import numpy as np
import random as rand
import pyglet

from numpy.core.fromnumeric import argpartition, partition

class Particle:

    def __init__(self, settings, id, pos : np.ndarray, vel : np.ndarray, angle : int, size : float, color : tuple, deacrising_value : float) -> None:
        self.id = id
        self.pos = pos
        self.vel = vel 
        self.angle = angle
        self.size = size # 0 - 1
        self.color = color # white / yellow / orange / red
        self.deacrising_value = deacrising_value # how particle fast particle is going to disappear 
        self.settings = settings
        self.shape = pyglet.shapes.Circle(self.pos[0][0], self.pos[1][0], self.size * 10, color = self.color)

        if self.angle < 90:
            self.vel[0][0] *= -1
        
        elif self.angle < 180:
            pass

        elif self.angle < 270:
            self.vel[1][0] *= -1

        else:
            self.vel[1][0] *= -1
            self.vel[0][0] *= -1

    def update (self, d_time):

        self.pos = self.pos + self.vel * d_time

        self.size *= self.deacrising_value
        print(f"Id: {self.id} Pos: {self.pos} Vel:{self.vel} angle: {self.angle} size: {self.size} color: {self.color} dea_value: {self.deacrising_value}")
        print(type(self.color))

        if self.color == -1 or self.size < 0.1:
            del(self)
            return
        
        return 1 if self.color != -1 else 0

    def draw (self):
        self.shape.x = self.pos[0][0]
        self.shape.y = self.pos[1][0]
        self.shape.color = self.color
        self.shape.radius = self.size * 10
        self.shape.draw()

class ParticleMenager:

    def __init__(self, settings, pos : np.ndarray, energy, degrees : tuple) -> None:
        self.pos = pos
        self.energy = energy
        self.degrees = degrees
        self.particles = []
        self.settings = settings

    def spawn_particles (self):
        particle_id = 0
        particles_per_angle = int(self.energy / (self.degrees[1] - self.degrees[0]) + 1)
        for a in range (self.degrees[0], self.degrees[1]):
            for i in range (particles_per_angle):
                color = rand.randint(1, 30)
                if color < 14:
                    color_tuple = self.settings.colors["red"]
                
                elif color < 22:
                    color_tuple = self.settings.colors["orange"]

                elif color < 27 :
                    color_tuple = self.settings.colors["yellow"]

                else: 
                    color_tuple = self.settings.colors["white"]

                vx = rand.randint(5, 15)
                vy = rand.randint(5, 15)
                s = rand.random()
                if s < 0.5:
                    s += 0.5
                self.particles.append(Particle(self.settings, particle_id, self.pos, np.array([[vx], [vy]]), angle = a, size = s, color = color_tuple, deacrising_value = rand.random()))
                particle_id += 1
        

    def update_particles (self, d_time):

        for particle in self.particles:
            if not particle.update (d_time):
                self.particles.remove(particle)

    def draw_particles (self):
        
        for particle in self.particles:
            particle.draw()