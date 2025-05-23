from settings import *
from sys import exit
from game import Game
from score import Score
from preview import Preview
from random import choice
from label import Label
from button import Button
from os import path

class Main:

    def __init__(self):

        # general
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')
        # Main menu
        self.isOpening = True
        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # Buttons setup
        self.buttons = pygame.sprite.Group()

        # Labels setup
        self.labels = pygame.sprite.Group()

        # screen components
        self.game = Game(self.get_next_shape,self.update_score)
        self.score = Score()
        self.preview = Preview()

        # Adding labels:
        fontTitle = pygame.font.Font(path.join('graphics', 'tetrisFont.ttf'), 60)
        font = pygame.font.SysFont(path.join('graphics', 'tetrisFont.ttf'), 38)
        self.AddLabel(WINDOW_WIDTH - 3*WINDOW_WIDTH / 4,
                      WINDOW_HEIGHT - WINDOW_HEIGHT / 4,
                      "click SPACE to start...", font,
                       effect="fade",speed=3)
        self.AddLabel(WINDOW_WIDTH -  3*WINDOW_WIDTH / 4,
                      WINDOW_HEIGHT - 3*WINDOW_HEIGHT / 4,
                      "TETRO SPACE", fontTitle,
                       speed=3)
    def update_score(self,lines,score,level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def AddLabel(self, x, y, text, font, text_color=(255, 255, 255), bg_color=None, effect=None, speed=3):
        self.labels.add(Label(x, y, text, font,
                              text_color=text_color,
                               bg_color=bg_color,
                              effect=effect, speed=speed))

    def AddButton(self, x, y, width, height, text, font, base_color, hover_color, text_color, command=None):
        if command:
            self.buttons.add(Button(x, y, width, height, text, font,
                                    base_color, hover_color, text_color, command))
        else:
            self.buttons.add(Button(x, y, width, height, text, font,
                                    base_color, hover_color, text_color))

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape


    # Adding buttons:

    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # display
            self.display_surface.fill(GRAY)
            # opening window
            if self.isOpening:
                self.MainMenu()
                self.labels.update()
                self.labels.draw(self.display_surface)
            else:
                # game components
                self.score.run()
                self.game.run()
                self.preview.run(self.next_shapes)
            # screen updating - Updates the game's screen
            pygame.display.update()
            self.clock.tick(FPS)

    def MainMenu(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.isOpening = False
            return
        open_window_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        open_win_rect = open_window_surface.get_rect(topright=(WINDOW_WIDTH, PADDING))

        open_window_surface.fill(GRAY)
        self.display_surface.blit(open_window_surface, open_win_rect)

    def board(self):
        for x in range(0, WINDOW_WIDTH, COLUMNS):
            for y in range(0, WINDOW_HEIGHT, ROWS):
                pygame.draw.rect(self.display_surface, 'blue', (x, y, CELL_SIZE, CELL_SIZE), 1)


if __name__ == '__main__':
    main = Main()
    main.board()
    main.run()
