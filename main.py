from settings import *
from sys import exit
from game import Game
from score import Score
from preview import Preview
from random import choice


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
        # Button setup
        self.button_font = pygame.font.SysFont("Ariel", 36)
        self.button_rect = pygame.Rect(125, 100, 150, 60)
        self.button_text = self.button_font.render("Click Me", True, WHITE)

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # componemts
        self.game = Game(self.get_next_shape)
        self.score = Score()
        self.preview = Preview()

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(TETROMINOS.keys())))
        return next_shape

    def draw_button(self, surface, rect, text_surface, hover=False):
        color = DARK_BLUE if hover else BLUE
        pygame.draw.rect(surface, color, rect, border_radius=10)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

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

                # Draw the button here
                mouse_pos = pygame.mouse.get_pos()
                is_hovering = self.button_rect.collidepoint(mouse_pos)
                self.draw_button(self.display_surface, self.button_rect, self.button_text, hover=is_hovering)

                # Handle click
                if pygame.mouse.get_pressed()[0] and is_hovering:
                    print("Button clicked!")
            else:
                # רכיבי המשחק
                self.score.run()
                self.game.run()
                self.preview.run(self.next_shapes)
            # מעדכן את המשחק
            pygame.display.update()
            self.clock.tick(FPS)

    def MainMenu(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.isOpening = False
            return
        open_window_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        open_win_rect = open_window_surface.get_rect(topright=(WINDOW_WIDTH, PADDING))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Welcome to my game!', True, GREEN, BLUE)
        textRect = text.get_rect()
        textRect.center = (WINDOW_WIDTH // 2, WINDOW_WIDTH // 2)
        open_window_surface.fill(GRAY)
        self.display_surface.blit(open_window_surface, open_win_rect)
        self.display_surface.blit(text, textRect)

    def board(self):
        for x in range(0, WINDOW_WIDTH, COLUMNS):
            for y in range(0, WINDOW_HEIGHT, ROWS):
                pygame.draw.rect(self.display_surface, 'blue', (x, y, CELL_SIZE, CELL_SIZE), 1)


if __name__ == '__main__':
    main = Main()
    main.board()
    main.run()
