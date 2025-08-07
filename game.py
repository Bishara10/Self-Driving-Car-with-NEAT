import math
import pygame
from pygame.locals import *
from constants import *
from Car import Car
from RayCaster import RayCaster

class Game:
    def __init__(self, population_number):
        pygame.init()
        # pygame.mixer.init()
        # pygame.font.init()

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

        self.cars_alive = population_number
        self.cars = [Car(900, 830) for _ in range(population_number)]
        self.raycasters = [RayCaster(self.cars[i]) for i in range(population_number)]
        # self.genomes = genomes

        self.objects_to_draw = [(self.ground_surf, (0, 0)),
                                (self.track_boundaries_surf, (0, 0)),
                                (self.track_surf, (0, 0))]

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

        for car in self.cars:
            self.screen.blit(car.image, car.rect)

    @staticmethod
    def _checkMaskCollision(obj1: pygame.mask.Mask, obj2: pygame.mask.Mask,
                            obj1_pos: tuple[int, int], obj2_pos: tuple[int, int]) -> tuple[int, int]:
        offset_x = obj2_pos[0] - obj1_pos[0]
        offset_y = obj2_pos[1] - obj1_pos[1]
        offset = (offset_x, offset_y)

        collision = obj1.overlap(obj2, offset)

        return collision

    def step(self, actions:list):
        """Advances the game by 1 frame.
            @:param - actions: a list of actions for each car.
            @:return - destroyed_cars_indices: a list indicating at which indices the destroyed cars are located
                        in self.cars list,
                       nearest_rays_collision_points_distances: An array to store all distances for nearest ray collision
                        points to the car.

        """
        self.clock.tick(60)

        # Destroyed cars' indices in self.cars
        destroyed_cars_indices: list[int] = []
        # An array to store all distances for nearest ray collision points to the car. Will be used
        # as input to train the genome of the corresponding car
        nearest_rays_collision_points_distances: list[tuple] = []

        # Handle events
        self._handleEvents()

        # Draw background and track
        self._drawObjects(self.objects_to_draw)

        # Cast rays
        for raycaster in self.raycasters:
            raycaster.cast_all_rays(self.screen)

        # Move cars and check for collisions
        for i, car in enumerate(self.cars):
            car.action(actions[i])
            car.update()
            if self._checkMaskCollision(car.mask, self.track_boundaries_mask, car.rect.topleft, (0, 0)):
                car.destroy()
                self.cars_alive -= 1
                destroyed_cars_indices.append(i)


        # An array to store all the distances for long and short rays
        all_ray_collision_points_distances = []
        # Check rays collisions with track border for each car
        for raycaster in self.raycasters:
            curr_car_distances = []
            for ray in raycaster.rays:
                collision = self._checkMaskCollision(ray.mask, self.track_boundaries_mask, ray.rect.topleft, (0, 0))
                distance = 120 # max ray distance
                if collision:
                    # Get the real collision point location by adding the ray's location
                    collision_point = (ray.rect.left + collision[0], ray.rect.top + collision[1])
                    # display a circle to mark the collision point
                    pygame.draw.circle(self.screen, (0, 255, 200), collision_point, 4)
                    #measure distance between collision point and the car center
                    distance = self._distance(raycaster.car.rect.center, collision_point)

                # add the distance to the array storing all distances of possible collision points for all rays.
                curr_car_distances.append(distance)

            all_ray_collision_points_distances.append(curr_car_distances)

        # Loop through all ray collision distances for long and short rays, and calculate the minimum distance of
        # collision points between the corresponding long and short rays for all cars.
        for car_collision_distances in all_ray_collision_points_distances:
            curr_car_distances = []
            for i in range(0, len(car_collision_distances), 2):
                long_ray_collision_point = car_collision_distances[i]
                short_ray_collision_point = car_collision_distances[i+1]
                curr_car_distances.append(min(long_ray_collision_point, short_ray_collision_point))

            nearest_rays_collision_points_distances.append(tuple(curr_car_distances))

        pygame.display.update()

        #remove destroyed cars and their raycasters
        i = 0
        for index in destroyed_cars_indices:
            self.cars.pop(index-i)
            self.raycasters.pop(index-i)
            i+=1

        return nearest_rays_collision_points_distances, destroyed_cars_indices
