# !/usr/bin/env python3
import pygame
from board import Board
from client import Client
from constant import SCREEN_WIDTH, SCREEN_HEIGHT

if __name__ == "__main__":
    FPS = 30
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battleship")
    running = True
    board = Board(screen)
    client = Client(board)
    ship_index = 0
    while running:
        board.draw_board()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and board.get_phase() == "player turn":
                if event.button == 1:
                    x, y = int(event.pos[0] / (SCREEN_WIDTH / 10)), int(event.pos[1] / (SCREEN_HEIGHT / 10))
                    if board.valid_guess((x,y)):
                        board.guess((x,y))
                        client.send("MOVE,{},{}".format(x, y))
            elif event.type == pygame.KEYDOWN and board.get_phase() == "placement":
                if event.key != pygame.K_RETURN:
                    board.move_ship(ship_index, event.key)
                else:
                    if board.place_ship(ship_index):
                        if ship_index < 1:
                            ship_index += 1
                        else:
                            client.send("READY")
            elif event.type == pygame.MOUSEBUTTONDOWN and board.get_phase() == "menu":
                if event.button == 1 and (
                        (SCREEN_HEIGHT / 2) - (SCREEN_HEIGHT / 10) <= event.pos[0]
                        < (SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 10)
                        and (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 6)
                        <= event.pos[1] < (SCREEN_WIDTH / 2) + (SCREEN_WIDTH / 6)):
                    board.set_phase("placement")
    pygame.quit()
