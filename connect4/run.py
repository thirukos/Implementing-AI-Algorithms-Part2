import pygame
from connectFour import ConnectFour # connect 4 game class


if __name__ == '__main__':
    pygame.init()
    game = ConnectFour()
    game.draw_board()
    game.run_game()
    pygame.quit()