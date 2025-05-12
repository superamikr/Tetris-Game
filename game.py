import pygame
import random
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
        # self.block = Block(self.sprites, (4, 6), 'red')

        # Tetromino
        self.tetromino = Tetromino(random.choice(list(TETROMINOS.keys())), self.sprites)

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


class Tetromino:
    def __init__(self, shape, sprite_group):
        # setup
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.sprite_group = sprite_group
        # create blocks
        self.blocks = [Block(self.sprite_group, pos, self.color) for pos in self.block_positions]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)

        # general
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # positions
        self.pos = pygame.Vector2(pos)+BLOCK_OFFSET
        x = self.pos.x
        y = self.pos.y
        self.rect = self.image.get_rect(topleft=(x * CELL_SIZE, y * CELL_SIZE))
