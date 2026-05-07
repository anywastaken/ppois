import pygame
import json
import sys
import random

from src.models.Ship import Ship
from src.models.Asteroid import Asteroid
from src.models.UFO import UFO
from src.models.PowerUp import PowerUp
from src.models.Particle import Particle

from src.utils.HighScoreManager import HighScoreManager
from src.utils.Button import Button

class AsteroidsGame:
    def __init__(self):
        """Инициализация игры и загрузка основных ресурсов"""
        pygame.init()

        self.config = self.load_config("configs/config.json")

        self.screen = pygame.display.set_mode((
            self.config["screen"]["width"], 
            self.config["screen"]["height"]
        ))
        pygame.display.set_caption(self.config["screen"]["title"])
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        self.ship = Ship(self.config)
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        for _ in range(self.config["asteroid"]["count"]):
            self.asteroids.add(Asteroid(self.config))
        
        self.last_asteriod_spawn_time = pygame.time.get_ticks()
        self.last_ufo_spawn_time = pygame.time.get_ticks()

        self.score = 0

        self.level = 0

        self.ufos = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()

        self.powerups = pygame.sprite.Group()
        self.powerup_time_to_spawn = self.config["powerups"]["spawn_points"]
        self.powerup_was_spawned_this_level = False

        self.hs_manager = HighScoreManager()
        self.user_name = ""

        center_x = self.config["screen"]["width"] // 2
        self.menu_buttons = [
            Button("START GAME", 40, center_x, 300),
            Button("HIGH SCORES", 40, center_x, 370),
            Button("HELP", 40, center_x, 440),
            Button("EXIT", 40, center_x, 510)
        ]

        self.particles = pygame.sprite.Group()

        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.config["audio"]["music_volume"])

        self.sounds = {}
        effects_cfg = self.config["audio"]["effects"]

        sound_files = {
            "shoot": "shoot.wav",
            "crash": "crash.wav",
            "powerup": "powerup.wav",
            "newrecord": "newrecord.mp3",
            "gameover": "gameover.mp3"
        }

        for key, file_name in sound_files.items():
            sound_path = f"assets/music/{file_name}"
            try:
                sound_obj = pygame.mixer.Sound(sound_path)
                volume = effects_cfg.get(key, 0.5) 
                sound_obj.set_volume(volume)
                self.sounds[key] = sound_obj
            except pygame.error as e:
                print(f"Не удалось загрузить звук {file_name}: {e}")

        self.play_bg_music("menu")

    def play_bg_music(self, track_name):
        """Воспроизведение фоновой музыки по имени трека"""
        pygame.mixer.music.load(f"assets/music/{track_name}.mp3")
        pygame.mixer.music.play(-1)

    def _add_segment_particles(self, position, base_velocity, segments, outward_scale, lifetime):
        """Создание частиц из набора линейных сегментов"""
        base_velocity = pygame.math.Vector2(base_velocity)

        for index, segment in enumerate(segments):
            start = pygame.math.Vector2(segment[0])
            end = pygame.math.Vector2(segment[1])
            midpoint = (start + end) / 2

            if midpoint.length_squared() == 0:
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = midpoint.normalize()

            tangent = pygame.math.Vector2(-direction.y, direction.x)
            tangent *= -1 if index % 2 else 1
            fragment_velocity = (
                base_velocity * 0.6
                + direction * outward_scale * (1 + index / max(1, len(segments)) * 0.35)
                + tangent * outward_scale * 0.18
            )
            angular_velocity = tangent.dot(fragment_velocity) * 0.35

            self.particles.add(
                Particle(
                    position=position + midpoint * 0.25,
                    velocity=fragment_velocity,
                    line=(start - midpoint, end - midpoint),
                    lifetime=lifetime,
                    angular_velocity=angular_velocity,
                )
            )

    def spawn_asteroid_explosion(self, asteroid):
        """Создание эффекта взрыва астероида"""
        center = pygame.math.Vector2(asteroid.radius, asteroid.radius)
        segments = []
        for index in range(len(asteroid.points)):
            start = pygame.math.Vector2(asteroid.points[index]) - center
            end = pygame.math.Vector2(asteroid.points[(index + 1) % len(asteroid.points)]) - center
            segments.append((start, end))
        self._add_segment_particles(asteroid.position, asteroid.velocity, segments, asteroid.radius * 0.06, 34)

    def spawn_ufo_explosion(self, ufo):
        """Создание эффекта взрыва НЛО"""
        radius = ufo.radius
        top_arc = [(-radius * 0.5, 0), (radius * 0.5, 0)]
        dome_left = [(-radius * 0.2, 0), (0, -radius * 0.45)]
        dome_right = [(0, -radius * 0.45), (radius * 0.2, 0)]
        body_top = [(-radius, radius * 0.1), (radius, radius * 0.1)]
        body_bottom = [(-radius * 0.65, radius * 0.35), (radius * 0.65, radius * 0.35)]
        body_left = [(-radius, radius * 0.1), (-radius * 0.65, radius * 0.35)]
        body_right = [(radius, radius * 0.1), (radius * 0.65, radius * 0.35)]
        segments = [top_arc, dome_left, dome_right, body_top, body_bottom, body_left, body_right]
        self._add_segment_particles(ufo.position, ufo.velocity, segments, radius * 0.11, 32)

    def spawn_ship_explosion(self):
        """Создание эффекта взрыва корабля игрока"""
        size = self.ship.size
        points = [
            pygame.math.Vector2(0, -size),
            pygame.math.Vector2(-size * 0.7, size * 0.8),
            pygame.math.Vector2(size * 0.7, size * 0.8),
        ]
        segments = [
            (points[0], points[1]),
            (points[0], points[2]),
            (points[1], points[2]),
        ]
        rotated_segments = []
        for start, end in segments:
            rotated_segments.append((start.rotate(-self.ship.angle), end.rotate(-self.ship.angle)))
        self._add_segment_particles(
            self.ship.position,
            self.ship.speed,
            rotated_segments,
            size * 0.17,
            36,
        )


    def reset_game(self):
        """Сброс игрового состояния к начальному"""
        self.ship = Ship(self.config)
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.ufos = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.score = 0
        self.level = 1
        self.powerups = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.powerup_time_to_spawn = self.config["powerups"]["spawn_points"]
        self.powerup_was_spawned_this_level = False
        self.lives = self.config["game"]["initial_lives"]
        self.ship.respawn()

        for _ in range(self.config["asteroid"]["count"]):
            self.asteroids.add(Asteroid(self.config))

    def load_config(self, path):
        """Загрузка конфигурации игры из JSON-файла"""
        with open(path, 'r') as f:
            return json.load(f)

    def handle_events(self):
        """Обработка событий клавиатуры и мыши"""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state in ["GAME", "HIGHSCORES", "HELP"]:
                        if self.state in ["GAME"]: self.play_bg_music("menu")
                        self.state = "MENU"
                        pygame.mouse.set_visible(True)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "MENU":
                    if self.menu_buttons[0].rect.collidepoint(mouse_pos):
                        self.reset_game()
                        self.play_bg_music("game")
                        self.state = "GAME"
                    elif self.menu_buttons[1].rect.collidepoint(mouse_pos):
                        self.state = "HIGHSCORES"
                    elif self.menu_buttons[2].rect.collidepoint(mouse_pos):
                        self.state = "HELP"
                    elif self.menu_buttons[3].rect.collidepoint(mouse_pos):
                        self.running = False

            if self.state == "INPUT_NAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.hs_manager.add_score(self.user_name, self.score)
                        self.state = "MENU"
                        self.play_bg_music("menu")
                        self.user_name = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    else:
                        if len(self.user_name) < 10:
                            self.user_name += event.unicode

    def calculate_points(self, size):
        """Расчет очков за уничтожение объекта"""
        points = 0
        if size == self.config["asteroid"]["size_large"]: points = 20
        if size == self.config["asteroid"]["size_large"]//2: points = 50
        if size == self.config["asteroid"]["size_large"]//4: points = 100
        if size == self.config["ufo"]["big_size"]: points = 100
        if size == self.config["ufo"]["small_size"]: points = 200
        if self.ship.active_powerups["double_score"] > 0:
            return points*2
        return points
        

    def process_input(self):
        """Обработка удерживаемых клавиш во время игры"""
        if self.state != "GAME":
            return

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.ship.rotate(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.ship.rotate(1)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.ship.accelerate()
        if keys[pygame.K_SPACE]:
            new_bullet = self.ship.shoot()
            if new_bullet:
                self.sounds["shoot"].play()
                self.bullets.add(new_bullet)

    def update(self):
        """Обновление состояния игры и всех игровых объектов"""
        self.particles.update()

        if self.state == "MENU":
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.menu_buttons:
                btn.check_hover(mouse_pos)

        if self.state == "GAME":
            # objects update
            self.ship.update()
            self.bullets.update()
            self.asteroids.update()
            self.ufo_bullets.update()
            self.powerups.update()


            # ufo shooting
            for ufo in self.ufos:
                ufo.update(self.ship.position)
                new_bullet = ufo.shoot(self.ship.position)
                if new_bullet:
                    self.ufo_bullets.add(new_bullet)


            # asteroids spawn
            now = pygame.time.get_ticks()
            if now - self.last_asteriod_spawn_time > self.config["level"]["asteroid_spawn_delay"] * \
                self.config["level"]["progression_coefficient"]**self.level:
                if len(self.asteroids) < self.config["level"]["asteroids_max_amount"] + \
                    self.config["level"]["asteroids_increase_amount_per_level"]:
                    self.asteroids.add(Asteroid(self.config))
                    self.last_asteriod_spawn_time = now


            # ufo spawn
            if self.level>=self.config["level"]["ufo_spawn_start"]:
                if now - self.last_ufo_spawn_time > self.config["level"]["ufo_spawn_delay"] * \
                    self.config["level"]["progression_coefficient"]**self.level:
                    self.last_ufo_spawn_time = now
                    if len(self.ufos) < self.config["level"]["ufo_max_amount"] + \
                        self.config["level"]["ufo_increase_amount_per_level"]:
                        is_small = random.random() < self.config["ufo"]["small_chance"]
                        self.ufos.add(UFO(self.config, is_small))

                
            # powerups spawn
            if self.score >= self.powerup_time_to_spawn and not self.powerup_was_spawned_this_level:
                powerup_type = random.choice(self.config["powerups"]["types"])
                self.powerups.add(PowerUp(self.config, powerup_type))
                self.powerup_time_to_spawn += 1000
                self.powerup_was_spawned_this_level = True


            # powerup_activation
            powerup_hits = pygame.sprite.spritecollide(self.ship, self.powerups, True)
            for powerup in powerup_hits:
                # Активируем на время из конфига
                self.sounds["powerup"].play()
                duration = self.config["powerups"]["duration"]
                self.ship.active_powerups[powerup.type] = pygame.time.get_ticks() + duration


            # asteriods collision
            hits = pygame.sprite.groupcollide(self.asteroids, self.bullets, True, True)
            for asteroid in hits:
                self.spawn_asteroid_explosion(asteroid)
                self.score += self.calculate_points(asteroid.radius)
                small_asteroids = asteroid.split()
                if small_asteroids:
                    self.asteroids.add(small_asteroids)


            # ufo collision
            hits = pygame.sprite.groupcollide(self.ufos, self.bullets, True, True)
            for ufo in hits:
                self.spawn_ufo_explosion(ufo)
                self.score += self.calculate_points(ufo.radius)


            # ship collision
            ship_asteroid_hits = pygame.sprite.spritecollide(
                self.ship, self.asteroids, False, pygame.sprite.collide_mask
            )
            ship_ufo_bullet_hits = pygame.sprite.spritecollide(
                self.ship, self.ufo_bullets, True, pygame.sprite.collide_mask
            )
            ship_ufo_hits = pygame.sprite.spritecollide(
                self.ship, self.ufos, False, pygame.sprite.collide_mask
            )

            if self.ship.active_powerups["shield"] > 0:
                for asteroid in ship_asteroid_hits:
                    if not asteroid.alive():
                        continue
                    self.spawn_asteroid_explosion(asteroid)
                    self.score += self.calculate_points(asteroid.radius)
                    small_asteroids = asteroid.split()
                    asteroid.kill()
                    if small_asteroids:
                        self.asteroids.add(small_asteroids)
                    self.sounds["crash"].play()

                for ufo in ship_ufo_hits:
                    if not ufo.alive():
                        continue
                    self.spawn_ufo_explosion(ufo)
                    self.score += self.calculate_points(ufo.radius)
                    ufo.kill()
                    self.sounds["crash"].play()

            elif ship_asteroid_hits or ship_ufo_bullet_hits or ship_ufo_hits:
                if self.lives > 0:
                    self.spawn_ship_explosion()
                    self.sounds["crash"].play()
                    self.lives -= 1
                    self.ship.respawn()
                else:
                    self.spawn_ship_explosion()
                    self.sounds["crash"].play()
                    pygame.mixer.music.stop()
                    if self.hs_manager.check_new_record(self.score):
                        self.play_bg_music("newrecord")
                        self.state = "INPUT_NAME"
                    else:
                        self.sounds["gameover"].play()
                        self.state = "MENU"
                        self.play_bg_music("menu")


            # level update
            if self.score >= self.level*self.config["level"]["points_per_level"]:
                self.level += 1
                self.powerup_was_spawned_this_level = False
                

    def draw(self):
        """Отрисовка текущего состояния игры на экране"""
        self.screen.fill(self.config["colors"]["black"])
        center_x = self.config["screen"]["width"] // 2
        self.particles.draw(self.screen)
        
        if self.state == "MENU":
            self.draw_text("ASTEROIDS", 72, center_x, 150)
            for btn in self.menu_buttons:
                btn.draw(self.screen)

        elif self.state == "HIGHSCORES":
            self.draw_text("TOP PILOTS", 48, center_x, 100)

            scores = self.hs_manager.load_scores()
            
            for i, entry in enumerate(scores):
                y_pos = 180 + i * 35
                name_text = f"{i+1}. {entry['name']}"
                score_text = str(entry['score'])

                self.draw_text(name_text, 24, center_x - 100, y_pos)
                self.draw_text(score_text, 24, center_x + 100, y_pos)
                
            self.draw_text("Press ESC to return", 20, center_x, 550)
        
        elif self.state == "GAME":
            self.draw_lives()
            self.ship.draw(self.screen)
            self.bullets.draw(self.screen)
            self.asteroids.draw(self.screen)
            self.ufos.draw(self.screen)
            self.ufo_bullets.draw(self.screen)
            self.powerups.draw(self.screen)
            self.draw_text(f"Score: {self.score}", 24, 70, 30)
            self.draw_text(f"level: {self.level}", 24, 70, 90)

        if self.state == "INPUT_NAME":
            self.draw_text("NEW HIGH SCORE!", 48, center_x, 200)
            self.draw_text(f"Your Score: {self.score}", 32, center_x, 260)
            self.draw_text("Enter your name:", 24, center_x, 320)
            self.draw_text(self.user_name + "_", 40, center_x, 380)

        elif self.state == "HELP":
            self.draw_text("HOW TO PLAY", 48, center_x, 100)

            rules = [
                "UP - Thrust (move forward)",
                "LEFT / RIGHT - Rotate ship",
                "SPACE - Fire cannons",
                "",
                "MODIFIERS:",
                "- Shield (protection)",
                "- Rapid Fire",
                "- Double Score",
                "",
                "Press ESC to return to Menu"
            ]
            
            for i, line in enumerate(rules):
                self.draw_text(line, 24, center_x, 200 + i * 30)

        pygame.display.flip()


    def draw_lives(self):
        """Отрисовка количества жизней"""
        for i in range(self.lives):
            x = 30 + i * 30
            y = 60
            size = 10
            points = [
                (x, y - size),
                (x - size//1.5, y + size),
                (x + size//1.5, y + size)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 255), points, 2)
    

    def draw_text(self, text, size, x, y):
        """Отрисовка текста по заданным координатам"""
        font = pygame.font.SysFont("Arial", size)
        text_surface = font.render(text, True, self.config["colors"]["white"])
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)


    def run(self):
        """Запуск основного игрового цикла"""
        while self.running:
            self.handle_events()
            self.process_input()
            self.update()
            self.draw()
            self.clock.tick(self.config["screen"]["fps"])
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = AsteroidsGame()
    game.run()
