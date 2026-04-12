"""Game over and pause overlay screens."""

import pygame

from highway_fury.config import WIDTH, HEIGHT, WHITE, RED, YELLOW, ORANGE, NEON_GREEN
from highway_fury.drawing.characters import FACE_DRAWERS


def draw_gameover(surface, game):
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 200))
    surface.blit(ov, (0, 0))

    wt = game.fonts["huge"].render("WASTED", True, RED)
    surface.blit(wt, (WIDTH // 2 - wt.get_width() // 2, 120))

    drawer = FACE_DRAWERS.get(game.selected_character)
    if drawer:
        drawer(surface, WIDTH // 2, 210, 40, hurt=True)

    if game.score >= game.high_score and game.score > 0:
        nt = game.fonts["medium"].render("NEW HIGH SCORE!", True, NEON_GREEN)
        surface.blit(nt, (WIDTH // 2 - nt.get_width() // 2, 260))

    stats = [
        (f"SCORE: {int(game.score)}", YELLOW),
        (f"DISTANCE: {game.distance:.1f} km", WHITE),
        (f"CARS PASSED: {game.passed_cars}", WHITE),
        (f"MAX COMBO: x{game.max_combo_reached}", ORANGE),
        (f"HIGH SCORE: {int(game.high_score)}", NEON_GREEN),
    ]
    for i, (text, color) in enumerate(stats):
        t = game.fonts["medium"].render(text, True, color)
        surface.blit(t, (WIDTH // 2 - t.get_width() // 2, 300 + i * 42))

    if int(pygame.time.get_ticks() / 500) % 2:
        surface.blit(game.fonts["medium"].render("[ SPACE ] RETRY", True, WHITE), (WIDTH // 2 - 100, 540))


def draw_pause(surface, game):
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 160))
    surface.blit(ov, (0, 0))

    surface.blit(game.fonts["large"].render("PAUSED", True, WHITE), (WIDTH // 2 - 80, 280))
    surface.blit(game.fonts["medium"].render("[ SPACE ] Resume  |  [ ESC ] Menu", True, YELLOW), (WIDTH // 2 - 220, 370))
