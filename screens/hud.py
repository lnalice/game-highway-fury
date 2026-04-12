"""In-game HUD: speed, HP bar, score, and character portrait."""

import pygame

from highway_fury.config import (
    WIDTH, HEIGHT, WHITE, DARK_GRAY, LIGHT_GRAY, RED, YELLOW, GREEN,
    ORANGE, CYAN, MAGENTA, NEON_GREEN, NEON_PINK, CHARACTERS, CHARACTER_KEYS,
)
from highway_fury.drawing.characters import FACE_DRAWERS


def draw_character_portrait(surface, game):
    px, py = 60, HEIGHT - 70
    bg = pygame.Surface((100, 100), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 140))
    surface.blit(bg, (px - 50, py - 50))
    drawer = FACE_DRAWERS.get(game.selected_character)
    if drawer:
        drawer(surface, px, py, 38, hurt=game.player.hurt_timer > 0)
    name = CHARACTERS[game.selected_character]["name"]
    nf = game.fonts["tiny"].render(name, True, WHITE)
    surface.blit(nf, (px - nf.get_width() // 2, py + 42))


def draw_hud(surface, game):
    player = game.player
    speed_kmh = int(player.speed)

    panel = pygame.Surface((220, 210), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 160))
    surface.blit(panel, (10, 10))

    sc = NEON_PINK if speed_kmh >= 500 else RED if speed_kmh >= 300 else YELLOW if speed_kmh >= 200 else WHITE
    st = game.fonts["large"].render(f"{speed_kmh}", True, sc)
    ut = game.fonts["tiny"].render("km/h", True, LIGHT_GRAY)
    surface.blit(st, (20, 15))
    surface.blit(ut, (20 + st.get_width() + 5, 40))

    bx, by, bw, bh = 20, 80, 195, 12
    pygame.draw.rect(surface, DARK_GRAY, (bx, by, bw, bh), border_radius=6)
    fw = int(bw * min(1, player.speed / player.nitro_max_speed))
    bc = GREEN if speed_kmh < 200 else YELLOW if speed_kmh < 400 else RED if speed_kmh < 600 else MAGENTA
    pygame.draw.rect(surface, bc, (bx, by, fw, bh), border_radius=6)

    ny = by + 18
    pygame.draw.rect(surface, DARK_GRAY, (bx, ny, bw, 8), border_radius=4)
    nf = int(bw * (player.nitro / player.max_nitro))
    nc = ORANGE if player.nitro_active else (200, 120, 0)
    pygame.draw.rect(surface, nc, (bx, ny, nf, 8), border_radius=4)
    nt = game.fonts["tiny"].render("NITRO [SHIFT]", True, ORANGE)
    surface.blit(nt, (bx + bw - nt.get_width(), ny + 10))

    hy = ny + 30
    for i in range(player.max_hp):
        hx = bx + i * 22
        c = RED if i < player.hp else (60, 20, 20)
        pygame.draw.rect(surface, c, (hx, hy, 18, 14), border_radius=4)
        if i < player.hp:
            pygame.draw.rect(surface, (255, 100, 100), (hx + 2, hy + 2, 14, 5), border_radius=3)

    surface.blit(game.fonts["small"].render(f"SCORE: {int(game.score)}", True, WHITE), (20, hy + 22))
    surface.blit(game.fonts["small"].render(f"DIST: {game.distance:.1f} km", True, WHITE), (20, hy + 42))
    surface.blit(game.fonts["small"].render(f"PASS: {game.passed_cars}", True, WHITE), (20, hy + 62))

    yy = hy + 82
    if player.shield > 0:
        surface.blit(game.fonts["tiny"].render(f"SHIELD: {player.shield:.0f}s", True, CYAN), (20, yy))
        yy += 18
    if player.score_mult > 1:
        surface.blit(game.fonts["tiny"].render(f"SCORE x{player.score_mult}: {player.score_mult_timer:.0f}s", True, NEON_GREEN), (20, yy))

    if game.combo > 1:
        cf = pygame.font.Font(None, int(48 * min(1.5, 1.0 + game.combo * 0.05)))
        ct = cf.render(f"COMBO x{game.combo}!", True, NEON_GREEN if game.combo >= 5 else ORANGE)
        surface.blit(ct, (WIDTH // 2 - ct.get_width() // 2, 80))

    if game.zone_timer > 0:
        zf = pygame.font.Font(None, 70)
        zt = zf.render(game.zone_text, True, NEON_PINK)
        zt.set_alpha(int(min(1.0, game.zone_timer) * 255))
        surface.blit(zt, (WIDTH // 2 - zt.get_width() // 2, 30))

    draw_character_portrait(surface, game)
