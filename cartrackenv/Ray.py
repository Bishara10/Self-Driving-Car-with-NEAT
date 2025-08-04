import pygame, math

def normalizeAngle(angle):
    angle = angle % (2 * math.pi)
    if (angle < 0):
        angle = (2 * math.pi) + angle

    return angle

class Ray(pygame.sprite.Sprite):
    def __init__(self, angle, player, group):
        super().__init__(group)
        self.ray_angle = angle
        self.player = player
        self.length = 150

        self.image = pygame.Surface((self.length, 1), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

    def cast(self):
        pass

    def update(self):
        # Compute ray end point
        dx = math.cos(self.ray_angle) * self.length
        dy = math.sin(self.ray_angle) * self.length

        # Create image surface large enough to fit the ray
        width = abs(dx) + 2
        height = abs(dy) + 2
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # Draw the ray line on the image
        start = self.player
        end = (dx, dy)
        pygame.draw.line(self.image, (255, 255, 255), start, end, 1)

        # Set the rect to follow the player
        self.rect = self.image.get_rect()
        self.rect.center = self.player


    def render(self, screen):
        # Temp
        print(self.player)
        pygame.draw.line(screen, (255, 255, 255), (self.player[0], self.player[1]), (self.player[0] + math.cos(self.ray_angle) * 150, self.player[1] + math.sin(self.ray_angle) * 150))

    

