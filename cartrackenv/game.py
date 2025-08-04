import os
import pygame
from pygame.locals import *
from random import randint
from constants import *
from Car import Car
from RayCaster import RayCaster

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # init main display
        self.screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pygame.display.set_caption('Car AI')

        #ground
        self.ground_surf = pygame.image.load('graphics/grass.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # car track
        self.track_surf = pygame.image.load("graphics/track23.png").convert_alpha()
        self.track_rect = self.track_surf.get_rect(topleft=(0, 0))

        self.car = Car(900, 830)
        # self.raycaster = RayCaster(self.car)

        self.track_borders_mask = self._getTrackBorders()

        self.clock = pygame.time.Clock()
        self.dt = 0

    def _getTrackBorders(self):
        ground_mask = pygame.mask.from_surface(self.ground_surf)
        track_mask = pygame.mask.from_surface(self.track_surf)

        # track_mask.invert()
        ground_mask.erase(track_mask, (0, 0))
        # subtract_shape = subtract_masks.to_surface()
        # subtract_rect = subtract_masks.get_rect()

        return ground_mask


    @staticmethod
    def _handleEvents():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

    @staticmethod
    def _checkCollision(player: pygame.mask.Mask, obj: pygame.mask.Mask, player_pos: tuple[int, int], obj_pos: tuple[int, int]) -> bool:
        offset_x = obj_pos[0] - player_pos[0]
        offset_y = obj_pos[1] - player_pos[1]
        collision = player.overlap(obj, (offset_x, offset_y))

        # self.screen.blit(collision.to_surface(), (90, 90))
        # self.screen.blit(self.track_borders_surf, self.track_borders_rect)
        # self.screen.blit(self.car.image, self.car.position)
        return True if collision else False


    def step(self):
        self.clock.tick(90)
        self.dt = self.clock.get_time()

        # # Check collisions
        if self._checkCollision(self.car.mask, self.track_borders_mask, self.car.rect.topleft, (0, 0)):
            print("Collision")

        # Draw ground and track
        self.screen.blit(self.ground_surf, self.ground_rect)
        self.screen.blit(self.track_surf, self.track_rect)
        self.screen.blit(self.car.image, self.car.rect)
        self.car.update()

        # Handle events
        self._handleEvents()

        pygame.display.update()
    

game = Game()
while(True):
    game.step()

