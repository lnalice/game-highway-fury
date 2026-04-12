"""Player car entity with character-specific abilities."""

import math
import random
import pygame

from highway_fury.config import (
    HEIGHT, LANE_CENTERS, ROAD_LEFT, ROAD_RIGHT,
    DIFFICULTY_PRESETS, CHARACTERS,
)
from highway_fury.drawing.vehicles import draw_car_body


class Player:
    def __init__(self, difficulty="normal", character="rabbit"):
        preset = DIFFICULTY_PRESETS[difficulty]
        self.x = LANE_CENTERS[1]
        self.y = HEIGHT - 150
        self.speed = 0
        self.max_speed = 500
        self.nitro_max_speed = 700
        self.acceleration = 200
        self.brake_power = 300
        self.friction = 25
        self.steering_speed = 450
        self.color = (0, 100, 255)
        self.width, self.height = 50, 100
        self.invincible = 0.0
        self.hp = preset["hp"]
        self.max_hp = preset["hp"]
        self.nitro = 100.0
        self.max_nitro = 100.0
        self.nitro_active = False
        self.nitro_regen = 8
        self.nitro_drain = 40
        self.shield = 0.0
        self.score_mult = 1
        self.score_mult_timer = 0.0
        self.tilt = 0.0
        self.hurt_timer = 0.0
        self.character = character
        self.difficulty = difficulty

        if character == "rabbit":
            self.steering_speed = 540
        elif character == "croc":
            self.hp += 1
            self.max_hp += 1
        elif character == "tiger":
            self.nitro_max_speed = 780
            self.nitro_drain = 30

    def update(self, dt, keys):
        is_nitro = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.nitro > 0
        if is_nitro and self.speed > 50:
            self.nitro_active = True
            self.nitro = max(0, self.nitro - self.nitro_drain * dt)
            cur_max, accel = self.nitro_max_speed, self.acceleration * 2.0
        else:
            self.nitro_active = False
            cur_max, accel = self.max_speed, self.acceleration
            self.nitro = min(self.max_nitro, self.nitro + self.nitro_regen * dt)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + accel * dt, cur_max)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - self.brake_power * dt, -30)
        else:
            if self.speed > 0:
                self.speed = max(0, self.speed - self.friction * dt)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.friction * dt)

        steer = self.steering_speed * (1.3 if self.speed > 300 else 1.0)
        move = steer * dt
        target_tilt = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= move
            target_tilt = -0.15
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += move
            target_tilt = 0.15
        self.tilt += (target_tilt - self.tilt) * min(1, dt * 10)

        self.x = max(ROAD_LEFT + self.width // 2 + 10,
                     min(ROAD_RIGHT - self.width // 2 - 10, self.x))

        if self.invincible > 0:
            self.invincible -= dt
        if self.shield > 0:
            self.shield -= dt
        if self.hurt_timer > 0:
            self.hurt_timer -= dt
        if self.score_mult_timer > 0:
            self.score_mult_timer -= dt
            if self.score_mult_timer <= 0:
                self.score_mult = 1

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2 + 5,
            self.y - self.height // 2 + 5,
            self.width - 10,
            self.height - 10,
        )

    def draw(self, surface):
        if self.invincible > 0 and int(self.invincible * 12) % 2 == 0:
            return
        draw_car_body(surface, int(self.x), int(self.y), self.width, self.height, self.color, True)

        if self.shield > 0:
            r = int(max(self.width, self.height) * 0.7 * (1.0 + 0.1 * math.sin(pygame.time.get_ticks() * 0.01)))
            ss = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(ss, (0, 200, 255, 60), (r, r), r)
            pygame.draw.circle(ss, (0, 200, 255, 120), (r, r), r, 3)
            surface.blit(ss, (int(self.x) - r, int(self.y) - r))

        if self.nitro_active:
            for _ in range(4):
                fx = self.x + random.randint(-8, 8)
                fy = self.y + self.height // 2 + random.randint(0, 15)
                c = random.choice([(255, 100, 0), (255, 200, 0), (255, 60, 0), (255, 255, 100)])
                pygame.draw.circle(surface, c, (int(fx), int(fy)), random.randint(5, 14))
