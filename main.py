# !/usr/bin/env python3
import pygame
import pygame.freetype
from board import Board
from client import Client
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, DARKGREY


def draw_menu(surface, font):
    surface.fill(DARKGREY)
    pygame.draw.rect(surface, WHITE,
                     pygame.Rect((SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 6),
                                 (SCREEN_HEIGHT * 11 / 10 / 2) - (SCREEN_HEIGHT / 10),
                                 SCREEN_WIDTH / 3,
                                 SCREEN_HEIGHT / 5))
    text_surface, rect = font.render("START", BLACK)
    surface.blit(text_surface,
                 ((SCREEN_WIDTH / 2) - (rect.width / 2), (SCREEN_HEIGHT * 11 / 10 / 2) - (rect.height / 2)))


if __name__ == "__main__":
    FPS = 30
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, int(SCREEN_HEIGHT * 11 / 10)))
    font = pygame.freetype.SysFont("Courier", 24)
    pygame.display.set_caption("Battleship")
    running = True
    board = None
    client = None
    ship_index = 1
    while running:
        if board:
            board.draw_board()
        else:
            draw_menu(screen, font)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not board:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and (
                            (SCREEN_HEIGHT / 2) - (SCREEN_HEIGHT / 10) <= event.pos[0]
                            < (SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 10)
                            and (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 6)
                            <= event.pos[1] < (SCREEN_WIDTH / 2) + (SCREEN_WIDTH / 6)):
                        board = Board(screen, font)
                        client = Client(board)
            if board:
                if event.type == pygame.MOUSEBUTTONDOWN and board.get_phase() == "player turn":
                    # Send guess if valid
                    if event.button == 1:
                        x, y = int(event.pos[0] / (SCREEN_WIDTH / 10)), int(event.pos[1] / (SCREEN_HEIGHT / 10))
                        if y > 0 and board.valid_guess((x, y)):
                            client.send("MOVE,{},{}".format(x, y))
                elif event.type == pygame.KEYDOWN and board.get_phase() == "placement":
                    if event.key != pygame.K_RETURN:
                        board.move_ship(str(ship_index), event.key)
                    else:
                        if board.place_ship(ship_index):
                            if ship_index < 2:
                                ship_index += 1
                            else:
                                client.send("READY")
                elif event.type == pygame.MOUSEBUTTONDOWN and board.get_phase() == "end":
                    if event.button == 1 and (
                            (SCREEN_HEIGHT / 2) - (SCREEN_HEIGHT / 10) <= event.pos[0]
                            < (SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 10)
                            and (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 6)
                            <= event.pos[1] < (SCREEN_WIDTH / 2) + (SCREEN_WIDTH / 6)):
                        client.close()
                        client = None
                        board = None

    pygame.quit()
