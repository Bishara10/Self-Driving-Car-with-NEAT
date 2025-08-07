import pygame, math
from Car import Car

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if angle < 0:
        angle = (2 * math.pi) + angle

    return angle

class Ray(pygame.sprite.Sprite):
    def __init__(self, angle, length, player_pos: tuple[int, int]):
        super().__init__()
        self.ray_angle = -angle
        self.length = length
        self.px, self.py = player_pos

        surf = pygame.Surface((self.length, 1), pygame.SRCALPHA)
        surf.fill((255, 255, 255))
        self.surf = pygame.transform.rotate(surf, math.degrees(angle))
        self.mask = pygame.mask.from_surface(self.surf)

        rx = (self.length * math.cos(angle))/2 + self.px
        ry = -(self.length * math.sin(angle))/2 + self.py

        # and shift it so that the start point aligns with the player
        self.rect = self.surf.get_rect(center=(rx, ry))


    def draw(self, screen):
        screen.blit(self.surf, self.rect)
