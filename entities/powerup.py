"""Collectible power-up entity."""

import math
import pygame

from highway_fury.config import (
    WHITE, ORANGE, CYAN, NEON_GREEN, LANE_CENTERS,
    POWERUP_NITRO, POWERUP_SHIELD,
)


class PowerUp:
    def __init__(self, ptype, lane, y_pos):
        self.type, self.lane = ptype, lane
        self.x, self.y = LANE_CENTERS[lane], y_pos
        self.size, self.timer = 20, 0.0
        if ptype == POWERUP_NITRO:
            self.color, self.symbol = ORANGE, "N"
        elif ptype == POWERUP_SHIELD:
            self.color, self.symbol = CYAN, "S"
        else:
            self.color, self.symbol = NEON_GREEN, "x2"

    def update(self, dt, player_speed):
        self.y += player_speed * dt * 3.5
        self.timer += dt

    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

    def draw(self, surface):
        r = int(self.size * (1.0 + 0.2 * math.sin(self.timer * 5)))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), r, 2)
        f = pygame.font.Font(None, 28)
        t = f.render(self.symbol, True, WHITE)
        surface.blit(t, (int(self.x) - t.get_width() // 2, int(self.y) - t.get_height() // 2))
