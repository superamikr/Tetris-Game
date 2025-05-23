import random

from template import *
from timer import Timer


class Game(Template):
    def __init__(self, get_next_shape,update_score):
        super().__init__()
        # General
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft=(PADDING, PADDING))


        # game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        # the-lines
        self.line_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        self.line_surface.fill((0, 255, 0, 120))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(120)

        # test Block
        self.sprites = pygame.sprite.Group()
        # self.block = Block(self.sprites, (4, 6), 'red')

        # Tetromino         #inner loop                 #outer loop
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        # Expression            #doing every time the Expression
        self.tetromino = Tetromino(
            random.choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

        # timer
        self.down_speed = UPDATE_START_SPEED
        self.faster_down_speed = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

        # Score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines]*self.current_level

        # every 10 lines += level by 1
        if self.current_lines/10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.faster_down_speed = self.down_speed * 0.3
            self.timers['vertical move'] = self.down_speed
        self.update_score(self.current_lines,self.current_score,self.current_level)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    # creating new tetromino
    def create_new_tetromino(self):
        self.check_full_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino, self.field_data
        )

    def move_down(self):
        self.tetromino.move_down()

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        # horizontal movement
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()
            # faster vertical movement
            if not self.down_pressed and (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                self.down_pressed = True
                self.timers['vertical move'].duration = self.faster_down_speed
            if self.down_pressed and not (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                self.down_pressed = False
                self.timers['vertical move'].duration = self.down_speed

        # rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_SPACE]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

    def check_full_rows(self):
        # get full row indexes
        delete_rows = []
        # returns a tuple with (i,item) of each row in field_data
        for i, row in enumerate(self.field_data):
            # "all" func returns if all the value-items in field_data
            # are true in the specific row: [1,1,1,1,1,1,1]  - means the row is full of the blocks
            if all(row):
                delete_rows.append(i)
        if delete_rows:
            for delete_row in delete_rows:

                # deletes full rows
                for block in self.field_data[delete_row]:
                    # "kills" the block sprite in the specific row,x
                    if isinstance(block, Block):
                        block.kill()
                # move down the blocks
                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1
            # rebuild the field data
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            # update score
            self.calculate_score(len(delete_rows))

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (x, 0), (x, self.surface.get_height()), 1)
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.surface, LINE_COLOR, (0, y), (self.surface.get_width(), y), 1)
        self.surface.blit(self.line_surface, (0, 0))

    def run(self):

        # update
        self.input()

        self.timer_update()
        self.sprites.update()

        # drawing
        self.surface.fill(GRAY)
        self.sprites.draw(self.surface)

        self.sprites.update()
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLOR, self.rect, 2, 2)


class Tetromino:
    def __init__(self, shape, sprite_group, create_new_tetromino, field_data):
        # setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.sprite_group = sprite_group
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data
        # create blocks
        self.blocks = [Block(self.sprite_group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in self.blocks]
        return True if any(collision_list) else False

    # movement
    # def faster_down_move(self):
    #     if not self.next_move_vertical_collide(self.blocks, 1):
    #         for block in self.blocks:
    #             block.pos.y += 1
    def move_down(self):
        if not self.next_move_vertical_collide(1):
            for block in self.blocks:
                block.pos.y += 1
        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()
            for row in self.field_data:
                print(row)

    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(amount):
            for block in self.blocks:
                block.pos.x += amount

    def rotate(self):
        if self.shape != '0':  # Assuming '0' is the O-block (square)
            pivot_pos = self.blocks[0].pos
            new_block_position = [block.rotate(pivot_pos) for block in self.blocks]

            for pos in new_block_position:
                # Horizontal bounds check
                if pos.x < 0 or pos.x >= COLUMNS:
                    return
                # Vertical bounds check
                if pos.y < 0 or pos.y >= ROWS:
                    return
                # Collision with other blocks
                if self.field_data[int(pos.y)][int(pos.x)]:
                    return

            # Apply new positions
            for i, block in enumerate(self.blocks):
                block.pos = new_block_position[i]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)

        # general
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # positions
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft=self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        return pivot_pos + (self.pos - pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS:
            return True
        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect = self.pos * CELL_SIZE
