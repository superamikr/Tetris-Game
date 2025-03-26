from settings import *
from sys import exit

class Main:
    def __init__(self):
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # display
            self.display_surface.fill(YELLOW)
            #מעדכן את המשחק
            pygame.display.update()
            self.clock.tick(60)

    def board(self):
        for x in range(0, WINDOW_WIDTH, COLUMNS):
            for y in range(0, WINDOW_HEIGHT, ROWS):
                pygame.draw.rect(self.display_surface, 'blue', (x, y, CELL_SIZE, CELL_SIZE), 1)

if __name__ == '__main__':
    main = Main()
    main.board()
    main.run()
