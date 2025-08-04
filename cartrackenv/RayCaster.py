from Ray import *
import constants
from Car import Car

class RayCaster():
    def __init__(self, player: Car):
        self.rays = []
        self.player = player

    def cast_all_rays(self):
        self.rays.clear()

        ray_angle = math.radians(115 + self.player.angle - constants.FOV/2)
        for i in range(constants.NUM_RAYS):
            ray = Ray(ray_angle, self.player.rect.center)
            ray.cast()
            self.rays.append(ray)

            ray_angle += constants.FOV/constants.NUM_RAYS

    def render(self, screen):
        for ray in self.rays:
            ray.render(screen)
