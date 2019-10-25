import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (100,100,100)
DARKGREY = (50, 50, 50)


class Board:

    def draw_board(self, screen, pieces):
        screen.fill(DARKGREY)
        for x in range(1, 11):
            pygame.draw.line(screen, LIGHTGREY, (SCREEN_WIDTH * x / 10, 0), (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT), 1)
            pygame.draw.line(screen, LIGHTGREY, (0, SCREEN_HEIGHT * x / 10), (SCREEN_WIDTH, SCREEN_HEIGHT * x / 10), 1)

        for piece in pieces:
            pygame.draw.rect(screen, WHITE, piece.get_rect())


class Piece:

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._rect = pygame.Rect(self._x * SCREEN_WIDTH / 10, self._y * SCREEN_HEIGHT / 10, SCREEN_WIDTH / 10, SCREEN_HEIGHT / 10)

    def get_rect(self):
        return self._rect

    def get_pos(self):
        return self._x, self._y


FPS = 30
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship")
running = True
pieces = []
board = Board()
pieces.append(Piece(1, 1))
pieces.append(Piece(5, 4))
while running:
    board.draw_board(screen, pieces)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
