# !/usr/bin/env python3
import time

import pygame
from ship import Ship
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY, DARKGREY, RED


class Board:
    def __init__(self, screen):
        self.phase = "menu"  # Can be menu, placement, waiting, player turn, opponent turn
        self._screen = screen
        self._ships = [Ship((0, 0), (4, 0), WHITE),
                       Ship((0, 0), (3, 0), BLACK)]
                       # Ship((0, 0), (2, 0), BLACK),
                       # Ship((0, 0), (1, 0), BLACK),
                       # Ship((0, 0), (1, 0), BLACK)]

        self._ship_tiles = None
        self._opponent_guesses = self._init_guesses()
        self._player_guesses = self._init_guesses()
        self._opponent_ships = []
        self._last_guess = None
        self._player_name = None
        self._game_ready = False

    def _init_guesses(self):
        guesses = {}
        for idx in range(len(self._ships)):
            guesses[idx] = []
        guesses["miss"] = []
        return guesses

    def _init_tiles(self):
        tiles = {}
        for idx, ship in enumerate(self._ships):
            tiles[idx] = ship.get_array()
        return tiles

    def draw_board(self):
        self._screen.fill(DARKGREY)
        if self.get_phase() != "menu":
            for x in range(1, 11):
                pygame.draw.line(self._screen, LIGHTGREY,
                                 (SCREEN_WIDTH * x / 10, 0),
                                 (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT), 1)
                pygame.draw.line(self._screen, LIGHTGREY,
                                 (0, SCREEN_HEIGHT * x / 10),
                                 (SCREEN_WIDTH, SCREEN_HEIGHT * x / 10), 1)
            if self.get_phase() == "player turn":
                self._draw_guesses()
                self._draw_opponent_ships()

            elif self.get_phase() == "opponent turn":
                self.draw_ships()
                self._draw_guesses()

            elif self.get_phase() == "placement":
                self.draw_ships()
            elif self.get_phase() == "waiting":
                pygame.draw.rect(self._screen, WHITE,
                                 pygame.Rect((SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 6),
                                             (SCREEN_HEIGHT / 2) - (SCREEN_HEIGHT / 10),
                                             SCREEN_WIDTH / 3,
                                             SCREEN_HEIGHT / 5))

        else:
            pygame.draw.rect(self._screen, WHITE,
                             pygame.Rect((SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 6),
                                         (SCREEN_HEIGHT / 2) - (SCREEN_HEIGHT / 10),
                                         SCREEN_WIDTH / 3,
                                         SCREEN_HEIGHT / 5))

    def get_phase(self):
        return self.phase

    def set_phase(self, phase):
        self.phase = phase

    def valid_guess(self, guess):
        return guess not in self._get_guesses()

    def _get_guesses(self):
        if self.get_phase() == "opponent turn":
            return self._opponent_guesses
        elif self.get_phase() == "player turn":
            return self._player_guesses

    def _draw_guesses(self):
        for guess, value in self._get_guesses().items():
            colour = RED if value == "HIT" else WHITE
            pygame.draw.circle(self._screen, colour,
                               (int((guess[0] + 0.5) * SCREEN_WIDTH / 10), int((guess[1] + 0.5) * SCREEN_HEIGHT / 10)),
                               SCREEN_WIDTH // 40)

    def draw_ships(self):
        for ship in self._ships:
            ship.draw_ship(self._screen)

    def _draw_opponent_ships(self):
        for ship in self._opponent_ships:
            ship.draw_ship(self._screen)

    def change_turn(self):
        print("changing turn")
        if self.get_phase() == "opponent turn":
            self.set_phase("player turn")
        elif self.get_phase() == "player turn":
            self.set_phase("opponent turn")
        else:
            return

    def move_ship(self, ship_idx, key):
        if key == pygame.K_r:
            self._ships[ship_idx].rotate()
        if key == pygame.K_UP:
            self._ships[ship_idx].translate((0, -1))
        if key == pygame.K_DOWN:
            self._ships[ship_idx].translate((0, 1))
        if key == pygame.K_LEFT:
            self._ships[ship_idx].translate((-1, 0))
        if key == pygame.K_RIGHT:
            self._ships[ship_idx].translate((1, 0))

    def place_ship(self, ship_idx):
        if not self._ships[ship_idx].check_collision(self._ships):
            self._ships[ship_idx].set_status("placed")
            if ship_idx < 1:
                self._ships[ship_idx + 1].set_status("moving")
            else:
                self.set_phase("player turn")
            return True
        return False

    def guess(self, guess):
        self._last_guess = guess

    def process_guess(self, message):
        guess = (int(message[0]), int(message[1]))
        if guess in self._ship_tiles:
            response = "HIT"
        else:
            response = "MISS"
        self._opponent_guesses[guess] = response
        return response

    def process_response(self, message):
        self._player_guesses[self._last_guess] = message

    def process_join(self, name):
        self._player_name = name

    def process_exit(self, name):
        print("Player {} has left the game".format(name))
        self.set_phase("menu")

    def process_ready(self, name):
        if self._game_ready:
            self._ship_tiles = self._init_tiles()
            if self._player_name == '1':
                self.set_phase("player turn")
            else:
                self.set_phase("opponent turn")
        elif name == self._player_name:
            self.set_phase("waiting")
        self._game_ready = True
