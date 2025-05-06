from settings import *


class Template():
    def __init__(self):
        self.surface = pygame.Surface((WINDOW_HEIGHT,WINDOW_WIDTH))
        self.rect = self.surface.get_rect()
        self.display_surface = pygame.display.get_surface()
    def run(self):
        self.display_surface.blit(self.surface,self.rect)
