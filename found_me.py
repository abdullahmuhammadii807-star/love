import math
import random
import sys
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Setup Screen
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Souls, One Universe")
clock = pygame.time.Clock()

# Colors
COLOR_BG = (8, 6, 15)
COLOR_PINK = (255, 90, 160)
COLOR_RED = (255, 40, 70)
COLOR_GOLD = (245, 210, 120)
COLOR_WHITE = (255, 255, 255)
COLOR_CARD = (25, 18, 30)

# Fonts
font_title = pygame.font.SysFont("georgia", 22)
font_large = pygame.font.SysFont("georgia", 40, bold=True)
font_sub = pygame.font.SysFont("sans-serif", 13)
font_card = pygame.font.SysFont("georgia", 16)


def draw_heart(surface, x, y, scale, color_alpha):
    """Utility function to draw a filled heart shape with alpha transparency."""
    points = []
    # Parametric heart formula
    for t in range(0, 360, 5):
        rad = math.radians(t)
        hx = 16 * (math.sin(rad) ** 3)
        hy = -(
            13 * math.cos(rad)
            - 5 * math.cos(2 * rad)
            - 2 * math.cos(3 * rad)
            - math.cos(4 * rad)
        )
        points.append((x + hx * scale, y + hy * scale))

    if len(points) > 2:
        pygame.draw.polygon(surface, color_alpha, points)


class BackgroundStar:
    """Floating background universe particles."""

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2.0)
        self.alpha = random.randint(40, 180)
        self.speed = random.uniform(0.1, 0.4)

    def update(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        s = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(
            s, (255, 255, 255, self.alpha), (2, 2), int(self.size)
        )
        surface.blit(s, (self.x, self.y))


class Particle:
    """Twinkling particle trail emitted from hearts."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.scale = random.uniform(0.1, 0.35)
        angle = random.uniform(0, math.tau)
        speed = random.uniform(0.5, 2.2)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 255
        self.decay = random.uniform(4, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay

    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((30, 30), pygame.SRCALPHA)
            draw_heart(s, 15, 15, self.scale, (*self.color, int(self.life)))
            surface.blit(s, (self.x - 15, self.y - 15))


class GlowingSoulHeart:
    """Interactive dragable glowing and twinkling HEART shape."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.color = color
        self.dragging = False
        self.particles = []
        self.twinkle_timer = random.uniform(0, 10)

    def update(self):
        # Smooth spring motion towards mouse when dragging
        self.x += (self.target_x - self.x) * 0.3
        self.y += (self.target_y - self.y) * 0.3
        self.twinkle_timer += 0.08

        # Emit heart trail particles continuously
        if random.random() < 0.65:
            px = self.x + random.uniform(-10, 10)
            py = self.y + random.uniform(-10, 10)
            self.particles.append(Particle(px, py, self.color))

        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, surface):
        # Draw particle trails
        for p in self.particles:
            p.draw(surface)

        # Calculate dynamic pulse / twinkle scaling
        pulse = 1.0 + 0.08 * math.sin(self.twinkle_timer)

        # Draw multi-layered outer glowing hearts
        for layer in range(4, 0, -1):
            scale = (layer * 0.75) * pulse
            s = pygame.Surface((160, 160), pygame.SRCALPHA)
            alpha = int(110 / (layer * 1.4))

            # Twinkle brightness fluctuation
            if random.random() < 0.05:
                alpha = min(255, alpha + 40)

            draw_heart(s, 80, 80, scale, (*self.color, alpha))
            surface.blit(s, (self.x - 80, self.y - 80))

        # Core bright inner white-pink heart
        core_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        draw_heart(core_surf, 40, 40, 0.8 * pulse, (255, 240, 245, 230))
        surface.blit(core_surf, (self.x - 40, self.y - 40))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot(event.pos[0] - self.x, event.pos[1] - self.y) < 45:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.target_x, self.target_y = event.pos


def main():
    bg_stars = [BackgroundStar() for _ in range(80)]
    soul_left = GlowingSoulHeart(250, 320, COLOR_RED)
    soul_right = GlowingSoulHeart(650, 320, COLOR_PINK)

    stage = "DRAG"
    running = True

    while running:
        clock.tick(60)
        screen.fill(COLOR_BG)

        # Update Universe Background
        for star in bg_stars:
            star.update()
            star.draw(screen)

        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if stage == "DRAG":
                soul_left.handle_event(event)
                soul_right.handle_event(event)

            elif stage == "REVEALED":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if 400 <= mx <= 500 and 380 <= my <= 440:
                        stage = "LETTER_OPEN"

            elif stage == "LETTER_OPEN":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if 615 <= mx <= 645 and 115 <= my <= 145:
                        stage = "REVEALED"

        # Collision detection between hearts
        dist = math.hypot(soul_left.x - soul_right.x, soul_left.y - soul_right.y)
        if stage == "DRAG" and dist < 55:
            stage = "REVEALED"

        # Render Stage 1: Drag Glowing Hearts
        if stage == "DRAG":
            header = font_title.render(
                "two souls. one universe.", True, (160, 160, 175)
            )
            screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 70))

            instruction = font_sub.render(
                "DRAG THE SOULS TOGETHER ♥", True, (110, 110, 130)
            )
            screen.blit(
                instruction, (WIDTH // 2 - instruction.get_width() // 2, 540)
            )

            soul_left.update()
            soul_right.update()
            soul_left.draw(screen)
            soul_right.draw(screen)

        # Render Stage 2: Fused Hearts & Revealed Text
        elif stage in ["REVEALED", "LETTER_OPEN"]:
            # Combined Heart Core Fusion in center
            cx, cy = WIDTH // 2, 100
            for scale, color in [(1.8, COLOR_RED), (1.2, COLOR_PINK)]:
                hs = pygame.Surface((160, 160), pygame.SRCALPHA)
                draw_heart(hs, 80, 80, scale, (*color, 90))
                screen.blit(hs, (cx - 80, cy - 80))

            t_sub = font_sub.render("IN 8 BILLION PEOPLE", True, (160, 160, 175))
            t_main = font_large.render('"...YOU FOUND ME."', True, COLOR_WHITE)
            t_cap = font_sub.render(
                "SOME THINGS ARE WRITTEN IN THE STARS", True, COLOR_GOLD
            )

            screen.blit(t_sub, (WIDTH // 2 - t_sub.get_width() // 2, 160))
            screen.blit(t_main, (WIDTH // 2 - t_main.get_width() // 2, 205))
            screen.blit(t_cap, (WIDTH // 2 - t_cap.get_width() // 2, 270))

            # Envelope Button
            env_rect = pygame.Rect(415, 370, 70, 48)
            pygame.draw.rect(screen, COLOR_RED, env_rect, border_radius=6)
            pygame.draw.polygon(
                screen, COLOR_WHITE, [(415, 370), (450, 395), (485, 370)]
            )

            hint = font_sub.render(
                "PULL APART WITH TWO FINGERS TO SEPARATE • OR CLICK ENVELOPE",
                True,
                (120, 120, 140),
            )
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 470))

        # Render Stage 3: Love Note Popup Modal
        if stage == "LETTER_OPEN":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            card = pygame.Rect(260, 110, 380, 390)
            pygame.draw.rect(screen, COLOR_CARD, card, border_radius=14)
            pygame.draw.rect(screen, COLOR_GOLD, card, width=1, border_radius=14)

            close_btn = font_title.render("×", True, (200, 200, 200))
            screen.blit(close_btn, (620, 120))

            lines = [
                ("Dear Love,", True),
                ("", False),
                ("My love for you grows stronger with", False),
                ("every passing second. You are the", False),
                ("missing piece of my soul that I finally", False),
                ("found. Thank you for being my universe,", False),
                ("my everything.", False),
                ("", False),
                ("With all my love,", False),
                ("From Love", True),
            ]

            y_pos = 145
            for text, is_bold in lines:
                if text:
                    color = COLOR_WHITE if not is_bold else COLOR_GOLD
                    txt_surface = font_card.render(text, True, color)
                    screen.blit(
                        txt_surface,
                        (WIDTH // 2 - txt_surface.get_width() // 2, y_pos),
                    )
                y_pos += 26

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()