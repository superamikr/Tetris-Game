from template import *
class Score(Template):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((SIDEBAR_WIDTH,GAME_HEIGHT*SCORE_HEIGHT_FRACTION-PADDING))
        self.rect = self.surface.get_rect(bottomright=(WINDOW_WIDTH-PADDING,WINDOW_HEIGHT-PADDING))
        self.display_surface = pygame.display.get_surface()
