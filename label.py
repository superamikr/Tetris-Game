from settings import *


class Label(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font, text_color=(255, 255, 255), bg_color=None, effect=None, speed=3,
                 outline_color=None):
        super().__init__()
        self.base_text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.outline_color = outline_color
        self.effect = effect  # "fade", "blink", or None
        self.speed = speed  # Speed of fade/blink
        self.alpha = 255  # Current opacity
        self.fade_direction = -1  # For fade in/out
        self.visible = True  # For blinking

        self.image = self.render_text()
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(topleft=(x, y))

    def render_text(self):
        text_surface = self.font.render(self.base_text, True, self.text_color, self.bg_color)

        # Add outline if needed
        if self.outline_color:
            # Create a slightly larger surface for the outline
            outline_thickness = 2
            new_surface = pygame.Surface(
                (text_surface.get_width() + outline_thickness * 2,
                 text_surface.get_height() + outline_thickness * 2),
                pygame.SRCALPHA
            )

            # Draw outline rect
            pygame.draw.rect(
                new_surface,
                self.outline_color,
                new_surface.get_rect(),
                width=outline_thickness
            )

            # Blit text on top
            new_surface.blit(text_surface, (outline_thickness, outline_thickness))
            return new_surface
        else:
            return text_surface

    def update(self):
        if self.effect == "fade":
            self.alpha += self.fade_direction * self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_direction = 1
            elif self.alpha >= 255:
                self.alpha = 255
                self.fade_direction = -1
            self.image.set_alpha(self.alpha)

        elif self.effect == "blink":
            if pygame.time.get_ticks() // (500 // self.speed) % 2 == 0:
                if not self.visible:
                    self.image = self.render_text()
                    self.visible = True
            else:
                if self.visible:
                    self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                    self.visible = False
