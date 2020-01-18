import time
import pygame
from ship import Ship
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY, DARKGREY


class Board:
    def __init__(self, screen):
        self.phase = "placement"  # Can be placement, player_turn, opponent_turn
        self.screen = screen
        self.ships = [Ship((0, 0), (4, 0), WHITE),
                      Ship((0, 0), (3, 0), BLACK),
                      Ship((0, 0), (2, 0), BLACK),
                      Ship((0, 0), (1, 0), BLACK),
                      Ship((0, 0), (1, 0), BLACK)]

        self._opponent_guesses = []
        self._player_guesses = []

    def draw_board(self):
        self.screen.fill(DARKGREY)
        for x in range(1, 11):
            pygame.draw.line(self.screen, LIGHTGREY,
                             (SCREEN_WIDTH * x / 10, 0),
                             (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT), 1)
            pygame.draw.line(self.screen, LIGHTGREY,
                             (0, SCREEN_HEIGHT * x / 10),
                             (SCREEN_WIDTH, SCREEN_HEIGHT * x / 10), 1)
        if self.get_phase() != "player_turn":
            for ship in self.ships:
                ship.draw_ship(self.screen)

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
            pygame.draw.circle(self.screen, WHITE,
                               (int((guess[0] + 0.5) * SCREEN_WIDTH / 10), int((guess[1] + 0.5) * SCREEN_HEIGHT / 10)),
                               SCREEN_WIDTH // 40)

    def add_guess(self, guess):
        self._get_guesses().append(guess)
        for i in range(10):
            pygame.draw.circle(self.screen, WHITE,
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
        
    def move_ship(self, ship_idx, key):
        if key == pygame.K_r:
            self.ships[ship_idx].rotate()
        if key == pygame.K_UP:
            self.ships[ship_idx].translate((0, -1))
        if key == pygame.K_DOWN:
            self.ships[ship_idx].translate((0, 1))
        if key == pygame.K_LEFT:
            self.ships[ship_idx].translate((-1, 0))
        if key == pygame.K_RIGHT:
            self.ships[ship_idx].translate((1, 0))

    def place_ship(self, ship_idx):
        if not self.ships[ship_idx].check_collision(self.ships):
            self.ships[ship_idx].set_status("placed")
            if ship_idx < 4:
                self.ships[ship_idx+1].set_status("moving")
            else:
                self.set_phase("player_turn")
            return True
        return False

