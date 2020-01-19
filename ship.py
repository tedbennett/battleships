# !/usr/bin/env python3
import pygame
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY


class Ship:
    def __init__(self, start, end, colour):
        self._start = start
        self._end = end
        self._colour = colour
        self.status = "not placed"
        self.array = []
        self._create_array(self._start, self._end)
        self.size = len(self.array)

    def _create_array(self, start, end):
        self.array = []
        x, y = start
        if start[0] == end[0]:
            for y in range(start[1], end[1] + 1):
                self.array.append((x, y))

        elif start[1] == end[1]:
            for x in range(start[0], end[0] + 1):
                self.array.append((x, y))

    def draw_ship(self, screen):
        for position in self.array:
            if self._colour != BLACK:
                pygame.draw.rect(screen, self._colour,
                                 pygame.Rect(position[0] * SCREEN_WIDTH / 10,
                                             position[1] * SCREEN_HEIGHT / 10,
                                             SCREEN_WIDTH / 10,
                                             SCREEN_HEIGHT / 10)
                                 )

    def translate(self, change):
        temp_start = (change[0] + self._start[0], change[1] + self._start[1])
        temp_end = (change[0] + self._end[0], change[1] + self._end[1])
        if not self._check_boundaries(temp_start, temp_end):
            return
        self._create_array(temp_start, temp_end)
        self._start, self._end = temp_start, temp_end

    def rotate(self):
        change = (self._end[0] - self._start[0], self._end[1] - self._start[1])
        temp_end = (change[1] + self._start[0], change[0] + self._start[1])
        if not self._check_boundaries(self._start, temp_end):
            return
        self._create_array(self._start, temp_end)
        self._end = temp_end

    def set_status(self, phase):
        self.status = phase
        if self.status == "not placed":
            self._set_colour(BLACK)
        elif self.status == "moving":
            self._set_colour(WHITE)
        elif self.status == "placed":
            self._set_colour(LIGHTGREY)

    def _check_boundaries(self, start, end):
        if (start[0] < 0 or start[0] > 9
                or start[1] < 1 or start[1] > 10
                or end[0] < 0 or end[0] > 9
                or end[1] < 1 or end[1] > 10):
            return False
        else:
            return True

    def check_collision(self, ships):
        for ship in ships.values():
            if ship.get_status() == "placed":
                for position in self.get_array():
                    if position in ship.get_array():
                        return True
        return False

    def get_size(self):
        return self.size

    def _set_colour(self, colour):
        self._colour = colour

    def get_array(self):
        return self.array

    def get_status(self):
        return self.status

    def __getitem__(self, item):
        return self.array[item]
