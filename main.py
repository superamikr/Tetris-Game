from settings import *
from sys import exit
from game import Game
from score import Score
from preview import Preview
from random import choice
from label import Label
from button import Button
from os import path
from pygame import mixer


class Main:

    def __init__(self):

        # general
        pygame.init()
        mixer.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')
        # Main menu
        self.isOpening = True
        self.bgSurf = pygame.image.load(path.join('graphics', 'bg.jpeg'))
        # Game Over
        self.isGameOver = False
        self.game_over_animation_index = ROWS - 1
        self.isAnimatingGameOver = False
        self.game_over_animation_timer = pygame.time.get_ticks()
        # Settings window
        self.isSettings = False
        #Controls
        self.isControls = False

        # shapes
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        # Buttons setup
        self.settingsButtons = pygame.sprite.Group()


        # Labels setup
        # open window labels
        fontTitle = pygame.font.Font(path.join('graphics', 'tetrisFont.ttf'), 60)
        font = pygame.font.SysFont(path.join('graphics', 'tetrisFont.ttf'), 38)
        openWinLbl1 = Label(WINDOW_WIDTH - 3 * WINDOW_WIDTH / 4,
                            WINDOW_HEIGHT - WINDOW_HEIGHT / 4,
                            "click SPACE to start...", font,
                            effect="fade", speed=3)
        openWinLbl2 = Label(WINDOW_WIDTH - 3 * WINDOW_WIDTH / 4,
                            WINDOW_HEIGHT - 3 * WINDOW_HEIGHT / 4,
                            "TETRO SPACE", fontTitle,text_color=(0, 0, 0),bg_color=(0,0,255),
                            speed=3)
        self.openWinLabels = pygame.sprite.Group(openWinLbl1, openWinLbl2)

        # Game over labels
        GameOver1 = Label(WINDOW_WIDTH - 3 * WINDOW_WIDTH / 4,
                          WINDOW_HEIGHT - WINDOW_HEIGHT / 4,
                          "click SPACE to continue...", font,
                          effect="fade", speed=3)
        GameOver2 = Label(WINDOW_WIDTH - 3 * WINDOW_WIDTH / 4,
                          WINDOW_HEIGHT - 3 * WINDOW_HEIGHT / 4,
                          "GAME OVER", pygame.font.SysFont("freesansbold.ttf", 38),
                          speed=3)
        self.GameOverLabels = pygame.sprite.Group(GameOver1, GameOver2)

        # screen components
        self.game = Game(self.get_next_shape, self.update_score, self.GameOver)
        self.score = Score()
        self.preview = Preview()
        # music
        mixer.music.load(path.join('music', 'tetrisMetalCut.mp3'))
        mixer.music.play(-1)

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def AddButton(self, x, y, width, height, text, font, base_color, hover_color, text_color,group, command=None):
        if command:
            group.add(Button(x, y, width, height, text, font,
                                    base_color, hover_color, text_color, command))
        else:
            group.add(Button(x, y, width, height, text, font,
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isSettings = not self.isSettings


            # display
            self.display_surface.fill(GRAY)
            # opening window
            # running windows:
            keys = pygame.key.get_pressed()
            if self.isOpening:

                self.MainMenu()

                # showing open window labels
                self.openWinLabels.update()
                self.openWinLabels.draw(self.display_surface)

            else:
                if self.isAnimatingGameOver:
                    self.run_game_over_animation()
                elif self.isGameOver:
                    self.GameOverLabels.update()
                    self.GameOverLabels.draw(self.display_surface)

                    if keys[pygame.K_SPACE]:
                        pygame.quit()
                        exit()
                else:
                    if self.isSettings:
                        self.SettingsMenu()
                    else:
                        self.score.run()
                        self.game.run()
                        self.preview.run(self.next_shapes)

            # screen updating - Updates the game's screen
            pygame.display.update()
            self.clock.tick(FPS)

    def MainMenu(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.isOpening = False
            mixer.music.unload()
            mixer.music.load(path.join('music', 'tetrisTechno.mp3'))
            mixer.music.play(-1)
            return
        self.display_surface.blit(self.bgSurf, (0,0))

    def GameOver(self):
        self.isAnimatingGameOver = True
        self.isGameOver = False  # Wait until animation finishes
        self.game_over_animation_index = ROWS - 1
        self.game_over_animation_timer = pygame.time.get_ticks()

    def SettingsMenu(self):
        SettingsSurface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA).convert_alpha()
        font = pygame.font.SysFont("freesansbold.ttf", 38)
        x = WINDOW_WIDTH * 0.1
        y = WINDOW_HEIGHT - WINDOW_HEIGHT / 5
        SettingsSurface.fill((255,255,255))
        SettingsSurface.fill((0, 0, 0, 60))  # Transparent black
        self.display_surface.blit(SettingsSurface, (0, 0))

        if len(self.settingsButtons.sprites()) == 0:  # Prevents duplicates
            self.AddButton(x, y, 200, 50, "Controls", font, (0, 0, 150), (255, 0, 0),
                           (255, 255, 255), self.settingsButtons, command=self.ControlsWin)

        # Clean up redundant button code
        self.settingsButtons.draw(self.display_surface)
        self.settingsButtons.update()

    def ControlsWin(self):
        controlsSurface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        controlsRect = controlsSurface.get_rect(topright=(WINDOW_WIDTH, PADDING))
        # spacebarRect =
        # pygame.draw.rect(spacebarRect,border_radius=50)
        font = pygame.font.SysFont("freesansbold.ttf", 38)
        controlsSurface.fill(GRAY)
        self.display_surface.blit(controlsSurface, controlsRect)




        #ללמוד על שני הפעולות

    def run_game_over_animation(self):
        now = pygame.time.get_ticks()
        if now - self.game_over_animation_timer > 50:
            if self.game_over_animation_index >= 0:
                print("Clearing row", self.game_over_animation_index)
                for x in range(COLUMNS):
                    block = self.game.field_data[self.game_over_animation_index][x]
                    if isinstance(block, pygame.sprite.Sprite):
                        block.kill()
                    self.game.field_data[self.game_over_animation_index][x] = 0
                self.game_over_animation_index -= 1
                self.game_over_animation_timer = now
            else:
                self.isAnimatingGameOver = False
                self.isGameOver = True

        self.game.surface.fill(GRAY)
        self.game.sprites.update()
        self.game.sprites.draw(self.game.surface)
        self.game.draw_grid()
        self.display_surface.blit(self.game.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.game.rect, 2, 2)

    def board(self):
        for x in range(0, WINDOW_WIDTH, COLUMNS):
            for y in range(0, WINDOW_HEIGHT, ROWS):
                pygame.draw.rect(self.display_surface, 'blue', (x, y, CELL_SIZE, CELL_SIZE), 1)


if __name__ == '__main__':
    main = Main()
    main.board()
    main.run()
