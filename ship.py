import pygame
from board import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


class Ship:
    def __init__(self, start, end):
        self._start = start
        self._end = end
        self._array = []
        self.create_array()
        self._size = len(self._array)

    def create_array(self):
        x = self._start[0]
        y = self._start[1]

        if self._start[0] == self._end[0]:
            for y in range(self._start[1], self._end[1] + 1):
                self._array.append((x, y))

        elif self._start[1] == self._end[1]:
            for x in range(self._start[0], self._end[0] + 1):
                self._array.append((x, y))

    def draw_piece(self, screen):
        for position in self._array:
            pygame.draw.rect(screen, WHITE, self.get_rect(position))

    def get_rect(self, x, y):
        return pygame.Rect(x * SCREEN_WIDTH / 10,
                           y * SCREEN_HEIGHT / 10,
                           SCREEN_WIDTH / 10,
                           SCREEN_HEIGHT / 10)

    def get_size(self):
        return self._size

    def __getitem__(self, item):
        return self._array[item]
