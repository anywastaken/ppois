import pygame
import random
import math

from src.models.Bullet import Bullet

class UFO(pygame.sprite.Sprite):
    def __init__(self, config, is_small=False):
        """Инициализация НЛО и его параметров"""
        super().__init__()
        self.config = config
        self.is_small = is_small
        self.radius = config["ufo"]["small_size"] if is_small else config["ufo"]["big_size"]

        self.side = random.choice([-1, 1])
        x = 0 if self.side == 1 else config["screen"]["width"]
        y = random.randint(50, config["screen"]["height"] - 50)
        
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(self.side * config["ufo"]["speed"], 0)

        self.last_dir_change = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()

        self.image = pygame.Surface((self.radius * 2, self.radius), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 255, 255), [0, self.radius//4, self.radius*2, self.radius//2], 2)
        pygame.draw.arc(self.image, (255, 255, 255), [self.radius//2, 0, self.radius, self.radius], 0, math.pi, 2)
        
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, ship_pos):
        """Обновление позиции и поведения НЛО"""
        self.position += self.velocity

        now = pygame.time.get_ticks()
        if now - self.last_dir_change > 2000:
            self.velocity.y = random.choice([-1, 0, 1])
            self.last_dir_change = now
            
        self.rect.center = self.position

        if not (0 <= self.position.x <= self.config["screen"]["width"]):
            self.kill()

    def shoot(self, ship_pos):
        """Создание пули НЛО при готовности к выстрелу"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.config["ufo"]["shoot_delay"]:
            self.last_shot = now

            if self.is_small:
                direction = ship_pos - self.position
                angle = -math.degrees(math.atan2(direction.y, direction.x)) - 90
            else:
                angle = random.uniform(0, 360)
                
            return Bullet(self.config, self.position, angle)
        return None
