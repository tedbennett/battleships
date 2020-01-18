import pygame
from ship import Ship
from board import Board
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


if __name__ == "__main__":
    FPS = 30
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battleship")
    running = True
    board = Board(screen)
    ship_index = 0
    while running:
        board.draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and board.get_phase() == "placement":
                if event.key != pygame.K_RETURN:
                    board.move_ship(ship_index, event.key)
                else:
                    if board.place_ship(ship_index):
                        ship_index += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and board.get_phase() != "placement":
                if event.button == 1:
                    pass
                    # guess = int(event.pos[0] / (SCREEN_WIDTH / 10)), int(event.pos[1] / (SCREEN_HEIGHT / 10))
                    # if board.valid_guess(guess):
                    # board.add_guess(guess)
    pygame.quit()
