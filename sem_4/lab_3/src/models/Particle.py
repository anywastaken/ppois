import math

import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        velocity,
        line,
        lifetime=36,
        angular_velocity=0,
        damping=0.97,
        color=(255, 255, 255),
    ):
        """Инициализация частицы для визуальных эффектов"""
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(velocity)
        self.line = [pygame.math.Vector2(point) for point in line]
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.angle = 0
        self.angular_velocity = angular_velocity
        self.damping = damping
        self.color = color

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.position)
        self._rebuild_image()

    def _rebuild_image(self):
        """Пересборка изображения частицы с учетом поворота"""
        alpha = max(0, min(255, int(255 * (self.lifetime / self.max_lifetime))))
        rotated_points = [point.rotate(self.angle) for point in self.line]

        min_x = min(point.x for point in rotated_points)
        max_x = max(point.x for point in rotated_points)
        min_y = min(point.y for point in rotated_points)
        max_y = max(point.y for point in rotated_points)

        padding = 3
        width = max(1, math.ceil(max_x - min_x) + padding * 2)
        height = max(1, math.ceil(max_y - min_y) + padding * 2)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        start = rotated_points[0] - pygame.math.Vector2(min_x, min_y) + (padding, padding)
        end = rotated_points[1] - pygame.math.Vector2(min_x, min_y) + (padding, padding)
        pygame.draw.line(self.image, (*self.color, alpha), start, end, 2)
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        """Обновление движения и времени жизни частицы"""
        self.position += self.velocity
        self.velocity *= self.damping
        self.angle += self.angular_velocity
        self.lifetime -= 1

        if self.lifetime <= 0:
            self.kill()
            return

        self._rebuild_image()
