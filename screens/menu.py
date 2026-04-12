"""Main menu, difficulty select, character select, and guide screens."""

import math
import pygame

from highway_fury.config import (
    WIDTH, HEIGHT, WHITE, GRAY, DARK_GRAY, LIGHT_GRAY, YELLOW, ORANGE,
    RED, CYAN, NEON_GREEN, NEON_PINK,
    DIFFICULTY_PRESETS, CHARACTERS, DIFFICULTY_KEYS, CHARACTER_KEYS, MENU_BUTTONS,
)
from highway_fury.drawing.characters import FACE_DRAWERS


def _draw_bg_overlay(surface, game):
    game.draw_background(surface)
    game.draw_road(surface)
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 140))
    surface.blit(ov, (0, 0))


def draw_menu(surface, game):
    _draw_bg_overlay(surface, game)
    pulse = 1.0 + 0.05 * math.sin(game.menu_time * 3)
    tf = pygame.font.Font(None, int(90 * pulse))
    title = tf.render("HIGHWAY FURY", True, NEON_PINK)
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))
    sub = game.fonts["medium"].render("- Extreme Racing -", True, YELLOW)
    surface.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 210))
    if game.high_score > 0:
        hs = game.fonts["small"].render(f"HIGH SCORE: {int(game.high_score)}", True, ORANGE)
        surface.blit(hs, (WIDTH // 2 - hs.get_width() // 2, 260))

    btn_y_start = 310
    btn_w, btn_h = 320, 60
    btn_colors = [NEON_GREEN, CYAN, ORANGE]
    for i, label in enumerate(MENU_BUTTONS):
        bx = WIDTH // 2 - btn_w // 2
        by = btn_y_start + i * 80
        selected = i == game.menu_index
        if selected:
            glow = pygame.Surface((btn_w + 8, btn_h + 8), pygame.SRCALPHA)
            glow.fill((*btn_colors[i], 50))
            surface.blit(glow, (bx - 4, by - 4))
            pygame.draw.rect(surface, btn_colors[i], (bx, by, btn_w, btn_h), border_radius=12)
            pygame.draw.rect(surface, WHITE, (bx, by, btn_w, btn_h), 3, border_radius=12)
            lt = game.fonts["medium"].render(f"> {label} <", True, WHITE)
        else:
            pygame.draw.rect(surface, (40, 40, 50), (bx, by, btn_w, btn_h), border_radius=12)
            pygame.draw.rect(surface, GRAY, (bx, by, btn_w, btn_h), 2, border_radius=12)
            lt = game.fonts["medium"].render(label, True, GRAY)
        surface.blit(lt, (bx + btn_w // 2 - lt.get_width() // 2, by + btn_h // 2 - lt.get_height() // 2))

    info_y = btn_y_start + 3 * 80 + 10
    cur_char = CHARACTERS[CHARACTER_KEYS[game.char_index]]
    cur_diff = DIFFICULTY_PRESETS[DIFFICULTY_KEYS[game.diff_index]]
    FACE_DRAWERS[CHARACTER_KEYS[game.char_index]](surface, WIDTH // 2 - 120, info_y + 28, 22)
    surface.blit(game.fonts["small"].render(f"{cur_char['name']}  |  {cur_diff['label']}", True, LIGHT_GRAY),
                 (WIDTH // 2 - 90, info_y + 18))
    surface.blit(game.fonts["tiny"].render("UP/DOWN: Select  |  ENTER/SPACE: Confirm", True, DARK_GRAY),
                 (WIDTH // 2 - 175, info_y + 55))


def draw_difficulty_select(surface, game):
    _draw_bg_overlay(surface, game)
    t = game.fonts["large"].render("DIFFICULTY", True, WHITE)
    surface.blit(t, (WIDTH // 2 - t.get_width() // 2, 60))
    surface.blit(game.fonts["small"].render("< LEFT/RIGHT >  ENTER: Start  |  ESC: Back", True, LIGHT_GRAY),
                 (WIDTH // 2 - 210, 130))
    bw = 260
    gap = 15
    start_x = (WIDTH - bw * 3 - gap * 2) // 2
    for i, key in enumerate(DIFFICULTY_KEYS):
        p = DIFFICULTY_PRESETS[key]
        bx = start_x + i * (bw + gap)
        by, bh = 180, 320
        selected = i == game.diff_index
        if selected:
            glow = pygame.Surface((bw + 10, bh + 10), pygame.SRCALPHA)
            glow.fill((*p["color"], 40))
            surface.blit(glow, (bx - 5, by - 5))
            pygame.draw.rect(surface, p["color"], (bx, by, bw, bh), 0, border_radius=12)
            pygame.draw.rect(surface, WHITE, (bx, by, bw, bh), 3, border_radius=12)
        else:
            pygame.draw.rect(surface, DARK_GRAY, (bx, by, bw, bh), 2, border_radius=12)
        cx = bx + bw // 2
        label = game.fonts["large"].render(p["label"], True, WHITE if selected else GRAY)
        surface.blit(label, (cx - label.get_width() // 2, by + 25))
        for j, line in enumerate([f"HP: {p['hp']}", f"Speed: x{p['speed_mult']}", f"Spawn: x{p['spawn_mult']}"]):
            lt = game.fonts["small"].render(line, True, WHITE if selected else GRAY)
            surface.blit(lt, (cx - lt.get_width() // 2, by + 110 + j * 35))
        for j, part in enumerate(p["desc"].split(" | ")):
            dt = game.fonts["tiny"].render(part, True, WHITE if selected else DARK_GRAY)
            surface.blit(dt, (cx - dt.get_width() // 2, by + bh - 75 + j * 22))


def draw_character_select(surface, game):
    _draw_bg_overlay(surface, game)
    t = game.fonts["large"].render("CHARACTER", True, WHITE)
    surface.blit(t, (WIDTH // 2 - t.get_width() // 2, 40))
    surface.blit(game.fonts["small"].render("< LEFT/RIGHT >  ENTER: Select  |  ESC: Back", True, LIGHT_GRAY),
                 (WIDTH // 2 - 215, 100))
    for i, key in enumerate(CHARACTER_KEYS):
        ch = CHARACTERS[key]
        bx = 35 + i * 218
        by, bw, bh = 150, 200, 360
        selected = i == game.char_index
        bc = ch["color"] if selected else DARK_GRAY
        if selected:
            pygame.draw.rect(surface, bc, (bx, by, bw, bh), 0, border_radius=12)
            pygame.draw.rect(surface, WHITE, (bx, by, bw, bh), 3, border_radius=12)
        else:
            pygame.draw.rect(surface, bc, (bx, by, bw, bh), 2, border_radius=12)
        face_cx, face_cy = bx + bw // 2, by + 100
        FACE_DRAWERS[key](surface, face_cx, face_cy, 55 if selected else 40)
        nt = game.fonts["medium"].render(ch["name"], True, WHITE if selected else GRAY)
        surface.blit(nt, (face_cx - nt.get_width() // 2, by + 170))
        if selected:
            for j, dl in enumerate(ch["desc"].split("!")):
                dl = dl.strip()
                if not dl:
                    continue
                dt = game.fonts["small"].render(dl + ("!" if j < len(ch["desc"].split("!")) - 1 else ""), True, YELLOW)
                surface.blit(dt, (face_cx - dt.get_width() // 2, by + 220 + j * 30))
            pygame.draw.rect(surface, ch["color"], (bx + 20, by + bh - 60, bw - 40, 40), border_radius=8)
            st = game.fonts["small"].render("SELECTED", True, WHITE)
            surface.blit(st, (face_cx - st.get_width() // 2, by + bh - 52))


def draw_guide(surface, game):
    _draw_bg_overlay(surface, game)
    t = game.fonts["large"].render("HOW TO PLAY", True, WHITE)
    surface.blit(t, (WIDTH // 2 - t.get_width() // 2, 15))

    lx, rx = 40, WIDTH // 2 + 20
    ft, fs = game.fonts["tiny"], game.fonts["small"]
    fm = game.fonts["medium"]

    # Left column: Controls
    sy = 70
    surface.blit(fm.render("CONTROLS", True, WHITE), (lx, sy))
    sy += 38
    for key, desc in [("UP / W", "Accelerate"), ("DOWN / S", "Brake / Reverse"),
                      ("LEFT / RIGHT", "Steer (A / D)"), ("SHIFT", "Nitro Boost!"),
                      ("SPACE", "Honk"), ("ESC", "Pause")]:
        pygame.draw.rect(surface, (50, 50, 70), (lx, sy, 130, 24), border_radius=5)
        kt = ft.render(key, True, YELLOW)
        surface.blit(kt, (lx + 65 - kt.get_width() // 2, sy + 3))
        surface.blit(ft.render(desc, True, LIGHT_GRAY), (lx + 142, sy + 3))
        sy += 30

    # Left column: Power-ups
    sy += 12
    surface.blit(fm.render("POWER-UPS", True, YELLOW), (lx, sy))
    sy += 38
    from highway_fury.config import ORANGE as _O, CYAN as _C, NEON_GREEN as _N
    for color, symbol, name, desc in [(_O, "N", "NITRO", "Nitro gauge +50"),
                                       (_C, "S", "SHIELD", "8s barrier"),
                                       (_N, "x2", "SCORE x2", "10s double pts")]:
        pygame.draw.circle(surface, color, (lx + 16, sy + 13), 14)
        pygame.draw.circle(surface, WHITE, (lx + 16, sy + 13), 14, 2)
        st = pygame.font.Font(None, 22).render(symbol, True, WHITE)
        surface.blit(st, (lx + 16 - st.get_width() // 2, sy + 13 - st.get_height() // 2))
        surface.blit(fs.render(name, True, color), (lx + 40, sy))
        surface.blit(ft.render(desc, True, LIGHT_GRAY), (lx + 40, sy + 24))
        sy += 48

    # Right column: Hazards
    sy = 70
    surface.blit(fm.render("HAZARDS", True, RED), (rx, sy))
    sy += 38
    for color, name, desc in [((220, 50, 50), "Car / Motorcycle", "1 damage on hit"),
                               ((40, 80, 160), "Truck / Police", "2 damage! Police chases you"),
                               ((255, 140, 0), "Barrier / Cone", "Road block, 1 damage"),
                               ((30, 30, 50), "Oil Slick", "Speed -40%, no damage"),
                               ((150, 150, 150), "Broken Car", "Stopped on road, hazard lights")]:
        pygame.draw.rect(surface, color, (rx, sy, 26, 18), border_radius=4)
        surface.blit(fs.render(name, True, WHITE), (rx + 34, sy - 2))
        surface.blit(ft.render(desc, True, LIGHT_GRAY), (rx + 34, sy + 20))
        sy += 48

    # Right column: Tips
    sy += 15
    surface.blit(fm.render("TIPS", True, NEON_GREEN), (rx, sy))
    sy += 38
    for tip in ["Near-miss dodges = COMBO bonus!",
                "Combos stack: x1, x2, x3...",
                "Trucks & Police deal 2x damage",
                "Staying still? Homing cars incoming!",
                "Collect powerups for survival"]:
        surface.blit(ft.render("- " + tip, True, LIGHT_GRAY), (rx, sy))
        sy += 24

    if int(pygame.time.get_ticks() / 500) % 2:
        gt = fm.render("[ SPACE / ENTER / ESC ] Back to Menu", True, LIGHT_GRAY)
        surface.blit(gt, (WIDTH // 2 - gt.get_width() // 2, HEIGHT - 45))
