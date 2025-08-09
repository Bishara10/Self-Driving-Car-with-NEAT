import pygame, math


class Ray(pygame.sprite.Sprite):
    def __init__(self, angle, length, player_pos: tuple[int, int]):
        super().__init__()
        self.ray_angle = -angle
        self.length = length
        self.px, self.py = player_pos

        surf = pygame.Surface((self.length, 1), pygame.SRCALPHA)
        surf.fill((255, 255, 255))

        # rotate the surface towards the middle of the car
        self.surf = pygame.transform.rotate(surf, math.degrees(angle))
        self.mask = pygame.mask.from_surface(self.surf)

        # calculate the middle point for the ray
        rx = (self.length * math.cos(angle))/2 + self.px
        ry = -(self.length * math.sin(angle))/2 + self.py

        # shift the ray so that its start point becomes the player's center point
        self.rect = self.surf.get_rect(center=(rx, ry))


    def draw(self, screen):
        screen.blit(self.surf, self.rect)
