import pygame

import constants
import math

class Car(pygame.sprite.Sprite):
    def __init__(self, posx: float, posy: float):
        super().__init__()
        image = pygame.image.load("assets/car.png").convert_alpha()

        self.position = posx, posy
        self.original_image = pygame.transform.scale(image, (90, 41))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)
        self.alive = True  # is used to detect whether the car crashed or not

        self.speed = constants.CAR_MAX_SPEED
        self.velocity = self.speed * pygame.math.Vector2(-1, 0)
        self.rot_angle_speed = constants.Car_Rotation_Angle_Speed
        self.angle = 0

    # Rotate car image and rectangle to a certain angle
    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    # Change direction of velocity vector based on angle
    def updateVelocityVector(self):
        radians = math.radians(self.angle)
        vertical = self.speed * math.sin(radians)
        horizontal = self.speed * math.cos(radians)

        self.velocity.x = -horizontal
        self.velocity.y = vertical

    # Can turn left or right. this is done by changing the car angle
    def action(self, action):
        if action == 1:
            #turn left
            self.angle += self.rot_angle_speed
        elif action == 2:
            #turn right
            self.angle -= self.rot_angle_speed

    # override update method
    def update(self):
        self.updateVelocityVector()
        self.rotate()

        # the position of the car is tracked by self.position variable for better
        # precision and smoother rotations as self.position is a float variable.
        # later, the rectangle is updated based on the self.position variable.
        self.position += self.velocity
        self.rect.center = self.position

    # stops car from moving and marks it as not alive
    def destroy(self):
        self.speed = 0
        self.alive = False




