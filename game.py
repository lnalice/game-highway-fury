"""Main Game class: state machine, update loop, rendering orchestration."""

import random
import sys

import pygame

from highway_fury.config import (
    WIDTH, HEIGHT, FPS, TITLE, WHITE, RED, ORANGE, CYAN, NEON_GREEN, NEON_PINK,
    SKY_BLUE, YELLOW, SHOULDER_COLOR, ROAD_COLOR, ROAD_LEFT, ROAD_RIGHT,
    ROAD_WIDTH, LANE_COUNT, LANE_WIDTH, LANE_CENTERS,
    OBS_CAR, OBS_TRUCK, OBS_MOTORCYCLE, OBS_BARRIER, OBS_CONE,
    OBS_OIL, OBS_BROKEN, OBS_POLICE,
    POWERUP_NITRO, POWERUP_SHIELD, POWERUP_MAGNET,
    DIFFICULTY_PRESETS, DIFFICULTY_KEYS, CHARACTER_KEYS,
)
from highway_fury.sounds import SoundBank
from highway_fury.drawing.scenery import draw_tree, draw_mountain
from highway_fury.entities import Particle, SpeedLine, FloatingText, Obstacle, PowerUp, Player
from highway_fury.screens import (
    draw_menu, draw_difficulty_select, draw_character_select, draw_guide,
    draw_hud, draw_gameover, draw_pause,
)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.render_surface = pygame.Surface((WIDTH, HEIGHT))
        self.sounds = SoundBank()

        self.fonts = {
            "huge":   pygame.font.Font(None, 90),
            "large":  pygame.font.Font(None, 72),
            "medium": pygame.font.Font(None, 42),
            "small":  pygame.font.Font(None, 30),
            "tiny":   pygame.font.Font(None, 24),
        }

        self.state = "menu"
        self.selected_difficulty = "normal"
        self.selected_character = "rabbit"
        self.diff_index = 1
        self.char_index = 0
        self.menu_index = 0

        self.player = Player()
        self.obstacles = []
        self.powerups = []
        self.particles = []
        self.speed_lines = []
        self.floating_texts = []
        self.road_offset = 0.0
        self.score = 0.0
        self.distance = 0.0
        self.high_score = 0.0
        self.spawn_timer = 0.0
        self.powerup_timer = 0.0
        self.difficulty = 1.0
        self.passed_cars = 0
        self.combo = 0
        self.combo_timer = 0.0
        self.max_combo_reached = 0

        self.trees_left = [(random.randint(20, 170), random.randint(0, HEIGHT)) for _ in range(15)]
        self.trees_right = [(random.randint(730, 880), random.randint(0, HEIGHT)) for _ in range(15)]

        self.shake_x = self.shake_y = 0
        self.shake_amount = 0.0
        self.screen_flash = 0.0
        self.flash_color = WHITE
        self.slow_mo = 1.0
        self.slow_mo_timer = 0.0
        self.menu_time = 0.0
        self.total_time = 0.0
        self.zone_text = ""
        self.zone_timer = 0.0
        self.cheese_timer = 0.0
        self.cheese_x = 0.0

    # ── Reset ──

    def reset(self):
        self.player = Player(self.selected_difficulty, self.selected_character)
        self.obstacles.clear()
        self.powerups.clear()
        self.particles.clear()
        self.speed_lines.clear()
        self.floating_texts.clear()
        self.score = self.distance = 0.0
        self.spawn_timer = 0.0
        self.powerup_timer = 5.0
        self.difficulty = 1.0
        self.passed_cars = self.combo = 0
        self.combo_timer = 0.0
        self.shake_amount = self.shake_x = self.shake_y = 0
        self.screen_flash = 0.0
        self.slow_mo = 1.0
        self.slow_mo_timer = self.total_time = 0.0
        self.zone_text = ""
        self.zone_timer = 0.0
        self.cheese_timer = self.cheese_x = 0.0
        self.max_combo_reached = 0

    # ── Effects ──

    def trigger_shake(self, amount=0.4):
        self.shake_amount = amount

    def trigger_flash(self, color=WHITE, duration=0.15):
        self.screen_flash = duration
        self.flash_color = color

    def trigger_slowmo(self, duration=0.5):
        self.slow_mo = 0.3
        self.slow_mo_timer = duration

    # ── Spawning ──

    def _pick_obstacle_type(self):
        d = self.difficulty
        r = random.random()
        if d < 2:
            if r < 0.45: return OBS_CAR
            if r < 0.65: return OBS_TRUCK
            if r < 0.80: return OBS_MOTORCYCLE
            if r < 0.90: return OBS_CONE
            return OBS_OIL
        if d < 4:
            if r < 0.30: return OBS_CAR
            if r < 0.45: return OBS_TRUCK
            if r < 0.58: return OBS_MOTORCYCLE
            if r < 0.68: return OBS_BARRIER
            if r < 0.76: return OBS_CONE
            if r < 0.84: return OBS_OIL
            if r < 0.92: return OBS_BROKEN
            return OBS_POLICE
        if r < 0.22: return OBS_CAR
        if r < 0.37: return OBS_TRUCK
        if r < 0.52: return OBS_MOTORCYCLE
        if r < 0.62: return OBS_BARRIER
        if r < 0.70: return OBS_CONE
        if r < 0.78: return OBS_OIL
        if r < 0.88: return OBS_BROKEN
        return OBS_POLICE

    def _has_obstacle_near(self, x, y, min_dist=180):
        return any(abs(o.x - x) < 40 and abs(o.y - y) < min_dist for o in self.obstacles)

    def _speed_mult(self):
        return DIFFICULTY_PRESETS[self.selected_difficulty]["speed_mult"]

    def spawn_obstacle(self):
        p = random.random()
        d = self.difficulty
        if p < 0.15 and d > 1.5:
            self._spawn_wall_pattern(); return
        if p < 0.30:
            self._spawn_offset(); return
        if p < 0.40 and d > 2.0:
            self._spawn_targeted(); return

        lane = random.randint(0, LANE_COUNT - 1)
        if self._has_obstacle_near(LANE_CENTERS[lane], -150):
            return
        speed = random.uniform(60, 140) * min(d, 3.0) * self._speed_mult()
        self.obstacles.append(Obstacle(self._pick_obstacle_type(), lane, -150, speed))

    def _spawn_offset(self):
        bi = random.randint(0, LANE_COUNT - 2)
        bx = ROAD_LEFT + (bi + 1) * LANE_WIDTH + random.randint(-10, 10)
        if self._has_obstacle_near(bx, -150):
            return
        otype = random.choice([OBS_CAR, OBS_MOTORCYCLE, OBS_BARRIER, OBS_OIL, OBS_CONE])
        speed = random.uniform(60, 140) * min(self.difficulty, 3.0) * self._speed_mult()
        self.obstacles.append(Obstacle(otype, bi, -150, speed, x_override=bx))

    def _spawn_wall_pattern(self):
        gap = random.randint(0, LANE_COUNT - 1)
        sm = self._speed_mult()
        for lane in range(LANE_COUNT):
            if lane == gap or self._has_obstacle_near(LANE_CENTERS[lane], -150, 250):
                continue
            otype = random.choice([OBS_CAR, OBS_TRUCK, OBS_BROKEN])
            speed = random.uniform(60, 100) * min(self.difficulty, 2.5) * sm
            self.obstacles.append(Obstacle(otype, lane, -150 + random.randint(-20, 20), speed))

    def _spawn_targeted(self):
        px = self.player.x
        if self._has_obstacle_near(px, -150, 200):
            return
        nl = min(range(LANE_COUNT), key=lambda i: abs(LANE_CENTERS[i] - px))
        otype = random.choice([OBS_POLICE, OBS_MOTORCYCLE, OBS_CAR])
        speed = random.uniform(80, 160) * min(self.difficulty, 3.0) * self._speed_mult()
        obs = Obstacle(otype, nl, -150, speed, x_override=px)
        if otype != OBS_POLICE:
            obs.tracks_player = True
            obs.track_speed = random.uniform(60, 140)
        self.obstacles.append(obs)

    def spawn_powerup(self):
        ptype = random.choice([POWERUP_NITRO, POWERUP_SHIELD, POWERUP_MAGNET])
        self.powerups.append(PowerUp(ptype, random.randint(0, LANE_COUNT - 1), -50))

    def _detect_cheese(self, dt):
        px = self.player.x
        if abs(px - self.cheese_x) < 25:
            self.cheese_timer += dt
        else:
            self.cheese_timer = max(0, self.cheese_timer - dt * 2)
            self.cheese_x = px
        if self.cheese_timer > 1.5 and self.player.speed > 30:
            self._spawn_targeted()
            if self.cheese_timer > 3.0:
                self._spawn_targeted()
                self._spawn_offset()
            self.cheese_timer = max(1.0, self.cheese_timer - 0.8)

    def _check_speed_zone(self):
        s = self.player.speed
        old = self.zone_text
        new = ("HYPER SPEED!" if s >= 600 else "INSANE!" if s >= 450 else
               "TURBO ZONE!" if s >= 300 else "FAST!" if s >= 200 else "")
        if new and new != old:
            self.zone_text = new
            self.zone_timer = 2.0
            self.trigger_flash(NEON_PINK, 0.1)

    # ── Collision / interaction ──

    def _check_near_miss(self):
        pr = self.player.get_rect()
        expanded = pr.inflate(35, 35)
        for o in self.obstacles:
            if o.type in (OBS_OIL, OBS_CONE):
                continue
            er = o.get_rect()
            if expanded.colliderect(er) and not pr.colliderect(er) and abs(o.y - self.player.y) < 30 and not o.passed:
                o.passed = True
                self.combo += 1
                self.combo_timer = 3.0
                self.max_combo_reached = max(self.max_combo_reached, self.combo)
                bonus = 50 * self.combo * self.player.score_mult
                if self.selected_character == "lion":
                    bonus *= 2
                self.score += bonus
                self.floating_texts.append(FloatingText(self.player.x, self.player.y - 60, f"NEAR MISS! +{int(bonus)}", NEON_GREEN))
                if self.combo >= 5:
                    self.trigger_flash(NEON_GREEN, 0.08)
                self.sounds.play("nearmiss")

    def _check_collisions(self):
        if self.player.invincible > 0:
            return
        pr = self.player.get_rect()
        for o in self.obstacles:
            if not pr.colliderect(o.get_rect()):
                continue
            if o.type == OBS_OIL:
                self.player.speed *= 0.6
                self.floating_texts.append(FloatingText(self.player.x, self.player.y - 40, "OIL!", (100, 100, 200)))
                self.obstacles.remove(o)
                self.trigger_shake(0.15)
                break
            if self.player.shield > 0:
                for _ in range(15):
                    self.particles.append(Particle(o.x, o.y, CYAN, gravity=100))
                self.floating_texts.append(FloatingText(o.x, o.y - 40, "BLOCKED!", CYAN))
                self.obstacles.remove(o)
                self.trigger_flash(CYAN, 0.1)
                break
            damage = 2 if o.type in (OBS_TRUCK, OBS_POLICE) else 1
            if self.selected_character == "croc" and damage > 1:
                damage -= 1
            self.player.hp -= damage
            self.player.speed *= 0.3
            self.combo = 0
            self.player.invincible = 1.5
            self.player.hurt_timer = 1.5
            self.score = max(0, self.score - 200)
            for _ in range(50):
                self.particles.append(Particle(self.player.x, self.player.y,
                    random.choice([(255, 150, 0), (255, 80, 0), (255, 220, 50), (255, 50, 0)]), gravity=150))
            for _ in range(10):
                self.particles.append(Particle(o.x, o.y, (200, 200, 200), gravity=80))
            self.trigger_shake(0.6 + damage * 0.2)
            self.trigger_flash(RED, 0.15)
            self.trigger_slowmo(0.3)
            self.floating_texts.append(FloatingText(self.player.x, self.player.y - 60, f"-{damage} HP!", RED, 1.5))
            self.sounds.play("crash")
            self.obstacles.remove(o)
            break

    def _check_powerup_pickup(self):
        pr = self.player.get_rect()
        for p in self.powerups[:]:
            if not pr.colliderect(p.get_rect()):
                continue
            if p.type == POWERUP_NITRO:
                self.player.nitro = min(self.player.max_nitro, self.player.nitro + 50)
                self.floating_texts.append(FloatingText(p.x, p.y - 30, "NITRO +50!", ORANGE))
            elif p.type == POWERUP_SHIELD:
                self.player.shield = 8
                self.floating_texts.append(FloatingText(p.x, p.y - 30, "SHIELD!", CYAN))
            elif p.type == POWERUP_MAGNET:
                self.player.score_mult = 2
                self.player.score_mult_timer = 10
                self.floating_texts.append(FloatingText(p.x, p.y - 30, "SCORE x2!", NEON_GREEN))
            for _ in range(15):
                self.particles.append(Particle(p.x, p.y, p.color, gravity=50))
            self.trigger_flash(p.color, 0.08)
            self.sounds.play("pickup")
            self.powerups.remove(p)

    def _explode_player(self):
        for _ in range(100):
            self.particles.append(Particle(
                self.player.x + random.randint(-30, 30),
                self.player.y + random.randint(-30, 30),
                random.choice([(255, 100, 0), (255, 200, 0), (255, 50, 0), (255, 255, 100), (200, 50, 0)]),
                random.uniform(-250, 250), random.uniform(-350, 100),
                random.uniform(0.5, 2.0), random.randint(3, 12), 200,
            ))
        self.trigger_shake(1.0)
        self.trigger_flash(ORANGE, 0.3)

    # ── Update ──

    def update(self, dt):
        if self.state == "menu":
            self.menu_time += dt
            return
        if self.state != "playing":
            return

        if self.slow_mo_timer > 0:
            self.slow_mo_timer -= dt
            if self.slow_mo_timer <= 0:
                self.slow_mo = 1.0
        dt *= self.slow_mo
        self.total_time += dt

        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)

        self.road_offset += self.player.speed * dt * 3.5
        self.distance += self.player.speed * dt * 0.01
        mult = self.player.score_mult
        if self.selected_character == "lion":
            mult *= 1 + self.combo * 0.1
        self.score += self.player.speed * dt * 0.15 * mult

        dr = DIFFICULTY_PRESETS[self.selected_difficulty]["diff_rate"]
        self.difficulty = 1.0 + self.distance * dr
        sm = DIFFICULTY_PRESETS[self.selected_difficulty]["spawn_mult"]

        self.spawn_timer -= dt
        spawn_interval = max(0.15, (1.0 - self.difficulty * 0.05) / sm)
        if self.spawn_timer <= 0 and self.player.speed > 10:
            self.spawn_obstacle()
            if self.difficulty > 2 and random.random() < 0.4:
                self.spawn_obstacle()
            if self.difficulty > 4 and random.random() < 0.3:
                self.spawn_obstacle()
            self.spawn_timer = spawn_interval

        self.powerup_timer -= dt
        if self.powerup_timer <= 0:
            self.spawn_powerup()
            self.powerup_timer = random.uniform(6, 12)

        px = self.player.x
        for o in self.obstacles:
            o.update(dt, self.player.speed, px)
        for p in self.powerups:
            p.update(dt, self.player.speed)

        self._detect_cheese(dt)
        self._check_near_miss()
        self._check_collisions()
        self._check_powerup_pickup()
        self._check_speed_zone()

        for o in self.obstacles[:]:
            if o.y > HEIGHT + 200:
                self.obstacles.remove(o)
                if not o.passed and o.type in (OBS_CAR, OBS_TRUCK, OBS_MOTORCYCLE, OBS_POLICE):
                    self.passed_cars += 1
                    self.score += 15 * mult
        self.powerups = [p for p in self.powerups if p.y <= HEIGHT + 100]
        self.floating_texts = [t for t in self.floating_texts if t.life > 0]
        for t in self.floating_texts:
            t.update(dt)

        sr = max(0, (self.player.speed - 200) / 300)
        while len(self.speed_lines) < int(sr * 20):
            self.speed_lines.append(SpeedLine())
        for sl in self.speed_lines:
            sl.update(dt)
        self.speed_lines = [sl for sl in self.speed_lines if sl.y <= HEIGHT + 100]

        spd = self.player.speed * dt * 3.5
        for i, (tx, ty) in enumerate(self.trees_left):
            self.trees_left[i] = (tx, (ty + spd) % (HEIGHT + 50))
        for i, (tx, ty) in enumerate(self.trees_right):
            self.trees_right[i] = (tx, (ty + spd) % (HEIGHT + 50))

        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update(dt)

        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo = 0
        if self.zone_timer > 0:
            self.zone_timer -= dt

        if self.shake_amount > 0:
            self.shake_x = random.randint(int(-self.shake_amount * 15), int(self.shake_amount * 15))
            self.shake_y = random.randint(int(-self.shake_amount * 15), int(self.shake_amount * 15))
            self.shake_amount -= dt * 2
        else:
            self.shake_x = self.shake_y = 0
        if self.screen_flash > 0:
            self.screen_flash -= dt

        if self.player.nitro_active:
            for _ in range(3):
                self.particles.append(Particle(
                    self.player.x + random.randint(-12, 12),
                    self.player.y + self.player.height // 2,
                    random.choice([(255, 140, 0), (255, 200, 50), (255, 80, 0)]),
                    random.uniform(-30, 30), random.uniform(100, 300), 0.4, random.randint(3, 8),
                ))
        if self.player.speed > 250 and random.random() < 0.4:
            side = random.choice([-1, 1])
            self.particles.append(Particle(
                self.player.x + side * self.player.width // 2,
                self.player.y + self.player.height // 2,
                (200, 200, 255), side * random.uniform(10, 40), random.uniform(50, 150), 0.3, 2, 0,
            ))

        if self.player.hp <= 0:
            self.high_score = max(self.high_score, self.score)
            self.state = "gameover"
            self._explode_player()
            self.sounds.play("crash")

    # ── Drawing helpers ──

    def draw_background(self, surface):
        surface.fill(SKY_BLUE)
        draw_mountain(surface, -50, 180, 300, 130, (120, 140, 160))
        draw_mountain(surface, 100, 180, 250, 100, (140, 155, 170))
        draw_mountain(surface, 600, 180, 350, 140, (115, 135, 155))
        draw_mountain(surface, 750, 180, 200, 90, (135, 150, 165))
        pygame.draw.rect(surface, (80, 160, 80), (0, 160, WIDTH, HEIGHT - 160))

    def draw_road(self, surface):
        pygame.draw.rect(surface, SHOULDER_COLOR, (ROAD_LEFT - 15, 0, ROAD_WIDTH + 30, HEIGHT))
        pygame.draw.rect(surface, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.rect(surface, YELLOW, (ROAD_LEFT - 5, 0, 5, HEIGHT))
        pygame.draw.rect(surface, YELLOW, (ROAD_RIGHT, 0, 5, HEIGHT))
        dl, gl = 40, 30
        offset = self.road_offset % (dl + gl)
        for lane in range(1, LANE_COUNT):
            lx = ROAD_LEFT + lane * LANE_WIDTH
            y = -offset
            while y < HEIGHT:
                pygame.draw.rect(surface, WHITE, (lx - 2, int(y), 4, dl))
                y += dl + gl

    def draw_scenery(self, surface):
        for tx, ty in self.trees_left:
            draw_tree(surface, int(tx), int(ty), 0.8)
        for tx, ty in self.trees_right:
            draw_tree(surface, int(tx), int(ty), 0.8)

    # ── Main draw ──

    def draw(self):
        surf = self.render_surface

        if self.state == "menu":
            draw_menu(surf, self)
            self.screen.blit(surf, (0, 0))
            return
        if self.state == "difficulty_select":
            draw_difficulty_select(surf, self)
            self.screen.blit(surf, (0, 0))
            return
        if self.state == "character_select":
            draw_character_select(surf, self)
            self.screen.blit(surf, (0, 0))
            return
        if self.state == "guide":
            draw_guide(surf, self)
            self.screen.blit(surf, (0, 0))
            return

        self.draw_background(surf)
        self.draw_road(surf)
        self.draw_scenery(surf)
        for sl in self.speed_lines:
            sl.draw(surf, max(0, (self.player.speed - 200) / 300))
        for o in self.obstacles:
            o.draw(surf)
        for p in self.powerups:
            p.draw(surf)
        self.player.draw(surf)
        for p in self.particles:
            p.draw(surf)
        for ft in self.floating_texts:
            ft.draw(surf)
        draw_hud(surf, self)

        if self.state == "paused":
            draw_pause(surf, self)
        elif self.state == "gameover":
            for p in self.particles:
                p.draw(surf)
            draw_gameover(surf, self)

        if self.screen_flash > 0:
            fs = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fs.fill((*self.flash_color[:3], int(min(200, self.screen_flash * 600))))
            surf.blit(fs, (0, 0))

        self.screen.blit(surf, (int(self.shake_x), int(self.shake_y)))

    # ── Event handling ──

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type != pygame.KEYDOWN:
                continue

            if self.state == "menu":
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.menu_index = (self.menu_index - 1) % 3
                    self.sounds.play("select")
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.menu_index = (self.menu_index + 1) % 3
                    self.sounds.play("select")
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if self.menu_index == 0:
                        self.state = "difficulty_select"
                    elif self.menu_index == 1:
                        self.state = "guide"
                    elif self.menu_index == 2:
                        self.state = "character_select"
                    self.sounds.play("boost")

            elif self.state == "difficulty_select":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.diff_index = (self.diff_index - 1) % 3
                    self.sounds.play("select")
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.diff_index = (self.diff_index + 1) % 3
                    self.sounds.play("select")
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.selected_difficulty = DIFFICULTY_KEYS[self.diff_index]
                    self.selected_character = CHARACTER_KEYS[self.char_index]
                    self.reset()
                    self.state = "playing"
                    self.sounds.play("boost")
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

            elif self.state == "character_select":
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.char_index = (self.char_index - 1) % 4
                    self.sounds.play("select")
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.char_index = (self.char_index + 1) % 4
                    self.sounds.play("select")
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.selected_character = CHARACTER_KEYS[self.char_index]
                    self.state = "menu"
                    self.sounds.play("boost")
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

            elif self.state == "guide":
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                    self.state = "menu"
                    self.sounds.play("select")

            elif self.state == "playing":
                if event.key == pygame.K_ESCAPE:
                    self.state = "paused"
                if event.key == pygame.K_SPACE:
                    self.sounds.play("honk")

            elif self.state == "paused":
                if event.key == pygame.K_SPACE:
                    self.state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "menu"

            elif self.state == "gameover":
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.state = "menu"

        return True

    # ── Main loop ──

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            if not self._handle_events():
                break
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    async def run_async(self):
        """pygbag-compatible async game loop for browser execution."""
        import asyncio
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            if not self._handle_events():
                break
            self.update(dt)
            self.draw()
            pygame.display.flip()
            await asyncio.sleep(0)
