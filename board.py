import pygame
from ship import Ship
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY, DARKGREY


class Board:
    def draw_board(self, screen, ships):
        screen.fill(DARKGREY)
        for x in range(1, 11):
            pygame.draw.line(screen, LIGHTGREY,
                             (SCREEN_WIDTH * x / 10, 0),
                             (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT), 1)
            pygame.draw.line(screen, LIGHTGREY,
                             (0, SCREEN_HEIGHT * x / 10),
                             (SCREEN_WIDTH, SCREEN_HEIGHT * x / 10), 1)
        for ship in ships:
            ship.draw_ship(screen)


FPS = 30
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship")
running = True
board = Board()
ships = [Ship((0, 0), (5, 0), WHITE),
         Ship((0, 0), (4, 0), BLACK),
         Ship((0, 0), (3, 0), BLACK),
         Ship((0, 0), (3, 0), BLACK),
         Ship((0, 0), (2, 0), BLACK)]
ship_index = 0
movement_phase = True
while running:
    board.draw_board(screen, ships)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and movement_phase:
            if event.key == pygame.K_r:
                ships[ship_index].rotate()
            if event.key == pygame.K_UP:
                ships[ship_index].translate((0, -1))
            if event.key == pygame.K_DOWN:
                ships[ship_index].translate((0, 1))
            if event.key == pygame.K_LEFT:
                ships[ship_index].translate((-1, 0))
            if event.key == pygame.K_RIGHT:
                ships[ship_index].translate((1, 0))
            if event.key == pygame.K_RETURN:
                if not ships[ship_index].check_collision(ships):
                    ships[ship_index].set_phase("placed")
                    if ship_index < 4:
                        ship_index += 1
                        ships[ship_index].set_phase("moving")
                    else:
                        movement_phase = False
pygame.quit()
