# import os
import math

import pygame
from pygame.locals import *
from constants import *
from Car import Car
from RayCaster import RayCaster
from Ray import Ray

class Game:
    def __init__(self):
        pygame.init()
        # pygame.mixer.init()
        # pygame.font.init()
        # current_dir = os.path.dirname(os.path.abspath(__file__))

        # init main display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Car AI')

        # ground
        self.ground_surf = pygame.image.load('assets/grass.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # car track
        self.track_surf = pygame.image.load("assets/track.png").convert_alpha()
        self.track_rect = self.track_surf.get_rect(topleft=(0, 0))
        # self.track_borders_mask = self._getTrackBorders()

        # track boundaries
        self.track_boundaries_surf = pygame.image.load("assets/track_borders.png")
        self.track_rect = self.track_surf.get_rect(topleft=(0, 0))
        self.track_boundaries_mask = pygame.mask.from_surface(self.track_boundaries_surf)

        self.car = Car(900, 830)
        self.raycaster = RayCaster(self.car)

        self.objects_to_draw = [(self.ground_surf, (0, 0)),
                                (self.track_boundaries_surf, (0, 0)),
                                (self.track_surf, (0, 0)) ]

        self.clock = pygame.time.Clock()

    @staticmethod
    def _handleEvents():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    @staticmethod
    def _distance(point1, point2):
        return math.sqrt((point1[0]-point2[0]) ** 2 + (point1[1]-point2[1]) ** 2)

    def _drawObjects(self, objects: list[tuple[pygame.surface.Surface, tuple[int, int]]]):
        for image, pos in objects:
            self.screen.blit(image, pos)

        self.screen.blit(self.car.image, self.car.rect)

    @staticmethod
    def _checkMaskCollision(obj1: pygame.mask.Mask, obj2: pygame.mask.Mask,
                            obj1_pos: tuple[int, int], obj2_pos: tuple[int, int]) -> tuple[int, int]:
        offset_x = obj2_pos[0] - obj1_pos[0]
        offset_y = obj2_pos[1] - obj1_pos[1]
        offset = (offset_x, offset_y)

        collision = obj1.overlap(obj2, offset)

        return collision

    def step(self):
        self.clock.tick(90)

        # An array to store all the distances for long and short rays
        all_ray_collision_points_distances = []
        # An array to store all distances for nearest ray collision points to the car
        nearest_rays_collision_points_distances = []

        # Handle events
        self._handleEvents()

        # Draw background and track
        self._drawObjects(self.objects_to_draw)

        # Cast rays
        self.raycaster.cast_all_rays(self.screen)

        # Check if player collides with track wall
        if self._checkMaskCollision(self.car.mask, self.track_boundaries_mask, self.car.rect.topright, (0, 0)):
            pass

        # Check rays collisions with track border
        for ray in self.raycaster.rays:
            collision = self._checkMaskCollision(ray.mask, self.track_boundaries_mask, ray.rect.topleft, (0, 0))
            distance = 120 # max ray distance
            if collision:
                # Get the real collision point location by adding the ray's location
                collision_point = (ray.rect.left + collision[0], ray.rect.top + collision[1])
                # display a circle to mark the collision point
                pygame.draw.circle(self.screen, (0, 255, 200), collision_point, 4)
                #measure distance between collision point and the car center
                distance = self._distance(self.car.rect.center, collision_point)

            # add the distance to the array storing all distances of possible collision points for all rays.
            all_ray_collision_points_distances.append(distance)

        # Loop through all ray collision distances for long and short rays, and calculate the minimum distance of
        # collision points between the corresponding long and short rays.
        for i in range(0, len(all_ray_collision_points_distances), 2):
            long_ray_collision_point = all_ray_collision_points_distances[i]
            short_ray_collision_point = all_ray_collision_points_distances[i+1]
            nearest_rays_collision_points_distances.append(min(long_ray_collision_point, short_ray_collision_point))

        self.car.update()
        pygame.display.update()
#
# g = Game()
# while True:
#     g.step()