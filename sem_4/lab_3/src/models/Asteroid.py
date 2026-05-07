import pygame
import random
import math

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, config, size=None, position=None):
        """Инициализация астероида с формой и движением"""
        super().__init__()
        self.config = config
        self.radius = size if size else self.config["asteroid"]["size_large"]

        if position:
            self.position = pygame.math.Vector2(position)
        else:
            self.position = self._get_random_offscreen_pos()

        speed = random.uniform(*self.config["asteroid"]["speed_range"])
        angle = random.uniform(0, 360)
        self.velocity = pygame.math.Vector2(0, speed).rotate(angle)

        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.points = self._generate_rock_shape()
        pygame.draw.polygon(self.image, (255, 255, 255), self.points, 2)

        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def _get_random_offscreen_pos(self):
        """Выбор случайной стартовой позиции вне экрана"""
        w = self.config["screen"]["width"]
        h = self.config["screen"]["height"]
        side = random.randint(0, 3)
        if side == 0: return pygame.math.Vector2(random.randint(0, w), -self.radius)
        if side == 1: return pygame.math.Vector2(random.randint(0, w), h + self.radius)
        if side == 2: return pygame.math.Vector2(-self.radius, random.randint(0, h))
        return pygame.math.Vector2(w + self.radius, random.randint(0, h))

    def _generate_rock_shape(self):
        """Генерация набора точек для формы астероида"""
        points = []
        num_points = 12
        for i in range(num_points):
            angle = (i / num_points) * math.pi * 2
            offset = random.uniform(self.radius * 0.7, self.radius)
            x = self.radius + math.cos(angle) * offset
            y = self.radius + math.sin(angle) * offset
            points.append((x, y))
        return points

    def update(self):
        """Обновление позиции астероида на экране"""
        self.position += self.velocity
        self.rect.center = self.position

        self.position.x %= self.config["screen"]["width"]
        self.position.y %= self.config["screen"]["height"]

    def split(self):
        """Создание осколков при разрушении астероида"""
        result = []
        if self.radius > self.config["asteroid"]["min_size"]:
                    new_radius = self.radius // 2
                    
                    asteroids_amount = random.randint(0,2)
                    for _ in range(asteroids_amount):
                        small_asteroid = Asteroid(self.config, size=new_radius, position=self.position)
                        small_asteroid.velocity *= 1.5 
                        result.append(small_asteroid)
        return result
