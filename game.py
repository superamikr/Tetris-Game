from template import *


class Game(Template):
    def __init__(self):
        super().__init__()
        # General
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))

        # the-lines
        self.line_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        self.line_surface.fill((0, 255, 0, 120))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # test Block
        self.sprites = pygame.sprite.Group()
        self.block = Block(self.sprites)

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)
        self.surface.blit(self.line_surface, (0, 0))

    def run(self):
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)
        self.sprites.update()
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)


class Block(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.waitT = 0
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=(0, 0))

    def update(self):
        if self.waitT ==0:
            self.rect.y += CELL_SIZE
            self.waitT = 30
        if self.waitT>0:
            self.waitT-=1
