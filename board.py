# !/usr/bin/env python3
import time

import pygame
from ship import Ship
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY, DARKGREY, RED, PINK


class Board:
    """Class representing the player's board. Contains ships and player's and opponent's guesses. """

    def __init__(self, screen, font):
        self.phase = "placement"  # Can be placement, waiting, player turn, opponent turn, end
        self._screen = screen
        self._font = font
        self._screen_text = [self._render_text("Placement phase")]
        self._player_ships = {'1': Ship((0, 1), (4, 1), WHITE),
                              '2': Ship((0, 1), (3, 1), BLACK)}
        # Ship((0, 0), (2, 0), BLACK),
        # Ship((0, 0), (1, 0), BLACK),
        # Ship((0, 0), (1, 0), BLACK)]
        self.num_ships = len(self._player_ships)
        self._valid_guesses = {}
        self._opponent_guesses = self._init_guesses()
        self._player_guesses = self._init_guesses()
        self._opponent_ships = {}
        self._last_guess = None
        self._player_name = None
        self._game_ready = False
        self._num_sunk = 0

    # Initialisation functions

    def _init_guesses(self):
        """ Create dict of empty lists for each ship, as well as misses."""
        guesses = {}
        for idx in self._player_ships:
            guesses[idx] = []
        guesses["miss"] = []
        return guesses

    def _init_tiles(self):
        """ Create dict of all coordinates occupied by a ship tile"""
        tiles = {}
        for idx, ship in self._player_ships.items():
            tiles[idx] = ship.get_array()
        return tiles

    # Public functions

    def draw_board(self):
        """ Draws the board to the pygame surface."""
        self._screen.fill(DARKGREY)
        for x in range(1, 11):
            pygame.draw.line(self._screen, LIGHTGREY,
                             (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT / 10),
                             (SCREEN_WIDTH * x / 10, SCREEN_HEIGHT + SCREEN_HEIGHT / 10), 1)
            pygame.draw.line(self._screen, LIGHTGREY,
                             (0, SCREEN_HEIGHT * x / 10),
                             (SCREEN_WIDTH, SCREEN_HEIGHT * x / 10), 1)

        if self.get_phase() != "waiting":
            self._draw_ships()
            if self.get_phase() != "placement":
                self._draw_guesses()

        for text_object in self._screen_text:
            self._screen.blit(text_object[0], (text_object[1], text_object[2]))

    def get_phase(self):
        return self.phase

    def _set_phase(self, phase, name=None):
        self.phase = phase
        self._update_text(name)

    def valid_guess(self, guess):
        """ Checks if guess has already been made. """
        for ship in self._get_guesses().values():
            if guess in ship:
                return False
        self._last_guess = guess
        return True

    # Placement phase public functions

    def move_ship(self, ship_idx, key):
        """ Moves ship in the placement phase by user input """
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
        """ Attempts to confirm the position of a piece in placement phase. Checks for collisions first. """
        if not self._player_ships[str(ship_idx)].check_collision(self._player_ships):
            self._player_ships[str(ship_idx)].set_status("placed")
            if ship_idx < 2:
                self._player_ships[str(ship_idx + 1)].set_status("moving")
            return True
        return False

    # Message processing public functions

    def process_message(self, message):
        """ Receives a message from the client and passes it to the relevant helper function """
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
                response = self._process_response(name, message[2:])
                return response
            elif message[1] == "END":
                self._set_phase("end", message[2])
        return None

    # Private functions

    def _change_turn(self):
        """ Changes game turn """
        print("changing turn")
        if self.get_phase() == "opponent turn":
            self._set_phase("player turn")
        elif self.get_phase() == "player turn":
            self._set_phase("opponent turn")
        else:
            return

    def _get_guesses(self):
        """ Returns guesses made based on the current turn. """
        if self.get_phase() == "opponent turn":
            return self._opponent_guesses
        elif self.get_phase() == "player turn":
            return self._player_guesses

    def _get_ships(self):
        """ Returns ships to draw based on the current turn. """
        if self.get_phase() == "opponent turn" or self.get_phase() == "placement":
            return self._player_ships
        elif self.get_phase() == "player turn":
            return self._opponent_ships

    # Private draw functions

    def _draw_guesses(self):
        """ Colours and draws guesses to the screen. """
        for name, guesses in self._get_guesses().items():
            if name != "miss":
                colour = RED
            else:
                colour = WHITE
            for guess in guesses:
                pygame.draw.circle(self._screen, colour,
                                   (int((guess[0] + 0.5) * SCREEN_WIDTH / 10),
                                    int((guess[1] + 0.5) * SCREEN_HEIGHT / 10)),
                                   SCREEN_WIDTH // 40)

    def _draw_ships(self):
        ships = self._get_ships()
        for ship in ships.values():
            ship.draw_ship(self._screen)

    def _render_text(self, text, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 20, colour=WHITE):
        text_surface, rect = self._font.render(text, colour)
        return [text_surface, x - (rect.width / 2), y - (rect.height / 2)]

    def _update_text(self, name):
        if self.phase == "waiting":
            self._screen_text = [self._render_text("Waiting for other player")]
        elif self.phase == "player turn":
            self._screen_text = [self._render_text("Your turn")]
        elif self.phase == "opponent turn":
            self._screen_text = [self._render_text("Opponent's turn")]
        elif self.phase == "end":
            if name:
                self._screen_text =[self._render_text("Player {} wins!".format(name))]
            else:
                self._screen_text = [self._render_text("Other player left game".format(name))]
            self._screen_text.append(self._render_text("BACK TO MENU", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 11 / 10 / 2, BLACK))

    # Message processing private functions

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
                # Plus one since the guesses will be updated later
                if len(self._opponent_guesses[idx]) + 1 == len(ship):
                    response = "RESP,SINK,{}".format(idx)
        return response

    def _process_response(self, name, message):
        """ Receive response from server.
            Update game state hits and misses and change the turn.
            Can be treated as HIT, MISS or SINK. """
        response = None
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
                if name != self._player_name:
                    self._num_sunk += 1
                    if self._num_sunk == self.num_ships:
                        response = "END,{}".format(name)
        time.sleep(1)
        self._change_turn()
        return response

    def _process_join(self, name):
        if not self._player_name:
            self._player_name = name
            print("Joined the game as Player {}".format(name))
        else:
            print("Player {} has joined the game".format(name))

    def _process_exit(self, name):
        print("Player {} has left the game".format(name))
        self._set_phase("end")

    def _process_ready(self, name):
        if self._game_ready:
            self._valid_guesses = self._init_tiles()
            if self._player_name == '1':
                self._set_phase("player turn")
            else:
                self._set_phase("opponent turn")
        elif name == self._player_name:
            self._set_phase("waiting")
        self._game_ready = True

    def _end_game(self, name=None):
        if name:
            self._set_phase("menu")
            print("Player {} has won the game".format(name))
