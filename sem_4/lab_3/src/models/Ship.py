import pygame
import math
from src.models.Bullet import Bullet

class Ship(pygame.sprite.Sprite):
    def __init__(self, config):
        """Инициализация корабля игрока"""
        super().__init__()
        self.config = config
        self.screen_width = config["screen"]["width"]
        self.screen_height = config["screen"]["height"]
        self.size = config["ship"]["size"]

        self.position = pygame.math.Vector2(self.screen_width // 2, self.screen_height // 2)
        self.speed = pygame.math.Vector2(0, 0)
        self.angle = 0 
        self.last_shot_time = 0

        self.original_image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self._render_ship()

        self.active_powerups = {
            "shield": 0,
            "rapid_fire": 0,
            "double_score": 0
        }

    def _render_ship(self):
        """Создание базового изображения корабля"""
        self.original_image.fill((0, 0, 0, 0))
        points = [
            (self.size, 0),
            (self.size // 3, self.size * 1.5),
            (self.size * 1.7, self.size * 1.5)
        ]
        pygame.draw.polygon(self.original_image, (255, 255, 255), points, 2)

    def rotate(self, direction):
        """Поворот корабля в заданную сторону"""
        self.angle += direction * self.config["ship"]["rotation_speed"]

    def accelerate(self):
        """Ускорение корабля по направлению его носа"""
        acceleration = pygame.math.Vector2(0, -self.config["ship"]["speed"]).rotate(self.angle)
        self.speed += acceleration

    def shoot(self):
        """Создание пули корабля с учетом скорострельности"""
        if self.active_powerups["rapid_fire"]>0:
            now = pygame.time.get_ticks()
            if now - self.last_shot_time > self.config["bullet"]["cooldown"]//2:
                self.last_shot_time = now
                return Bullet(self.config, self.position, self.angle)
            return None
        else:
            now = pygame.time.get_ticks()
            if now - self.last_shot_time > self.config["bullet"]["cooldown"]:
                self.last_shot_time = now
                return Bullet(self.config, self.position, self.angle)
            return None

    def update(self):
        """Обновление движения и эффектов корабля"""
        self.speed *= self.config["ship"]["friction"]
        self.position += self.speed

        self.position.x %= self.screen_width
        self.position.y %= self.screen_height

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.position)

        self.mask = pygame.mask.from_surface(self.image)

        now = pygame.time.get_ticks()
        for key in self.active_powerups:
            if self.active_powerups[key] > 0 and now > self.active_powerups[key]:
                self.active_powerups[key] = 0

    def draw(self, surface):
        """Отрисовка корабля и активного щита"""
        surface.blit(self.image, self.rect)
        if self.active_powerups["shield"] > 0:
            pygame.draw.circle(surface, (0, 255, 255), self.position, self.size * 1.8, 2)

    def respawn(self):
        """Возврат корабля в центр после потери жизни"""
        self.position = pygame.math.Vector2(
            self.config["screen"]["width"] // 2, 
            self.config["screen"]["height"] // 2
        )
        self.speed = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.active_powerups["shield"] = pygame.time.get_ticks() + self.config["game"]["respawn_shield_duration"]
