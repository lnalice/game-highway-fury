"""Drawing functions for road obstacles and background scenery."""

import pygame

from highway_fury.config import BLACK, ORANGE, WHITE, BROWN, DARK_GREEN, GREEN


def draw_barrier(surface, x, y, w, h):
    pygame.draw.rect(surface, (255, 140, 0), (x - w // 2, y - h // 2, w, h), border_radius=3)
    stripe_w = w // 5
    for i in range(0, w, stripe_w * 2):
        pygame.draw.rect(surface, BLACK, (x - w // 2 + i, y - h // 2, stripe_w, h))


def draw_cone(surface, x, y):
    pygame.draw.polygon(surface, ORANGE, [(x, y - 20), (x - 10, y + 10), (x + 10, y + 10)])
    pygame.draw.rect(surface, WHITE, (x - 12, y + 10, 24, 6))
    pygame.draw.rect(surface, WHITE, (x - 5, y - 8, 10, 4))


def draw_oil(surface, x, y, r):
    pygame.draw.ellipse(surface, (20, 20, 30), (x - r, y - r // 2, r * 2, r))
    pygame.draw.ellipse(surface, (40, 40, 55), (x - r + 5, y - r // 2 + 3, r, r // 2))


def draw_tree(surface, x, y, size=1.0):
    tw, th = int(12 * size), int(30 * size)
    pygame.draw.rect(surface, BROWN, (x - tw // 2, y - th, tw, th))
    r = int(25 * size)
    pygame.draw.circle(surface, DARK_GREEN, (x, y - th - r // 2), r)
    pygame.draw.circle(surface, GREEN, (x - int(8 * size), y - th - r // 2 - int(5 * size)), int(r * 0.7))


def draw_mountain(surface, x, y, w, h, color):
    pygame.draw.polygon(surface, color, [(x, y), (x + w // 2, y - h), (x + w, y)])
    pygame.draw.polygon(surface, (240, 240, 255), [
        (x + w // 2, y - h),
        (x + w // 2 - w // 8, y - h + h // 5),
        (x + w // 2 + w // 8, y - h + h // 5),
    ])
