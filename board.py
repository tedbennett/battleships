import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Board:

    def draw_board(self, screen):
        screen.fill(WHITE)
        for x in range(1, 11):
            pygame.draw.line(screen, BLACK, (SCREEN_WIDTH * x / 10, 0), (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT), 1)
            pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT * x / 10), (SCREEN_WIDTH, SCREEN_HEIGHT * x / 10), 1)


FPS = 30
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
running = True
while running:
    board = Board()
    board.draw_board(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()