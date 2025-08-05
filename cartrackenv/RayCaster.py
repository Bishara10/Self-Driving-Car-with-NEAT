from Ray import *
import constants
from Car import Car

class RayCaster():
    def __init__(self, player: Car):
        self.rays = []
        self.player = player

    def cast_all_rays(self, screen):
        self.rays.clear()

        ray_angle = math.radians(118 + self.player.angle - constants.FOV/2)
        ray_length = 120
        for i in range(constants.NUM_RAYS):
            ray1 = Ray(ray_angle, ray_length, self.player.rect.center)
            ray2 = Ray(ray_angle, ray_length//2, self.player.rect.center)
            ray1.draw(screen)
            ray2.draw(screen)
            self.rays.append(ray1)
            self.rays.append(ray2)

            ray_angle += constants.FOV/constants.NUM_RAYS

    def render(self, screen):
        for ray in self.rays:
            ray.render(screen)
