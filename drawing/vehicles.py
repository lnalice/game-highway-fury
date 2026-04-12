"""Drawing functions for player car, enemy cars, trucks, and motorcycles."""

import pygame


def draw_car_body(surface, x, y, w, h, color, is_player=False):
    pygame.draw.rect(surface, color, (x - w // 2, y - h // 2, w, h), border_radius=8)
    darker = tuple(max(0, c - 50) for c in color)
    roof_w, roof_h = int(w * 0.7), int(h * 0.3)
    roof_y = y - h // 2 + (int(h * 0.25) if is_player else int(h * 0.35))
    pygame.draw.rect(surface, darker, (x - roof_w // 2, roof_y, roof_w, roof_h), border_radius=5)

    ws = (180, 220, 255)
    ws_w, ws_h = int(w * 0.65), int(h * 0.12)
    ws_x = x - ws_w // 2
    front_ws = y - h // 2 + int(h * 0.22)
    rear_ws  = y - h // 2 + int(h * 0.55)
    if is_player:
        pygame.draw.rect(surface, ws, (ws_x, front_ws, ws_w, ws_h), border_radius=3)
        pygame.draw.rect(surface, ws, (ws_x, rear_ws, ws_w, ws_h), border_radius=3)
    else:
        pygame.draw.rect(surface, ws, (ws_x, rear_ws, ws_w, ws_h), border_radius=3)
        pygame.draw.rect(surface, ws, (ws_x, front_ws, ws_w, ws_h), border_radius=3)

    if is_player:
        pygame.draw.rect(surface, (255, 255, 200), (x - w // 2 + 5, y - h // 2 + 2, 10, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 255, 200), (x + w // 2 - 15, y - h // 2 + 2, 10, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 50, 50), (x - w // 2 + 5, y + h // 2 - 8, 8, 5), border_radius=2)
        pygame.draw.rect(surface, (255, 50, 50), (x + w // 2 - 13, y + h // 2 - 8, 8, 5), border_radius=2)
    else:
        pygame.draw.rect(surface, (255, 50, 50), (x - w // 2 + 5, y + h // 2 - 8, 10, 6), border_radius=2)
        pygame.draw.rect(surface, (255, 50, 50), (x + w // 2 - 15, y + h // 2 - 8, 10, 6), border_radius=2)

    wc = (30, 30, 30)
    for dy in [-h // 4, h // 4 - 10]:
        pygame.draw.rect(surface, wc, (x - w // 2 - 3, y + dy, 8, 18), border_radius=3)
        pygame.draw.rect(surface, wc, (x + w // 2 - 5, y + dy, 8, 18), border_radius=3)


def draw_truck(surface, x, y, w, h, color):
    pygame.draw.rect(surface, color, (x - w // 2, y - h // 2, w, h), border_radius=4)
    darker = tuple(max(0, c - 60) for c in color)
    cab_h = int(h * 0.25)
    pygame.draw.rect(surface, darker, (x - w // 2 + 3, y + h // 2 - cab_h, w - 6, cab_h), border_radius=3)
    pygame.draw.rect(surface, (180, 220, 255), (x - int(w * 0.3), y + h // 2 - cab_h + 4, int(w * 0.6), int(cab_h * 0.5)), border_radius=2)
    for i in range(3):
        pygame.draw.rect(surface, darker, (x - w // 2 + 4, y - h // 2 + 10 + i * int(h * 0.2), w - 8, 3))
    pygame.draw.rect(surface, (255, 50, 50), (x - w // 2 + 4, y - h // 2 + 2, 12, 8), border_radius=2)
    pygame.draw.rect(surface, (255, 50, 50), (x + w // 2 - 16, y - h // 2 + 2, 12, 8), border_radius=2)
    wc = (25, 25, 25)
    for dy in [-h // 4, h // 4 - 10]:
        pygame.draw.rect(surface, wc, (x - w // 2 - 4, y + dy, 9, 22), border_radius=3)
        pygame.draw.rect(surface, wc, (x + w // 2 - 5, y + dy, 9, 22), border_radius=3)


def draw_motorcycle(surface, x, y, w, h, color):
    pygame.draw.ellipse(surface, color, (x - w // 2, y - h // 2, w, h))
    rider = tuple(max(0, c - 80) for c in color)
    pygame.draw.ellipse(surface, rider, (x - w // 3, y - h // 4, int(w * 0.66), int(h * 0.5)))
    pygame.draw.circle(surface, (60, 60, 60), (x, y - h // 3), int(w * 0.3))
    pygame.draw.circle(surface, (40, 40, 40), (x, y + h // 2 - 2), 6)
    pygame.draw.circle(surface, (40, 40, 40), (x, y - h // 2 + 6), 5)
    pygame.draw.rect(surface, (255, 255, 150), (x - 3, y - h // 2, 6, 4), border_radius=1)
    pygame.draw.rect(surface, (255, 30, 30), (x - 2, y + h // 2 - 4, 4, 4), border_radius=1)
