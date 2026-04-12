"""Procedural sound generation via pygame.mixer."""

import math
import pygame


def make_beep(freq=440, duration_ms=100, volume=0.15):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = bytearray(n_samples * 2)
    for i in range(n_samples):
        t = i / sample_rate
        envelope = min(1.0, min(i, n_samples - i) / (sample_rate * 0.005))
        val = int(32767 * volume * envelope * math.sin(2 * math.pi * freq * t))
        buf[i * 2] = val & 0xFF
        buf[i * 2 + 1] = (val >> 8) & 0xFF
    return pygame.mixer.Sound(buffer=bytes(buf))


class SoundBank:
    """Lazy-initialised collection of all game sounds."""

    def __init__(self):
        self.available = False
        try:
            self.boost    = make_beep(180, 200, 0.12)
            self.crash    = make_beep(80,  300, 0.20)
            self.nearmiss = make_beep(880,  80, 0.08)
            self.pickup   = make_beep(660, 120, 0.10)
            self.honk     = make_beep(350, 250, 0.10)
            self.select   = make_beep(520,  80, 0.08)
            self.available = True
        except Exception:
            pass

    def play(self, name: str):
        if self.available:
            sound = getattr(self, name, None)
            if sound:
                sound.play()
