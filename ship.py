import pygame
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, LIGHTGREY


class Ship:
    def __init__(self, start, end, colour):
        self._start = start
        self._end = end
        self._colour = colour
        self._phase = "not placed"
        self._array = []
        self.create_array(self._start, self._end)
        self._size = len(self._array)

    def create_array(self, start, end):
        self._array = []
        x, y = start
        if start[0] == end[0]:
            for y in range(start[1], end[1] + 1):
                self._array.append((x, y))

        elif start[1] == end[1]:
            for x in range(start[0], end[0] + 1):
                self._array.append((x, y))

    def draw_ship(self, screen):
        for position in self._array:
            if self._colour != BLACK:
                pygame.draw.rect(screen, self._colour, self.get_rect(position))

    def get_rect(self, position):
        return pygame.Rect(position[0] * SCREEN_WIDTH / 10,
                           position[1] * SCREEN_HEIGHT / 10,
                           SCREEN_WIDTH / 10,
                           SCREEN_HEIGHT / 10)

    def translate(self, change):
        temp_start = (change[0] + self._start[0], change[1] + self._start[1])
        temp_end = (change[0] + self._end[0], change[1] + self._end[1])
        if not self._check_boundaries(temp_start, temp_end):
            return
        self.create_array(temp_start, temp_end)
        self._start, self._end = temp_start, temp_end

    def rotate(self):
        change = (self._end[0] - self._start[0], self._end[1] - self._start[1])
        temp_end = (change[1] + self._start[0], change[0] + self._start[1])
        if not self._check_boundaries(self._start, temp_end):
            return
        self.create_array(self._start, temp_end)
        self._end = temp_end

    def get_size(self):
        return self._size

    def _set_colour(self, colour):
        self._colour = colour

    def set_phase(self, phase):
        self._phase = phase
        if self._phase == "not placed":
            self._set_colour(BLACK)
        if self._phase == "moving":
            self._set_colour(WHITE)
        if self._phase == "placed":
            self._set_colour(LIGHTGREY)

    def _check_boundaries(self, start, end):
        if (start[0] < 0 or start[0] > 9
                or start[1] < 0 or start[1] > 9
                or end[0] < 0 or end[0] > 9
                or end[1] < 0 or end[1] > 9):
            return False
        else:
            return True

    def check_collision(self, ships):
        for ship in ships:
            if ship.get_phase() == "placed":
                for position in self.get_array():
                    if position in ship.get_array():
                        return True
        return False

    def get_array(self):
        return self._array

    def get_phase(self):
        return self._phase

    def __getitem__(self, item):
        return self._array[item]
