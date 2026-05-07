import pygame
import random
import os

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, config, p_type):
        """Инициализация бонуса выбранного типа"""
        super().__init__()
        self.config = config
        self.type = p_type
        
        path = os.path.join("assets", "images", "powerups", f"{p_type}.png")
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except pygame.error:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 0, 255))

        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(
            random.randint(50, config["screen"]["width"] - 50),
            random.randint(50, config["screen"]["height"] - 50)
        )
        self.rect.center = self.position
        self.spawn_time = pygame.time.get_ticks()

    def _get_color(self):
        """Возврат цвета бонуса по его типу"""
        if self.type == "shield": return (0, 255, 255)
        if self.type == "rapid_fire": return (255, 255, 0)
        return (255, 0, 255)

    def update(self):
        """Удаление бонуса по истечении времени жизни"""
        if pygame.time.get_ticks() - self.spawn_time > self.config["powerups"]["lifetime"]:
            self.kill()
