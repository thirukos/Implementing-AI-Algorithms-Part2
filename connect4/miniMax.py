import numpy as np
import pygame
import sys
import math
from connectFour import ConnectFour

class ConnectFourBot(ConnectFour):
    def __init__(self):
        super().__init__()

    def get_bot_move(self):
        for col in range(self.COLUMN_COUNT):
            row = self.get_next_open_row(col)
            if self.is_valid_location(col):
                self.drop_piece(row, col, 2)
                if self.winning_move(2):
                    return col
                self.drop_piece(row, col, 0)
        
        for col in range(self.COLUMN_COUNT):
            row = self.get_next_open_row(col)
            if self.is_valid_location(col):
                self.drop_piece(row, col, 1)
                if self.winning_move(1):
                    self.drop_piece(row, col, 0)
                    return col
                self.drop_piece(row, col, 0)

        return np.random.choice(np.where(self.board[0] == 0)[0])

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
                if event.type == pygame.MOUSEBUTTONDOWN and self.turn == 0:
                    pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.SQUARESIZE))
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
                        continue
                else:
                    col = self.get_bot_move()

                    if self.is_valid_location(col):
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, 2)

                        if self.winning_move(2):
                            label = self.myfont.render("Bot wins!!", 1, self.player2_color)
                            self.screen.blit(label, (40,10))
                            self.game_over = True

                self.print_board()
                self.draw_board()
                self.turn += 1
                self.turn = self.turn % 2

                if self.game_over:
                    pygame.time.wait(3000)
