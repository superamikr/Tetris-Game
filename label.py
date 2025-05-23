from settings import *


class Label(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font, text_color=(255, 255, 255), bg_color=None, effect=None, speed=3):
        super().__init__()
        self.base_text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.effect = effect  # "fade", "blink", or None
        self.speed = speed  # Speed of fade/blink
        self.alpha = 255  # Current opacity
        self.fade_direction = -1  # For fade in/out
        self.visible = True  # For blinking
        self.image = self.render_text()
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(topleft=(x, y))

    def render_text(self):
        """Render the label text."""
        if self.bg_color:
            return self.font.render(self.base_text, True, self.text_color, self.bg_color)
        else:
            return self.font.render(self.base_text, True, self.text_color)

    def update(self):
        """Apply animation effect."""
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
            # Toggle visibility every 30 frames
            if pygame.time.get_ticks() // (500 // self.speed) % 2 == 0:
                if not self.visible:
                    self.image = self.render_text()
                    self.visible = True
            else:
                if self.visible:
                    self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                    self.visible = False
