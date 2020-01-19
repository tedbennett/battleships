# !/usr/bin/env python3
import time

import pygame
from ship import Ship
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY, DARKGREY, RED, PINK


class Board:
    def __init__(self, screen):
        self.phase = "menu"  # Can be menu, placement, waiting, player turn, opponent turn
        self._screen = screen
        self._player_ships = {'1': Ship((0, 0), (4, 0), WHITE),
                              '2': Ship((0, 0), (3, 0), BLACK)}
        # Ship((0, 0), (2, 0), BLACK),
        # Ship((0, 0), (1, 0), BLACK),
        # Ship((0, 0), (1, 0), BLACK)]

        self._valid_guesses = {}
        self._opponent_guesses = self._init_guesses()
        self._player_guesses = self._init_guesses()
        self._opponent_ships = {}
        self._last_guess = None
        self._player_name = None
        self._game_ready = False

    def _init_guesses(self):
        guesses = {}
        for idx in self._player_ships:
            guesses[idx] = []
        guesses["miss"] = []
        return guesses

    def _init_tiles(self):
        tiles = {}
        for idx, ship in self._player_ships.items():
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
            elif self.get_phase() == "waiting": # need to redo this
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
        # check if guess has already been made. Search all hit and miss containers.
        for ship in self._get_guesses().values():
            if guess in ship:
                return False
        return True

    def _get_guesses(self):
        if self.get_phase() == "opponent turn":
            return self._opponent_guesses
        elif self.get_phase() == "player turn":
            return self._player_guesses

    def _draw_guesses(self):
        for name, guesses in self._get_guesses().items():
            if name != "miss":
                colour = RED
            else:
                colour = WHITE
            for guess in guesses:
                pygame.draw.circle(self._screen, colour,
                                   (int((guess[0] + 0.5) * SCREEN_WIDTH / 10), int((guess[1] + 0.5) * SCREEN_HEIGHT / 10)),
                                   SCREEN_WIDTH // 40)

    def draw_ships(self):
        for ship in self._player_ships.values():
            ship.draw_ship(self._screen)

    def _draw_opponent_ships(self):
        for ship in self._opponent_ships.values():
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
            self._player_ships[ship_idx].rotate()
        if key == pygame.K_UP:
            self._player_ships[ship_idx].translate((0, -1))
        if key == pygame.K_DOWN:
            self._player_ships[ship_idx].translate((0, 1))
        if key == pygame.K_LEFT:
            self._player_ships[ship_idx].translate((-1, 0))
        if key == pygame.K_RIGHT:
            self._player_ships[ship_idx].translate((1, 0))

    def place_ship(self, ship_idx):
        if not self._player_ships[str(ship_idx)].check_collision(self._player_ships):
            self._player_ships[str(ship_idx)].set_status("placed")
            if ship_idx < 2:
                self._player_ships[str(ship_idx + 1)].set_status("moving")
            else:
                self.set_phase("player turn")
            return True
        return False

    def guess(self, guess):
        self._last_guess = guess

    def _process_move(self, message):
        """ Receive a move (guess) from another player.
            Check if it has hit any ships. Then see if it has sunk any.
            Update any guess lists and return the response. """
        guess = (int(message[0]), int(message[1]))
        self._last_guess = guess
        response = "RESP,MISS"
        for idx, ship in self._valid_guesses.items():
            if idx == "miss":
                continue
            if guess in ship:
                response = "RESP,HIT,{}".format(idx)
                # self._opponent_guesses[idx].append(guess)
                # Plus one since the guesses will be updated later
                if len(self._opponent_guesses[idx]) + 1 == len(ship):
                    response = "RESP,SINK,{}".format(idx)
        # if response == "RESP,MISS":
        #     self._opponent_guesses["miss"].append(guess)

        return response

    def _process_response(self, name, message):
        """ Receive response from server.
            Update game state hits and misses and change the turn.
            Can be treated as HIT, MISS or SINK. """
        if name == self._player_name:
            guesses = self._opponent_guesses
            ships = self._player_ships
        else:
            guesses = self._player_guesses
            ships = self._opponent_ships

        if message[0] == "MISS":
            guesses["miss"].append(self._last_guess)
        else:
            guesses[message[1]].append(self._last_guess)
            if message[0] == "SINK":
                sunk_ship = guesses[message[1]]
                coords = [i[0] + i[1] for i in sunk_ship]
                start, end = coords.index(min(coords)), coords.index(max(coords))
                ships[message[1]] = Ship(sunk_ship[start], sunk_ship[end], PINK)
        time.sleep(1)
        self.change_turn()

    def _process_join(self, name):
        if not self._player_name:
            self._player_name = name
            print("Joined the game as Player {}".format(name))
        else:
            print("Player {} has joined the game".format(name))

    def _process_exit(self, name):
        print("Player {} has left the game".format(name))
        self.set_phase("menu")

    def _process_ready(self, name):
        if self._game_ready:
            self._valid_guesses = self._init_tiles()
            if self._player_name == '1':
                self.set_phase("player turn")
            else:
                self.set_phase("opponent turn")
        elif name == self._player_name:
            self.set_phase("waiting")
        self._game_ready = True

    def process_message(self, message):
        name = message[0]
        if len(message) == 2:
            if message[-1] == "JOIN":
                self._process_join(name)
            elif message[-1] == "EXIT":
                self._process_exit(name)
            elif message[-1] == "READY":
                self._process_ready(name)

        else:
            if name != self._player_name and message[1] == "MOVE":
                return self._process_move(message[2:])
            elif message[1] == "RESP":
                self._process_response(name, message[2:])
        return None
