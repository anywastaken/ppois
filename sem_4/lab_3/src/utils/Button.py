import pygame

class Button:
    def __init__(self, text, size, x, y, color=(255, 255, 255), hover_color=(0, 255, 255)):
        """Инициализация кнопки интерфейса"""
        self.text = text
        self.font = pygame.font.SysFont("Arial", size)
        self.color = color
        self.hover_color = hover_color

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=(x, y))
        self.is_hovered = False

    def draw(self, surface):
        """Отрисовка кнопки с учетом наведения курсора"""
        current_color = self.hover_color if self.is_hovered else self.color
        self.image = self.font.render(self.text, True, current_color)
        surface.blit(self.image, self.rect)

    def check_hover(self, mouse_pos):
        """Проверка наведения курсора на кнопку"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
