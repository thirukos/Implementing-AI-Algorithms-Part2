# reference: 
# https://pythonguides.com/create-a-game-using-python-pygame/
import pygame
import numpy as np
import pygame, sys

class TicTacToeGame:
    def __init__(self, screen_size=(600, 600)):
        # Calculate the scaling factor based on the default screen size (600x600)
        scaling_factor = min(screen_size[0] / 600, screen_size[1] / 600)
        self.screen_size = screen_size
        self.board_rows = 3
        self.board_cols = 3
        self.square_size = int(200 * scaling_factor)
        self.width = int(600 * scaling_factor)
        self.height = int(600 * scaling_factor)
        self.line_width = int(15 * scaling_factor)
        self.win_line_width = int(10 * scaling_factor)
        self.circle_radius = int(60 * scaling_factor)
        self.circle_width = int(15 * scaling_factor)
        self.cross_width = int(25 * scaling_factor)
        self.space = int(55 * scaling_factor)
        self.bg_color = (247, 249, 249)
        self.line_color = (28, 40, 51)
        self.circle_color = (23, 32, 42)
        self.cross_color = (23, 32, 42)
        self.board = np.zeros((self.board_rows, self.board_cols))
        self.player = 1
        self.game_over = False
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('TIC TAC TOE')
        self.screen.fill(self.bg_color)
        self.draw_lines()

    def draw_lines(self):
        pygame.draw.line(self.screen, self.line_color, (0, self.square_size), (self.width, self.square_size), self.line_width)
        pygame.draw.line(self.screen, self.line_color, (0, 2 * self.square_size), (self.width, 2 * self.square_size), self.line_width)
        pygame.draw.line(self.screen, self.line_color, (self.square_size, 0), (self.square_size, self.height), self.line_width)
        pygame.draw.line(self.screen, self.line_color, (2 * self.square_size, 0), (2 * self.square_size, self.height), self.line_width)

    def draw_figures(self):
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, self.circle_color, (int(col * self.square_size + self.square_size//2), int(row * self.square_size + self.square_size//2)), self.circle_radius, self.circle_width)
                elif self.board[row][col] == 2:
                    pygame.draw.line(self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.square_size - self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.space), self.cross_width)  
                    pygame.draw.line(self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.square_size - self.space), self.cross_width)

    def mark_square(self, row, col):
        self.board[row][col] = self.player

    def available_square(self, row, col):
        return self.board[row][col] == 0

    def is_board_full(self):
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == 0:
                    return False
        return True

    def check_win(self):
        for col in range(self.board_cols):
            if self.board[0][col] == self.player and self.board[1][col] == self.player and self.board[2][col] == self.player:
                self.draw_vertical_winning_line(col)
                self.game_over = True
                return True

        for row in range(self.board_rows):
            if self.board[row][0] == self.player and self.board[row][1] == self.player and self.board[row][2] == self.player:
                self.draw_horizontal_winning_line(row)
                self.game_over = True
                return True

        if self.board[2][0] == self.player and self.board[1][1] == self.player and self.board[0][2] == self.player:
            self.draw_asc_diagonal()
            self.game_over = True
            return True

        if self.board[0][0] == self.player and self.board[1][1] == self.player and self.board[2][2] == self.player:
            self.draw_desc_diagonal()
            self.game_over = True
            return True

        return False

    def draw_vertical_winning_line(self, col):
        pos_x = col * self.square_size + self.square_size//2

        if self.player == 1:
            color = self.circle_color
        elif self.player == 2:
            color = self.cross_color

        pygame.draw.line(self.screen, color, (pos_x, 15), (pos_x, self.height - 15), self.line_width)

    def draw_horizontal_winning_line(self, row):
        pos_y = row * self.square_size + self.square_size//2

        if self.player == 1:
            color = self.circle_color
        elif self.player == 2:
            color = self.cross_color

        pygame.draw.line(self.screen, color, (15, pos_y), (self.width - 15, pos_y), self.win_line_width)

    def draw_asc_diagonal(self):
        if self.player == 1:
            color = self.circle_color
        elif self.player == 2:
            color = self.cross_color

        pygame.draw.line(self.screen, color, (15, self.height - 15), (self.width - 15, 15), self.win_line_width)

    def draw_desc_diagonal(self):
        if self.player == 1:
            color = self.circle_color
        elif self.player == 2:
            color = self.cross_color

        pygame.draw.line(self.screen, color, (15, 15), (self.width - 15, self.height - 15), self.win_line_width)

    def restart(self):
        self.screen.fill(self.bg_color)
        self.draw_lines()
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                self.board[row][col] = 0
        self.player = 1
        self.game_over = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:

                    mouse_x = event.pos[0] 
                    mouse_y = event.pos[1] 

                    clicked_row = int(mouse_y // self.square_size)
                    clicked_col = int(mouse_x // self.square_size)

                    if self.available_square(clicked_row, clicked_col):

                        self.mark_square(clicked_row, clicked_col)
                        if self.check_win():
                            self.game_over = True
                        self.player = self.player % 2 + 1

                        self.draw_figures()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                        self.game_over = False

            pygame.display.update()

               
# def main():
#     pygame.init()
#     screen_size = (400, 400)
#     game = TicTacToeGame(screen_size)
#     game.run()

# if __name__ == '__main__':
#     main()
