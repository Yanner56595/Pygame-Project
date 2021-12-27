# -*- coding: utf-8 -*-
import sys

import pygame
import os
from enum import Enum
from math import exp

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class TileType(Enum):
    FIELD = 0
    ROCK = 1
    CASTLE = 2
    WATER = 3


class Tileset:
    def __init__(self, sheet, columns, rows):
        self.tiles = []
        self.cut_sheet(sheet, columns, rows)

    def cut_sheet(self, sheet, columns, rows):
        rect = pygame.Rect((0, 0),
                           (sheet.get_width() // columns,
                            sheet.get_height() // rows))
        for j in range(rows):
            for i in range(columns):
                tile_location = (rect.w * i, rect.h * j)
                self.tiles.append(sheet.subsurface(pygame.Rect(
                    tile_location, rect.size)))


class Tile:
    ground_tileset = Tileset(load_image("ground.png"), 2, 2)
    images = {
        TileType.FIELD: ground_tileset.tiles[0],
        TileType.ROCK: ground_tileset.tiles[2],
    }

    def __init__(self, tile_type=TileType.FIELD):
        self.tile_type = tile_type
        self.unit = None


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[Tile(TileType.FIELD)] * width for _ in range(height)]
        self.outline = 2
        self.cell_size = 30
        self.outlined_cell = None
        self.set_view()

    def set_view(self, left=10, top=10, cell_size=30, outline=2):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.outline = outline
        for type, image in Tile.images.items():
            Tile.images[type] = pygame.transform.scale(image, (cell_size, cell_size))

    def render(self, target):
        buffer = pygame.Surface(self.get_total_board_size())
        for row in range(self.height):
            for column in range(self.width):
                x = self.outline + column * (self.cell_size + self.outline * 2)
                y = self.outline + row * (self.cell_size + self.outline * 2)
                cell_rect = pygame.Rect((x, y), (self.cell_size, self.cell_size))
                buffer.blit(Tile.images[self.board[row][column].tile_type], cell_rect)
        self.draw_outline(self.outlined_cell, buffer)
        return buffer

    def draw_outline(self, cell, surface):
        if cell:
            x = cell[0] * (self.cell_size + self.outline * 2)
            y = cell[1] * (self.cell_size + self.outline * 2)
            size = self.outline * 2 + self.cell_size
            outline_rect = pygame.Rect((x, y), (size, size))
            pygame.draw.rect(surface, pygame.Color("red"), outline_rect, width=self.outline)

    def get_cell(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        column = mouse_x // (self.cell_size + self.outline * 2)
        row = mouse_y // (self.cell_size + self.outline * 2)
        if (0 <= column < self.width and 0 <= row < self.height and
                0 <= mouse_x - column * (self.cell_size + 2 * self.outline) - self.outline <= self.cell_size and
                0 <= mouse_y - row * (self.cell_size + 2 * self.outline) - self.outline <= self.cell_size):
            return column, row
        return None

    def on_click(self, cell):
        # print(cell)
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_total_board_size(self):
        width = self.outline * self.width * 2 + self.cell_size * self.width
        height = self.outline * self.height * 2 + self.cell_size * self.height
        return width, height


def translate_point(x, y):
    center_x = width/2
    center_y = height/2
    return (x - offset_x) / scale, (y - offset_y) / scale

board = Board(10, 7)
board.set_view(cell_size=64)
width, height = board.get_total_board_size()
offset_x = 10
offset_y = 10
if __name__ == '__main__':
    scale = 1
    screen = pygame.display.set_mode((width + offset_x * 2, height + offset_y * 2))
    running = True
    moving = False
    fps = 60
    clock = pygame.time.Clock()
    distance = 0, 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    moving = True
                    distance = event.pos
                else:    
                    board.get_click(translate_point(*event.pos))
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    moving = False
            if event.type == pygame.MOUSEMOTION:
                board.outlined_cell = board.get_cell(translate_point(*event.pos))
                if moving:
                    offset_x -= distance[0] - event.pos[0]
                    offset_y -= distance[1] - event.pos[1]
                    distance = event.pos
            if event.type == pygame.MOUSEWHEEL:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_origin = translate_point(mouse_pos[0], mouse_pos[1])
                scale = max(0.625, min(2, scale * exp(event.y * 0.1)))
                offset_x = mouse_pos[0] - mouse_pos_origin[0] * scale
                offset_y = mouse_pos[1] - mouse_pos_origin[1] * scale
        screen.fill((0, 0, 0))
        brd = board.render(screen)
        brd = pygame.transform.scale(brd, (width * scale, height * scale))
        screen.blit(brd, (offset_x, offset_y))
        pygame.display.flip()
        clock.tick(fps)