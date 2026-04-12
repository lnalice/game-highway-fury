"""Character face drawing functions (normal + hurt expressions)."""

import math
import pygame

from highway_fury.config import WHITE


def draw_face_rabbit(surface, cx, cy, r, hurt=False):
    pygame.draw.circle(surface, (240, 230, 230), (cx, cy), r)
    pygame.draw.circle(surface, (220, 210, 210), (cx, cy), r, 2)
    ear_w, ear_h = int(r * 0.3), int(r * 0.9)
    for side in [-1, 1]:
        ex = cx + side * int(r * 0.35)
        ey = cy - r - int(ear_h * 0.5)
        pygame.draw.ellipse(surface, (240, 230, 230), (ex - ear_w // 2, ey, ear_w, ear_h))
        pygame.draw.ellipse(surface, (255, 180, 190), (ex - ear_w // 4, ey + ear_h // 6, ear_w // 2, int(ear_h * 0.6)))
    eye_y = cy - int(r * 0.15)
    if hurt:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.3)
            pygame.draw.line(surface, (60, 60, 60), (ex - 5, eye_y - 4), (ex + 5, eye_y + 4), 2)
            pygame.draw.line(surface, (60, 60, 60), (ex - 5, eye_y + 4), (ex + 5, eye_y - 4), 2)
        pygame.draw.ellipse(surface, (60, 60, 60), (cx - 5, cy + int(r * 0.25), 10, 12))
    else:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.3)
            pygame.draw.circle(surface, (60, 20, 20), (ex, eye_y), int(r * 0.14))
            pygame.draw.circle(surface, WHITE, (ex + 2, eye_y - 2), int(r * 0.05))
        pygame.draw.ellipse(surface, (255, 150, 170), (cx - int(r * 0.12), cy + int(r * 0.2), int(r * 0.24), int(r * 0.15)))
    pygame.draw.circle(surface, (255, 180, 190), (cx - int(r * 0.45), cy + int(r * 0.1)), int(r * 0.12))
    pygame.draw.circle(surface, (255, 180, 190), (cx + int(r * 0.45), cy + int(r * 0.1)), int(r * 0.12))


def draw_face_croc(surface, cx, cy, r, hurt=False):
    pygame.draw.ellipse(surface, (80, 160, 80), (cx - r, cy - int(r * 0.8), r * 2, int(r * 1.8)))
    snout_y = cy + int(r * 0.15)
    pygame.draw.ellipse(surface, (90, 175, 90), (cx - int(r * 0.7), snout_y, int(r * 1.4), int(r * 0.6)))
    eye_y = cy - int(r * 0.25)
    if hurt:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.35)
            pygame.draw.line(surface, (30, 30, 30), (ex - 6, eye_y - 4), (ex + 6, eye_y + 4), 3)
            pygame.draw.line(surface, (30, 30, 30), (ex - 6, eye_y + 4), (ex + 6, eye_y - 4), 3)
    else:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.35)
            pygame.draw.ellipse(surface, (240, 240, 100), (ex - int(r * 0.14), eye_y - int(r * 0.16), int(r * 0.28), int(r * 0.32)))
            pygame.draw.ellipse(surface, (20, 20, 20), (ex - int(r * 0.06), eye_y - int(r * 0.12), int(r * 0.12), int(r * 0.28)))
    mouth_y = cy + int(r * 0.35)
    if hurt:
        pygame.draw.arc(surface, (30, 60, 30), (cx - int(r * 0.4), mouth_y - 4, int(r * 0.8), 12), 0, math.pi, 2)
    else:
        pygame.draw.line(surface, (30, 60, 30), (cx - int(r * 0.5), mouth_y), (cx + int(r * 0.5), mouth_y), 2)
        for i in range(5):
            tx = cx - int(r * 0.4) + i * int(r * 0.2)
            pygame.draw.polygon(surface, WHITE, [(tx, mouth_y), (tx + 4, mouth_y + 6), (tx + 8, mouth_y)])
    for side in [-1, 1]:
        pygame.draw.circle(surface, (50, 120, 50), (cx + side * int(r * 0.15), snout_y + int(r * 0.05)), 3)


def draw_face_tiger(surface, cx, cy, r, hurt=False):
    pygame.draw.circle(surface, (240, 180, 50), (cx, cy), r)
    for side in [-1, 1]:
        ex = cx + side * int(r * 0.5)
        ey = cy - int(r * 0.7)
        pygame.draw.polygon(surface, (240, 180, 50), [(ex - int(r * 0.25), ey + int(r * 0.35)), (ex, ey - int(r * 0.2)), (ex + int(r * 0.25), ey + int(r * 0.35))])
        pygame.draw.polygon(surface, (255, 200, 150), [(ex - int(r * 0.15), ey + int(r * 0.3)), (ex, ey), (ex + int(r * 0.15), ey + int(r * 0.3))])
    stripe = (60, 40, 20)
    for i, dy in enumerate([-0.4, -0.15, 0.1]):
        sw = int(r * (0.3 + i * 0.05))
        sy = cy + int(r * dy)
        for side in [-1, 1]:
            pygame.draw.line(surface, stripe, (cx + side * int(r * 0.5), sy - 3), (cx + side * int(r * 0.5) - side * sw, sy + 2), 2)
    eye_y = cy - int(r * 0.15)
    if hurt:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.28)
            pygame.draw.line(surface, stripe, (ex - 6, eye_y - 5), (ex + 6, eye_y + 5), 3)
            pygame.draw.line(surface, stripe, (ex - 6, eye_y + 5), (ex + 6, eye_y - 5), 3)
        pygame.draw.ellipse(surface, stripe, (cx - 6, cy + int(r * 0.3), 12, 10))
    else:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.28)
            pygame.draw.circle(surface, (30, 30, 30), (ex, eye_y), int(r * 0.13))
            pygame.draw.circle(surface, (200, 180, 50), (ex, eye_y), int(r * 0.13), 2)
            pygame.draw.circle(surface, WHITE, (ex + 2, eye_y - 2), int(r * 0.04))
    nose_y = cy + int(r * 0.15)
    pygame.draw.ellipse(surface, (200, 120, 80), (cx - 6, nose_y, 12, 8))
    if not hurt:
        pygame.draw.line(surface, stripe, (cx, nose_y + 8), (cx, cy + int(r * 0.35)), 2)
        pygame.draw.arc(surface, stripe, (cx - 10, cy + int(r * 0.25), 20, 12), math.pi, 2 * math.pi, 2)
    for side in [-1, 1]:
        for wy in range(-2, 4, 3):
            pygame.draw.line(surface, stripe, (cx + side * int(r * 0.4), nose_y + wy), (cx + side * int(r * 0.4) + side * int(r * 0.3), nose_y + wy - 1), 1)


def draw_face_lion(surface, cx, cy, r, hurt=False):
    mane_r = int(r * 1.35)
    for angle in range(0, 360, 15):
        mx = cx + int(math.cos(math.radians(angle)) * mane_r * 0.9)
        my = cy + int(math.sin(math.radians(angle)) * mane_r * 0.85)
        pygame.draw.circle(surface, (180, 120, 30), (mx, my), int(r * 0.3))
    pygame.draw.circle(surface, (220, 170, 60), (cx, cy), r)
    eye_y = cy - int(r * 0.2)
    lc = (80, 50, 20)
    if hurt:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.28)
            pygame.draw.line(surface, lc, (ex - 6, eye_y - 4), (ex + 6, eye_y + 4), 3)
            pygame.draw.line(surface, lc, (ex - 6, eye_y + 4), (ex + 6, eye_y - 4), 3)
        pygame.draw.arc(surface, lc, (cx - 8, cy + int(r * 0.25), 16, 12), 0, math.pi, 2)
    else:
        for side in [-1, 1]:
            ex = cx + side * int(r * 0.28)
            pygame.draw.circle(surface, lc, (ex, eye_y), int(r * 0.12))
            pygame.draw.circle(surface, WHITE, (ex + 2, eye_y - 2), int(r * 0.04))
        pygame.draw.arc(surface, lc, (cx - 10, cy + int(r * 0.22), 20, 12), math.pi, 2 * math.pi, 2)
    pygame.draw.ellipse(surface, (180, 120, 70), (cx - 7, cy + int(r * 0.08), 14, 10))
    pygame.draw.line(surface, lc, (cx, cy + int(r * 0.18)), (cx, cy + int(r * 0.3)), 2)
    for side in [-1, 1]:
        for wy in range(-1, 4, 3):
            ny = cy + int(r * 0.15) + wy
            pygame.draw.line(surface, lc, (cx + side * int(r * 0.35), ny), (cx + side * int(r * 0.35) + side * int(r * 0.25), ny), 1)


FACE_DRAWERS = {
    "rabbit": draw_face_rabbit,
    "croc":   draw_face_croc,
    "tiger":  draw_face_tiger,
    "lion":   draw_face_lion,
}
