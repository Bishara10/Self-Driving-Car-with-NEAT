import os
import pygame
from pygame.locals import *
from random import randint
from constants import *
from Car import Car
from RayCaster import RayCaster
from Ray import Ray

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # init main display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Car AI')

        #ground
        self.ground_surf = pygame.image.load('assets/grass.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # car track
        self.track_surf = pygame.image.load("assets/track23.png").convert_alpha()
        self.track_rect = self.track_surf.get_rect(topleft=(0, 0))
        self.track_borders_mask = self._getTrackBorders()


        self.car = Car(900, 830)
        self.raycaster = RayCaster(self.car)

        self.objects_to_draw = [(self.ground_surf, (0, 0)), (self.track_surf, (0, 0))]

        self.clock = pygame.time.Clock()
        self.dt = 0

    def _getTrackBorders(self):
        ground_mask = pygame.mask.from_surface(self.ground_surf)
        track_mask = pygame.mask.from_surface(self.track_surf)

        ground_mask.erase(track_mask, (0, 0))

        return ground_mask

    @staticmethod
    def _handleEvents():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    @staticmethod
    def _checkMaskCollision(obj1: pygame.mask.Mask, obj2: pygame.mask.Mask, obj1_pos: tuple[int, int], obj2_pos: tuple[int, int]) -> tuple[int, int]:
        offset_x = obj2_pos[0] - obj1_pos[0]
        offset_y = obj2_pos[1] - obj1_pos[1]
        collision = obj1.overlap(obj2, (offset_x, offset_y))

        return collision

    @staticmethod
    def _checkRayCollision(ray: Ray):
        pass

    def _drawObjects(self, objects: list[tuple[pygame.surface.Surface, tuple[int, int]]]):
        for image, pos in objects:
            self.screen.blit(image, pos)

        self.screen.blit(self.car.image, self.car.rect)

    def step(self):
        self.clock.tick(90)
        self.dt = self.clock.get_time()

        # Handle events
        self._handleEvents()

        # Draw ground and track
        self._drawObjects(self.objects_to_draw)

        # Cast rays
        self.raycaster.cast_all_rays()
        self.raycaster.render(self.screen)

        # Check if player collides with track wall
        if self._checkCollision(self.car.mask, self.track_borders_mask, self.car.rect.topleft, (0, 0)):
            pass

        # Check rays collisions with track border


        self.car.update()
        pygame.display.update()
    

game = Game()
while(True):
    game.step()

