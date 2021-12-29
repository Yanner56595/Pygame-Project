# -*- coding: utf-8 -*-
import sys
import pygame
import os
from threading import Thread, Event
from enum import Enum
from math import exp, ceil, floor


pygame.init()


def move_towards(cur, tar, delta):
    if tar < cur and cur - delta > tar:
        cur -= delta
    elif tar > cur and cur + delta < tar:
        cur += delta
    else:
        cur = tar
    return cur


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)    
    if colorkey:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def change_color(img, dr, dg, db, da):
    new_img = img.copy()
    new_img.fill((dr, dg, db, da), special_flags=pygame.BLEND_RGBA_MULT)
    return new_img


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
    def __init__(self, tile_type=TileType.FIELD):
        self.tile_type = tile_type
        self.unit = None
        self.walkable = False


class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = tux_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.tile_speed = 2
        self.moving_speed = 5
        self.attack_range = 1
        self.moved = False
        self.is_moving = False

    def get_walkable_tiles(self, brd, unit_pos):
        if self.moved:
            return
        for row in range(brd.height):
            for column in range(brd.width):
                if abs(unit_pos[0] - column) + abs(unit_pos[1] - row) <= self.tile_speed:
                    if brd.board[row][column].tile_type != TileType.ROCK:
                        brd.board[row][column].walkable = True

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def get_cur_cell(self, board):
        return board.get_cell(self.rect.center)

    def move(self, tar):
        Thread(target=self.start_movement, args=tar).start()
    
    def start_movement(self, x, y):
        self.is_moving = True
        while self.rect.x != x:
            drawing_event.clear()
            self.rect.x = move_towards(self.rect.x, x, self.moving_speed)
            drawing_event.wait()
        while self.rect.y != y:
            drawing_event.clear()
            self.rect.y = move_towards(self.rect.y, y, self.moving_speed)
            drawing_event.wait()
        self.is_moving = False

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[Tile(TileType.FIELD) for _ in range(width)] for _ in range(height)]
        self.units = []
        self.outline_width = 2
        self.cell_size = 30
        self.outlined_cell = None
        self.selected_unit = None
        ground_tileset = Tileset(load_image("ground.png"), 2, 2)
        self.ground_images = {
            TileType.FIELD: ground_tileset.tiles[0],
            TileType.ROCK: ground_tileset.tiles[2],
        }
        self.set_view()

    def set_view(self, cell_size=64, outline_width=2):
        self.cell_size = cell_size
        self.outline_width = outline_width
        for type, image in self.ground_images.items():
            self.ground_images[type] = pygame.transform.scale(image, (cell_size, cell_size))

    def render(self, target):
        buffer = pygame.Surface(self.get_total_board_size())
        for row in range(self.height):
            for column in range(self.width):
                x, y = self.get_cell_coords((column, row))
                cell_rect = pygame.Rect((x, y), (self.cell_size, self.cell_size))
                image = self.ground_images[self.board[row][column].tile_type]
                if self.board[row][column].walkable:
                    image = change_color(image, 128, 128, 255, 255)
                if (column, row) == self.outlined_cell:
                    image = pygame.transform.scale(image, (image.get_width() + 5, image.get_height() + 5))
                    buffer.blit(image, cell_rect.move(-2.5, -2.5))
                else:
                    buffer.blit(image, cell_rect)
                unit = self.board[row][column].unit
                if unit:
                    if not unit.is_moving:
                        unit.rect.center = cell_rect.center
        for unit in self.units:
            unit.draw(buffer)
        self.draw_outline(self.outlined_cell, buffer)
        drawing_event.set()
        return buffer

    def draw_outline(self, cell, surface):
        if cell:
            x = cell[0] * (self.cell_size + self.outline_width * 2)
            y = cell[1] * (self.cell_size + self.outline_width * 2)
            size = self.outline_width + self.cell_size + 2.5
            outline_rect = pygame.Rect((x, y), (size, size))
            pygame.draw.rect(surface, pygame.Color("red"), outline_rect, width=self.outline_width)

    def get_cell(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        column = mouse_x // (self.cell_size + self.outline_width * 2)
        row = mouse_y // (self.cell_size + self.outline_width * 2)
        if (0 <= column < self.width and 0 <= row < self.height and
                0 <= mouse_x - column * (self.cell_size + 2 * self.outline_width) - self.outline_width <= self.cell_size and
                0 <= mouse_y - row * (self.cell_size + 2 * self.outline_width) - self.outline_width <= self.cell_size):
            return int(column), int(row)
        return None

    def on_click(self, cell):
        tile = self.board[cell[1]][cell[0]]
        if tile.unit:
            if self.selected_unit is tile.unit:
                self.selected_unit = None
                self.reset_tiles()
            else:
                self.selected_unit = tile.unit
                self.reset_tiles()
                self.selected_unit.get_walkable_tiles(self, cell)
        else:
            if self.board[cell[1]][cell[0]].walkable and self.selected_unit:
                cur_cell = self.selected_unit.get_cur_cell(board)
                self.board[cur_cell[1]][cur_cell[0]].unit = None
                self.board[cell[1]][cell[0]].unit = self.selected_unit
                self.selected_unit.move(self.get_cell_coords(cell))
                self.selected_unit = None
                self.reset_tiles()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_total_board_size(self):
        width = self.outline_width * self.width * 2 + self.cell_size * self.width
        height = self.outline_width * self.height * 2 + self.cell_size * self.height
        return width, height

    def reset_tiles(self):
        for row in range(self.height):
            for column in range(self.width):
                self.board[row][column].walkable = False

    def get_cell_coords(self, cell):
        x = self.outline_width + cell[0] * (self.cell_size + self.outline_width * 2)
        y = self.outline_width + cell[1] * (self.cell_size + self.outline_width * 2)
        return x, y
        
def translate_point(x, y):
    center_x = width/2
    center_y = height/2
    return (x - offset_x) / scale, (y - offset_y) / scale


if __name__ == '__main__':
    scale = 1
    width, height = size = 800, 600
    offset_x = 10
    offset_y = 10
    
    screen = pygame.display.set_mode(size)
    board = Board(10, 7)

    drawing_event = Event()
    
    tux_img = pygame.transform.scale(load_image("tux.png"), (64, 64))
    tux = Unit(0, 0)
    board.board[3][4].unit = tux
    board.units.append(tux)
    
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
        brd = pygame.transform.scale(brd, (brd.get_width() * scale, brd.get_height() * scale))
        screen.blit(brd, (offset_x, offset_y))
        pygame.display.flip()
        clock.tick(fps)
