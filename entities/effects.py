"""Visual effect entities: particles, speed lines, floating text."""

import random
import pygame

from highway_fury.config import WHITE, ROAD_LEFT, ROAD_RIGHT


class Particle:
    __slots__ = ['x', 'y', 'vx', 'vy', 'life', 'max_life', 'color', 'size', 'gravity']

    def __init__(self, x, y, color, vx=None, vy=None, life=None, size=None, gravity=200):
        self.x, self.y = x, y
        self.vx = vx if vx is not None else random.uniform(-120, 120)
        self.vy = vy if vy is not None else random.uniform(-200, 50)
        self.life = life if life is not None else random.uniform(0.3, 1.2)
        self.max_life = self.life
        self.color = color
        self.size = size if size is not None else random.randint(2, 7)
        self.gravity = gravity

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.life -= dt

    def draw(self, surface):
        if self.life > 0:
            s = max(1, int(self.size * (self.life / self.max_life)))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), s)


class SpeedLine:
    __slots__ = ['x', 'y', 'length', 'speed']

    def __init__(self):
        self.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 10)
        self.y = random.randint(-50, 0)
        self.length = random.randint(20, 60)
        self.speed = random.uniform(1500, 2500)

    def update(self, dt):
        self.y += self.speed * dt

    def draw(self, surface, _alpha=1.0):
        pygame.draw.line(surface, WHITE,
                         (int(self.x), int(self.y)),
                         (int(self.x), int(self.y + self.length)), 2)


class FloatingText:
    __slots__ = ['x', 'y', 'text', 'color', 'life', 'max_life', 'font']

    def __init__(self, x, y, text, color, life=1.5):
        self.x, self.y = x, y
        self.text, self.color = text, color
        self.life = self.max_life = life
        self.font = pygame.font.Font(None, 38)

    def update(self, dt):
        self.y -= 60 * dt
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return
        t = self.font.render(self.text, True, self.color)
        t.set_alpha(int((self.life / self.max_life) * 255))
        surface.blit(t, (int(self.x) - t.get_width() // 2, int(self.y)))
