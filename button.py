from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, text_color, command=None):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.command = command

        self.hovered = False
        self.update_image()

    def update_image(self):
        # Change background color on hover
        color = self.hover_color if self.hovered else self.base_color
        self.image.fill(color)

        # Render text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surf, text_rect)

    def update(self):
        # Check if the mouse is over the button
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered != was_hovered:
            self.update_image()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.command:
                    self.command()
