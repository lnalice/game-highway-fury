"""Obstacle entity with lane-changing AI and player tracking."""

import math
import random
import pygame

from highway_fury.config import (
    HEIGHT, YELLOW, WHITE, LANE_COUNT, LANE_CENTERS, LANE_WIDTH,
    ROAD_LEFT, ROAD_RIGHT, ENEMY_COLORS,
    OBS_CAR, OBS_TRUCK, OBS_MOTORCYCLE, OBS_BARRIER, OBS_CONE,
    OBS_OIL, OBS_BROKEN, OBS_POLICE,
)
from highway_fury.drawing import (
    draw_car_body, draw_truck, draw_motorcycle,
    draw_barrier, draw_cone, draw_oil,
)


class Obstacle:
    def __init__(self, obs_type, lane, y_pos, speed=0, x_override=None):
        self.type = obs_type
        self.lane = lane
        self.base_x = LANE_CENTERS[lane] if x_override is None else x_override
        self.x = self.base_x
        self.y = y_pos
        self.speed = speed
        self.color = random.choice(ENEMY_COLORS)
        self.sway = random.uniform(-0.5, 0.5)
        self.sway_timer = random.uniform(0, math.pi * 2)
        self.passed = False
        self.flash_timer = 0
        self.lane_change_timer = random.uniform(1.5, 4.0)
        self.lane_change_speed = random.uniform(80, 180)
        self.target_x = self.base_x
        self.tracks_player = False
        self.track_speed = 0

        if obs_type == OBS_CAR:
            self.width, self.height = 50, 100
            if random.random() >= 0.35:
                self.lane_change_timer = 999
        elif obs_type == OBS_TRUCK:
            self.width, self.height = 62, 150
            self.speed *= 0.6
            self.color = random.choice([(180, 40, 40), (40, 80, 160), (200, 200, 200), (80, 80, 80), (0, 100, 0)])
            self.lane_change_timer = 999
        elif obs_type == OBS_MOTORCYCLE:
            self.width, self.height = 28, 60
            self.speed *= 1.5
            self.color = random.choice([(200, 30, 30), (30, 30, 30), (255, 200, 0), (0, 150, 255)])
            self.lane_change_speed = random.uniform(150, 300)
            self.lane_change_timer = random.uniform(0.8, 2.0)
        elif obs_type == OBS_BARRIER:
            self.width, self.height = 80, 30; self.speed = 0; self.lane_change_timer = 999
        elif obs_type == OBS_CONE:
            self.width, self.height = 24, 30; self.speed = 0; self.lane_change_timer = 999
        elif obs_type == OBS_OIL:
            self.width, self.height = 60, 30; self.speed = 0; self.lane_change_timer = 999
        elif obs_type == OBS_BROKEN:
            self.width, self.height = 50, 100; self.speed = 0
            self.flash_timer = random.uniform(0, 3)
            self.color = random.choice([(150, 150, 150), (120, 100, 80)])
            self.lane_change_timer = 999
        elif obs_type == OBS_POLICE:
            self.width, self.height = 52, 105
            self.color = (30, 30, 30); self.flash_timer = 0
            self.tracks_player = True
            self.track_speed = random.uniform(120, 220)
            self.lane_change_timer = 999

    def update(self, dt, player_speed, player_x=None):
        self.y += (player_speed - self.speed) * dt * 3.5

        if self.tracks_player and player_x is not None and -50 < self.y < HEIGHT + 50:
            diff = player_x - self.x
            if abs(diff) > 5:
                self.x += self.track_speed * dt * (1 if diff > 0 else -1)
        elif self.lane_change_timer < 999:
            self.lane_change_timer -= dt
            if self.lane_change_timer <= 0:
                new_lane = random.choice([i for i in range(LANE_COUNT) if i != self.lane])
                self.lane = new_lane
                self.target_x = LANE_CENTERS[new_lane] + random.uniform(-15, 15)
                self.lane_change_timer = random.uniform(1.5, 4.0)
            diff = self.target_x - self.x
            if abs(diff) > 3:
                self.x += self.lane_change_speed * dt * (1 if diff > 0 else -1)
            else:
                self.x = self.target_x
        else:
            if self.type in (OBS_CAR, OBS_MOTORCYCLE):
                self.sway_timer += dt
                self.x = self.base_x + math.sin(self.sway_timer * self.sway) * 8

        self.x = max(ROAD_LEFT + self.width // 2, min(ROAD_RIGHT - self.width // 2, self.x))

        if self.type == OBS_POLICE:
            self.flash_timer += dt * 8
        elif self.type == OBS_BROKEN:
            self.flash_timer += dt

    def get_rect(self):
        s = 8 if self.type != OBS_OIL else 0
        return pygame.Rect(
            self.x - self.width // 2 + s,
            self.y - self.height // 2 + s,
            self.width - s * 2,
            self.height - s * 2,
        )

    def draw(self, surface):
        ix, iy = int(self.x), int(self.y)
        if self.type == OBS_CAR:
            draw_car_body(surface, ix, iy, self.width, self.height, self.color)
        elif self.type == OBS_TRUCK:
            draw_truck(surface, ix, iy, self.width, self.height, self.color)
        elif self.type == OBS_MOTORCYCLE:
            draw_motorcycle(surface, ix, iy, self.width, self.height, self.color)
        elif self.type == OBS_BARRIER:
            draw_barrier(surface, ix, iy, self.width, self.height)
        elif self.type == OBS_CONE:
            draw_cone(surface, ix, iy)
        elif self.type == OBS_OIL:
            draw_oil(surface, ix, iy, self.width // 2)
        elif self.type == OBS_BROKEN:
            draw_car_body(surface, ix, iy, self.width, self.height, self.color)
            if int(self.flash_timer * 2) % 2:
                pygame.draw.polygon(surface, YELLOW, [
                    (ix - 8, iy - self.height // 2 - 15),
                    (ix + 8, iy - self.height // 2 - 15),
                    (ix + 3, iy - self.height // 2 - 5),
                    (ix - 3, iy - self.height // 2 - 5),
                ])
        elif self.type == OBS_POLICE:
            draw_car_body(surface, ix, iy, self.width, self.height, self.color)
            fp = int(self.flash_timer) % 2
            pygame.draw.circle(surface, (255, 50, 50) if fp else (50, 100, 255), (ix - 12, iy - self.height // 2 + 5), 6)
            pygame.draw.circle(surface, (50, 100, 255) if fp else (255, 50, 50), (ix + 12, iy - self.height // 2 + 5), 6)
            pygame.draw.rect(surface, WHITE, (ix - 18, iy + 10, 36, 12), border_radius=2)
