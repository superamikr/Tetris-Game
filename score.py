from settings import *
from os.path import join
from template import Template


class Score(Template):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()

        # Font
        self.font = pygame.font.Font(join('graphics', 'Russo_One.ttf'), 30)

        # increment
        self.increment_height = self.surface.get_height() / 3

        # data
        self.lines = 0
        self.score = 0
        self.level = 1

    def display_text(self, pos, text):
        text_surface = self.font.render(f'{text[0]} : {text[1]}', True, 'white')
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill(GRAY)
        for i, text in enumerate([('Score',self.score), ('Level',self.level), ('Lines',self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            self.display_text((x, y), text)

        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)
