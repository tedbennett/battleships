import time

import pygame
from ship import Ship
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY, DARKGREY
from client import Client

class Board:
    def __init__(self):
        self.phase = "player_turn"  # Can be placement, own_turn, opponent_turn
        self._opponent_guesses = []
        self._player_guesses = []

    def draw_board(self, screen, ships):
        screen.fill(DARKGREY)
        for x in range(1, 11):
            pygame.draw.line(screen, LIGHTGREY,
                             (SCREEN_WIDTH * x / 10, 0),
                             (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT), 1)
            pygame.draw.line(screen, LIGHTGREY,
                             (0, SCREEN_HEIGHT * x / 10),
                             (SCREEN_WIDTH, SCREEN_HEIGHT * x / 10), 1)
        if self.get_phase() != "player_turn":
            for ship in ships:
                ship.draw_ship(screen)
        # if self._get_guesses():
        #     self.draw_guesses()

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase

    def valid_guess(self, guess):
        return guess not in self._get_guesses()

    def _get_guesses(self):
        if self.get_phase() == "opponent_turn":
            return self._opponent_guesses
        elif self.get_phase() == "player_turn":
            return self._player_guesses

    def draw_guesses(self):
        for guess in self._get_guesses():
            pygame.draw.circle(screen, WHITE,
                               (int((guess[0]+0.5) * SCREEN_WIDTH / 10), int((guess[1]+0.5) * SCREEN_HEIGHT / 10)),
                               SCREEN_WIDTH // 40)

    def add_guess(self, guess):
        self._get_guesses().append(guess)
        for i in range(10):
            pygame.draw.circle(screen, WHITE,
                               (int((guess[0] + 0.5) * SCREEN_WIDTH / 10), int((guess[1] + 0.5) * SCREEN_HEIGHT / 10)),
                               SCREEN_WIDTH // 40)
            pygame.display.flip()
        time.sleep(1)

    def change_turn(self):
        print("changing turn")
        if self.get_phase() == "opponent_turn":
            self.set_phase("player_turn")
            pygame.display.set_caption("Battleship - Player Turn")
        elif self.get_phase() == "player_turn":
            self.set_phase("opponent_turn")
            pygame.display.set_caption("Battleship - Opponent's Turn")
        else:
            return


FPS = 30
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship")
running = True
board = Board()
client = Client(board)
ships = [Ship((0, 0), (4, 0), WHITE),
         Ship((0, 0), (3, 0), BLACK),
         Ship((0, 0), (2, 0), BLACK),
         Ship((0, 0), (1, 0), BLACK),
         Ship((0, 0), (1, 0), BLACK)]
ship_index = 0
while running:
    board.draw_board(screen, ships)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and board.get_phase() == "placement":
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
                    ships[ship_index].set_status("placed")
                    if ship_index < 4:
                        ship_index += 1
                        ships[ship_index].set_status("moving")
                    else:
                        board.set_phase("player_turn")
        elif event.type == pygame.MOUSEBUTTONDOWN and board.get_phase() != "placement":
            if event.button == 1:
                # guess = int(event.pos[0] / (SCREEN_WIDTH / 10)), int(event.pos[1] / (SCREEN_HEIGHT / 10))
                # if board.valid_guess(guess):
                    # board.add_guess(guess)
                board.change_turn()
                client.send("end of turn")


pygame.quit()
