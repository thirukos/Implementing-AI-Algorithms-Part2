# # reference:
# # https://github.com/KeithGalli/Connect4-Python
import numpy as np
import pygame
import sys
import math

class ConnectFour:
    def __init__(self):
        self.board_color = (0,0,255)
        self.background_color = (0,0,0)
        self.player1_color = (255,0,0)
        self.player2_color = (255,255,0)
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.SQUARESIZE = 80
        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT+1) * self.SQUARESIZE
        self.RADIUS = int(self.SQUARESIZE/2 - 5)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('CONNECT 4')
        self.board = self.create_board()
        self.myfont = pygame.font.SysFont("monospace", 25)
        self.game_over = False
        self.turn = 0

    def create_board(self):
        board = np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))
        return board

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT-1][col] == 0
    
    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r
        return -1
            
    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal
        for r in range(self.ROW_COUNT):
            for c in range(self.COLUMN_COUNT-3):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check diagonal (positive slope)
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check diagonal (negative slope)
        for r in range(3, self.ROW_COUNT):
            for c in range(self.COLUMN_COUNT-3):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

        return False

    def draw_board(self):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, self.board_color, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.background_color, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.player1_color, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.player2_color, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()

    def run_game(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == 0:
                        pygame.draw.circle(self.screen, self.player1_color, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                    else:
                        pygame.draw.circle(self.screen, self.player2_color, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.SQUARESIZE))
                    if self.turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, 1)

                            if self.winning_move(1):
                                label = self.myfont.render("Player 1 wins!!", 1, self.player1_color)
                                self.screen.blit(label, (40,10))
                                self.game_over = True
                    else:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))
                        if self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, 2)

                            if self.winning_move(2):
                                label = self.myfont.render("Player 2 wins!!", 1, self.player2_color)
                                self.screen.blit(label, (40,10))
                                self.game_over = True
                    self.print_board()
                    self.draw_board()
                    self.turn += 1
                    self.turn = self.turn % 2
                    if self.game_over:
                        pygame.time.wait(3000)
