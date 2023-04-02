# reference: 
# https://pythonguides.com/create-a-game-using-python-pygame/
import pygame
import numpy as np
import pygame, sys
import random

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
        self.draw_figures()
        pygame.display.update()
        pygame.time.wait(3000)
        self.screen.fill(self.bg_color)
        self.draw_lines()
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                self.board[row][col] = 0
        self.player = 1
        self.game_over = False

    def get_available_moves(self):
        moves = []
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == 0:
                    moves.append((row, col))
        return moves

    def tictactoe_Bot(self):
        bot_symbol = self.player  # player 2 is the bot in this implementation
        human_symbol = self.player % 2 + 1  # player 1 is the human player in this implementation
        # try to make a winning move horizontally
        for row in range(self.board_rows):
            bot_moves = 0
            empty_col = None
            for col in range(self.board_cols):
                if self.board[row][col] == bot_symbol:
                    bot_moves += 1
                elif self.board[row][col] == 0:
                    empty_col = col
            if bot_moves == self.board_cols - 1 and empty_col is not None:
                self.board[row][empty_col] = bot_symbol
                return row, empty_col

        # try to make a winning move vertically
        for col in range(self.board_cols):
            bot_moves = 0
            empty_row = None
            for row in range(self.board_rows):
                if self.board[row][col] == bot_symbol:
                    bot_moves += 1
                elif self.board[row][col] == 0:
                    empty_row = row
            if bot_moves == self.board_rows - 1 and empty_row is not None:
                self.board[empty_row][col] = bot_symbol
                return empty_row, col

        # try to make a winning move diagonally
        if self.board[0][0] == bot_symbol and self.board[1][1] == bot_symbol and self.available_square(2, 2):
            self.board[2][2] = bot_symbol
            return 2, 2
        elif self.board[0][0] == bot_symbol and self.board[2][2] == bot_symbol and self.available_square(1, 1):
            self.board[1][1] = bot_symbol
            return 1, 1
        elif self.board[1][1] == bot_symbol and self.board[2][2] == bot_symbol and self.available_square(0, 0):
            self.board[0][0] = bot_symbol
            return 0, 0
        elif self.board[0][2] == bot_symbol and self.board[1][1] == bot_symbol and self.available_square(2, 0):
            self.board[2][0] = bot_symbol
            return 2, 0
        elif self.board[0][2] == bot_symbol and self.board[2][0] == bot_symbol and self.available_square(1, 1):
            self.board[1][1] = bot_symbol
            return 1, 1
        elif self.board[1][1] == bot_symbol and self.board[2][0] == bot_symbol and self.available_square(0, 2):
            self.board[0][2] = bot_symbol
            return 0, 2

        # try to block opponent from winning horizontally
        for row in range(self.board_rows):
            human_moves = 0
            empty_col = None
            for col in range(self.board_cols):
                if self.board[row][col] == human_symbol:
                    human_moves += 1
                elif self.board[row][col] == 0:
                    empty_col = col
            if human_moves == self.board_cols - 1 and empty_col is not None:
                self.board[row][empty_col] = bot_symbol
                return row, empty_col

        # try to block opponent from winning vertically
        for col in range(self.board_cols):
            human_moves = 0
            empty_row = None
            for row in range(self.board_rows):
                if self.board[row][col] == human_symbol:
                    human_moves += 1
                elif self.board[row][col] == 0:
                    empty_row = row
            if human_moves == self.board_rows - 1 and empty_row is not None:
                self.board[empty_row][col] = bot_symbol
                return empty_row, col

        # try to block opponent from winning diagonally
        if self.board[0][0] == human_symbol and self.board[1][1] == human_symbol and self.available_square(2, 2):
            self.board[2][2] = bot_symbol
            return 2, 2
        elif self.board[0][0] == human_symbol and self.board[2][2] == human_symbol and self.available_square(1, 1):
            self.board[1][1] = bot_symbol
            return 1, 1
        elif self.board[1][1] == human_symbol and self.board[2][2] == human_symbol and self.available_square(0, 0):
            self.board[0][0] = bot_symbol
            return 0, 0
        elif self.board[0][2] == human_symbol and self.board[1][1] == human_symbol and self.available_square(2, 0):
            self.board[2][0] = bot_symbol
            return 2, 0
        elif self.board[0][2] == human_symbol and self.board[2][0] == human_symbol and self.available_square(1, 1):
            self.board[1][1] = bot_symbol
            return 1, 1
        elif self.board[1][1] == human_symbol and self.board[2][0] == human_symbol and self.available_square(0, 2):
            self.board[0][2] = bot_symbol
            return 0, 2
        
        # prioritize center, corners, and then edges
        # if self.available_square(1, 1):
        #     row, col = 1, 1
        # elif self.available_square(0, 0):
        #     row, col = 0, 0
        # elif self.available_square(0, 2):
        #     row, col = 0, 2
        # elif self.available_square(2, 0):
        #     row, col = 2, 0
        # elif self.available_square(2, 2):
        #     row, col = 2, 2
        # elif self.available_square(0, 1):
        #     row, col = 0, 1
        # elif self.available_square(1, 0):
        #     row, col = 1, 0
        # elif self.available_square(1, 2):
        #     row, col = 1, 2
        # elif self.available_square(2, 1):
        #     row, col = 2, 1
        else:
        # make a random move
            row, col = random.randint(0, self.board_rows-1), random.randint(0, self.board_cols-1)
            while not self.available_square(row, col):
                row, col = random.randint(0, self.board_rows-1), random.randint(0, self.board_cols-1)
        
        self.board[row][col] = bot_symbol
        return row, col
        
    def minimax(self, board, depth, maximizing_player, alpha, beta):
        best_row = -1
        best_col = -1
        if maximizing_player:
            best_score = -float("inf")
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = 2
                        score, _, _ = self.minimax(board, depth+1, False, alpha, beta)
                        board[row][col] = 0
                        if score > best_score:
                            best_score = score
                            best_row, best_col = row, col
                        alpha = max(alpha, best_score)
                        if alpha >= beta:
                            break
            return best_score, best_row, best_col

        else:
            best_score = float("inf")
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        score, _, _ = self.minimax(board, depth+1, True, alpha, beta)
                        board[row][col] = 0
                        if score < best_score:
                            best_score = score
                            best_row, best_col = row, col
                        beta = min(beta, best_score)
                        if alpha >= beta:
                            break
            return best_score, best_row, best_col

    def run(self, mode="P2P"):
        if mode == "P2B":
            while not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if self.player == 1:
                        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                            mouse_x = event.pos[0] 
                            mouse_y = event.pos[1] 

                            clicked_row = int(mouse_y // self.square_size)
                            clicked_col = int(mouse_x // self.square_size)

                            if self.available_square(clicked_row, clicked_col):
                                self.mark_square(clicked_row, clicked_col)
                                if self.check_win():
                                    self.game_over = True
                                elif self.is_board_full():
                                    self.restart()
                                self.player = self.player % 2 + 1
                                self.draw_figures()


                    elif self.player == 2:
                        row, col = self.tictactoe_Bot()
                        self.mark_square(row, col)
                        if self.check_win():
                            self.game_over = True
                        elif self.is_board_full():
                            self.restart()
                        self.player = self.player % 2 + 1
                        self.draw_figures()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart()
                            self.game_over = False

                pygame.display.update()
                if self.game_over:
                    pygame.time.wait(2000)

        elif mode == "B2MiniMax":
            while not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if self.player == 1:
                        row, col = self.tictactoe_Bot() 
                        self.mark_square(row, col)
                        if self.check_win():
                            self.game_over = True
                        elif self.is_board_full():
                            self.restart()
                        self.player = self.player % 2 + 1
                        self.draw_figures()
                        pygame.time.wait(2000)
                        
                    elif self.player == 2:
                        alpha = -float("inf")
                        beta = float("inf")
                        _, row, col = self.minimax(self.board, depth=0, maximizing_player = False, alpha = alpha, beta = beta)
                        self.mark_square(row, col)
                        if self.check_win():
                            self.game_over = True
                        elif self.is_board_full():
                            self.restart()
                        self.player = self.player % 2 + 1
                        self.draw_figures()
                        pygame.time.wait(2000)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart()
                            self.game_over = False
                pygame.display.update()
                if self.game_over:
                    pygame.time.wait(3000)

        elif mode == "B2QLearning":
            pass

        else:
            while not self.game_over:
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
                            elif self.is_board_full():
                                self.restart()
                            self.player = self.player % 2 + 1
                            self.draw_figures()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart()
                            self.game_over = False

                pygame.display.update()
                if self.game_over:
                    pygame.time.wait(3000)

               
def main():
    pygame.init()
    screen_size = (400, 400)
    game = TicTacToeGame(screen_size)
    #P2B
    #B2MiniMax 

    game.run(mode = "B2MiniMax")

if __name__ == '__main__':
    main()
