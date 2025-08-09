from Ray import *
import constants
from Car import Car

# Responsible for casting rays
class RayCaster():
    def __init__(self, car: Car):
        self.rays = []  # array of rays
        self.collision_points = []  # point of collision between rays and track boundaries
        self.car = car  # corresponding car

    # Cast rays by creating Ray objects and adding them to self.rays array
    # each ray consists of 2 rays: long and short one. They both have the same
    # exact functionality, but the short ray makes sure that the boundaries detected
    # are close to the car, as long ray can detect boundaries that are not reachable by the
    # car at its specific position.
    def cast_all_rays(self, screen):
        self.rays.clear()
        self.collision_points.clear()

        # cast rays depending on their corresponding angle
        ray_angle = math.radians(118 + self.car.angle - constants.FOV / 2)
        ray_length = 120
        for i in range(constants.NUM_RAYS):
            # long ray
            ray1 = Ray(ray_angle, ray_length, self.car.rect.center)
            # short ray
            ray2 = Ray(ray_angle, ray_length//2, self.car.rect.center)
            ray1.draw(screen)
            ray2.draw(screen)
            self.rays.append(ray1)
            self.rays.append(ray2)

            ray_angle += constants.FOV / constants.NUM_RAYS

    def render(self, screen):
        for ray in self.rays:
            ray.render(screen)

