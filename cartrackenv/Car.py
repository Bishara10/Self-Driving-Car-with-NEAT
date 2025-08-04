import pygame
from pygame import SRCALPHA

import constants
import math

class Car(pygame.sprite.Sprite):
    def __init__(self, posx: float, posy: float):
        super().__init__()

        self.position = posx, posy
        image = pygame.image.load("assets/car2.png").convert_alpha()
        self.original_image = pygame.transform.scale(image, (90, 41))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

        self.velocity = constants.CAR_MAX_SPEED * pygame.math.Vector2(-1, 0)
        self.angle = 0
        self.rot_angle_speed = 1.9

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def updateVelocityVector(self):
        radians = math.radians(self.angle)
        vertical = constants.CAR_MAX_SPEED * math.sin(radians)
        horizontal = constants.CAR_MAX_SPEED * math.cos(radians)

        self.velocity.x = -horizontal
        self.velocity.y = vertical

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rot_angle_speed
        if keys[pygame.K_LEFT]:
            self.angle += self.rot_angle_speed

        self.updateVelocityVector()
        self.rotate()

        self.position += self.velocity
        self.rect.center = self.position





