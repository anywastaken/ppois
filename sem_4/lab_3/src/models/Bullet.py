import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, config, pos, angle):
        """Инициализация пули с направлением движения"""
        super().__init__()
        self.config = config

        self.position = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, -self.config["bullet"]["speed"]).rotate(angle)
        
        self.lifetime = self.config["bullet"]["lifetime"]
        self.image = pygame.Surface((self.config["bullet"]["size"] * 2, self.config["bullet"]["size"] * 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        """Обновление позиции и времени жизни пули"""
        self.position += self.velocity
        self.rect.center = self.position

        self.position.x %= self.config["screen"]["width"]
        self.position.y %= self.config["screen"]["height"]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
