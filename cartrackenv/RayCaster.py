import pygame
from Ray import *
import constants

class RayCaster():
    def __init__(self, player):
        self.rays = []
        self.player = player

    def cast_all_rays(self, group):
        for ray in self.rays:
            ray.kill()

        ray_angle = (self.player.direction - constants.FOV/2)
        for i in range(constants.NUM_RAYS):
            ray = Ray(ray_angle, self.player.rect.center, group)
            ray.cast()
            self.rays.append(ray)

            ray_angle += constants.FOV/constants.NUM_RAYS

    def render(self, screen):
        for ray in self.rays:
            ray.render(screen)
