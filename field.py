#!usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame
import os
import random
from csv import reader
from enum import IntEnum
from math import exp


class ResType(IntEnum):
    TEXTURE = 0


class UnitType(IntEnum):
    ELF = 0
    MAG = 1
    KNIGHT = 2
    GOBLIN = 3
    SCULL = 4
    WIZARD = 5
    DEMON = 6


class Textures(IntEnum):
    GROUND = 0
    ELF = 1
    MAG = 2
    KNIGHT = 3
    GOBLIN = 4
    SCULL = 5
    WIZARD = 6
    DEMON = 7
    GROUND_LIGHTED = 8
    AIM = 9
    WOUND = 10


class TileType(IntEnum):
    FIELD = 0
    ROCK = 1
    CASTLE = 2
    SPIKE = 3


class ImageType(IntEnum):
    ORIG = 0
    LIGHTED = 1


FPS = 60
DELTATIME = 0
TILE_DEFENCE = {
    TileType.FIELD: 0,
    TileType.CASTLE: 3,
    TileType.SPIKE: -3,
}
    

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
        print(f"File '{fullname}' not found")
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


def create_elf(board, unit_coords, tex_holder, turn):
    unit = Unit(tex_holder.get(Textures.ELF),
                tex_holder.get(Textures.AIM),
                tex_holder.get(Textures.WOUND),
                4, 100, *board.get_cell_coords(unit_coords), turn, board)
    return unit


def create_knight(board, unit_coords, tex_holder, turn):
    unit = Unit(tex_holder.get(Textures.KNIGHT),
                tex_holder.get(Textures.AIM),
                tex_holder.get(Textures.WOUND),
                4, 100, *board.get_cell_coords(unit_coords), turn, board)
    return unit


def create_mag(board, unit_coords, tex_holder, turn):
    unit = Unit(tex_holder.get(Textures.MAG),
                tex_holder.get(Textures.AIM),
                tex_holder.get(Textures.WOUND),
                5, 100, *board.get_cell_coords(unit_coords), turn, board)
    return unit


def create_goblin(board, unit_coords, tex_holder, turn):
    unit = Unit(tex_holder.get(Textures.GOBLIN),
                tex_holder.get(Textures.AIM),
                tex_holder.get(Textures.WOUND),
                4, 100, *board.get_cell_coords(unit_coords), turn, board)
    return unit


def create_scull(board, unit_coords, tex_holder, turn):
    unit = Unit(tex_holder.get(Textures.SCULL),
                tex_holder.get(Textures.AIM),
                tex_holder.get(Textures.WOUND),
                3, 100, *board.get_cell_coords(unit_coords), turn, board)
    return unit


def create_wizard(board, unit_coords, tex_holder, turn):
    unit = Unit(tex_holder.get(Textures.WIZARD),
                tex_holder.get(Textures.AIM),
                tex_holder.get(Textures.WOUND),
                4, 100, *board.get_cell_coords(unit_coords), turn, board)
    return unit


def create_demon(board, unit_coords, tex_holder, turn):
    unit = Unit(tex_holder.get(Textures.DEMON),
                tex_holder.get(Textures.AIM),
                tex_holder.get(Textures.WOUND),
                4, 100, *board.get_cell_coords(unit_coords), turn, board)
    return unit


def load_board(name, tex_holder):
    fullname = os.path.join('data', name)
    with open(fullname) as csvfile:
        data = reader(csvfile)
        board = Board(*map(int, next(data)), tex_holder)
        for i in range(board.height):
            row = next(data)
            for j, tile_type in enumerate(row):
                board.cells[i][j].tile_type = int(tile_type)
        for unit_data in data:
            if unit_data:
                unit_coords = tuple(map(int, unit_data[1:]))
                unit = None
                if int(unit_data[0]) == UnitType.ELF:
                    unit = create_elf(board, unit_coords, tex_holder, 1)
                elif int(unit_data[0]) == UnitType.MAG:
                    unit = create_mag(board, unit_coords, tex_holder, 1)
                elif int(unit_data[0]) == UnitType.KNIGHT:
                    unit = create_knight(board, unit_coords, tex_holder, 1)
                elif int(unit_data[0]) == UnitType.GOBLIN:
                    unit = create_goblin(board, unit_coords, tex_holder, 2)
                elif int(unit_data[0]) == UnitType.SCULL:
                    unit = create_scull(board, unit_coords, tex_holder, 2)
                elif int(unit_data[0]) == UnitType.WIZARD:
                    unit = create_wizard(board, unit_coords, tex_holder, 2)
                elif int(unit_data[0]) == UnitType.DEMON:
                    unit = create_demon(board, unit_coords, tex_holder, 2)
                board.cells[unit_coords[1]][unit_coords[0]].unit = unit
        return board


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx_min, dx_max, dy_min, dx_max,
                 grav_min, grav_max, dtime_min, dtime_max, dsize,
                 tileset):
        super().__init__(self)
        
        self.image = random.choice(tileset).copy()
        self.rect = self.image.get_rect()
        self.velocity = [random.randint(dx_min, dx_max),
                         random.randint(dy_min, dy_max)]
        self.dsize = dsize
        self.dtime = random.randint(dtime_min, dtime_max)
        self.rect.x, self.rect.y = pos
        self.gravity = random.randint(grav_max, grav_min)

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class ResourceHolder:
    def __init__(self, res_type=ResType.TEXTURE):
        self.res = {}
        self.res_type = res_type

    def load(self, iden, filename, tile_size):
        if self.res_type == ResType.TEXTURE:
            img = load_image(filename)
            self.res[iden] = pygame.transform.scale(img, (img.get_width() * (tile_size / img.get_height()),
                                                          tile_size))
    def get(self, iden):
        return self.res[iden]

    def add(self, iden, obj):
        self.res[iden] = obj
    

class Tileset:
    def __init__(self, sheet, columns):
        self.tiles = []
        self.cut_sheet(sheet, columns)

    def cut_sheet(self, sheet, columns):
        rect = pygame.Rect((0, 0),
                           (sheet.get_width() // columns,
                            sheet.get_height()))
        for i in range(columns):
            tile_pos = (rect.w * i, 0)
            self.tiles.append(
                sheet.subsurface(pygame.Rect(tile_pos, rect.size)))


class AnimatedSprite(pygame.sprite.Sprite, Tileset):
    def __init__(self, sheet, columns, frame_time, x, y, *group):
        pygame.sprite.Sprite.__init__(self, *group)
        Tileset.__init__(self, sheet, columns)
        self.frame_time = frame_time
        self.cur_time = frame_time
        self.cur_frame = 0
        self.image = self.tiles[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        
    def update(self):
        self.cur_time -= DELTATIME
        if self.cur_time < 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.tiles)
            self.cur_time = self.frame_time
            self.image = self.tiles[self.cur_frame]


class Tile:
    def __init__(self, tile_type=TileType.FIELD):
        self.tile_type = tile_type
        self.unit = None
        self.walkable = False


class Unit(AnimatedSprite):
    def __init__(self, sheet, aim_img, wound_img, columns, frame_time, x, y, turn, board):
        AnimatedSprite.__init__(self, sheet, columns, frame_time, x, y, board.units)
        
        self.wound_img = wound_img
        self.wound_rect = self.wound_img.get_rect()
        
        self.aim_img = aim_img
        self.aim_rect = self.aim_img.get_rect()
        
        self.board = board
        
        self.wound_time = 1500
        self.wound_cur = self.wound_time
        self.rec_dmg = 0
        
        self.tar_coords = (x, y)

        self.tile_speed = 2
        self.moving_speed = 0.25
        self.turn = turn
        self.moved = False
        self.attack_range = 1
        self.has_attacked = False
        self.under_attack = False

        self.hp = 20
        self.attack_dmg = 7
        self.armor = 2

        self.enemies_in_range = []

    def get_walkable_tiles(self):
        if self.moved:
            return
        unit_pos = self.board.get_cell(self.rect.center)
        for row in range(self.board.height):
            for column in range(self.board.width):
                dis_x = abs(unit_pos[0] - column)
                dis_y = abs(unit_pos[1] - row)
                if dis_x + dis_y <= self.tile_speed:
                    if self.board.cells[row][column].tile_type != TileType.ROCK and not self.board.cells[row][column].unit:
                        self.board.cells[row][column].walkable = True

    def get_enemies(self):
        self.enemies_in_range.clear()
        if self.has_attacked:
            return
        unit_pos = self.board.get_cell(self.rect.center)
        for target in self.board.units:
            if target.turn != self.turn:
                target_pos = self.board.get_cell(target.rect.center)
                dis_x = abs(unit_pos[0] - target_pos[0])
                dis_y = abs(unit_pos[1] - target_pos[1])
                if dis_x + dis_y <= self.attack_range:
                    self.enemies_in_range.append(target)
                    target.under_attack = True

    def attack(self, tar):
        self.has_attacked = True
        tar_cell = tar.board.get_cell(tar.rect.center)
        tar_tile = tar.board.cells[tar_cell[1]][tar_cell[0]]
        
        dmg = self.attack_dmg - tar.armor - TILE_DEFENCE[tar_tile.tile_type]

        if dmg >= 1:
            tar.hp -= dmg
            tar.rec_dmg = dmg

        if tar.hp <= 0:
            tar.kill()
            tar_tile.unit = None

    def update(self):
        self.cur_time -= DELTATIME
        if self.cur_time < 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.tiles)
            self.cur_time = self.frame_time
            self.image = self.tiles[self.cur_frame]

        if self.rec_dmg:
            self.wound_cur -= DELTATIME
            if self.wound_cur < 0:
                self.wound_cur = self.wound_time
                self.rec_dmg = 0

        if self.rect.x != self.tar_coords[0]:
            self.rect.x = round(move_towards(self.rect.x, self.tar_coords[0], self.moving_speed * DELTATIME))

        elif self.rect.y != self.tar_coords[1]:
            self.rect.y = round(move_towards(self.rect.y, self.tar_coords[1], self.moving_speed * DELTATIME))

    def draw(self, target):
        target.blit(self.image, self.rect)
        if self.rec_dmg:
            self.wound_rect.center = self.rect.center
            target.blit(self.wound_img, self.wound_rect)
            wound_lvl_f = pygame.font.Font(None, 32)
            wound_lvl_t = wound_lvl_f.render(str(self.rec_dmg), True, pygame.Color("red"))
            target.blit(wound_lvl_t, self.rect.topleft)
        if self.under_attack:
            self.aim_rect.center = self.rect.center
            target.blit(self.aim_img, self.aim_rect)


class GameManager:
    def __init__(self, map_name, lang='ru'):
        self.screen_sizes = 800, 600
        self.screen = pygame.display.set_mode(self.screen_sizes)
        self.selected_unit = None
        self.moving = False
        self.running = True
        self.prev_pos = 0, 0
        self.light_color = (128, 128, 255, 255)

        self.tex_holder = ResourceHolder(ResType.TEXTURE)
        self.load_textures(tile_size=64)
        
        self.board = load_board(map_name, self.tex_holder)
        self.cur_turn = 1

    def load_textures(self, tile_size=64):
        self.tex_holder.load(Textures.GROUND, "ground.png", tile_size)
        self.tex_holder.load(Textures.ELF, "elf.png", tile_size)
        self.tex_holder.load(Textures.KNIGHT, "knight.png", tile_size)
        self.tex_holder.load(Textures.MAG, "mag.png", tile_size)
        self.tex_holder.load(Textures.GOBLIN, "goblin.png", tile_size)
        self.tex_holder.load(Textures.SCULL, "scull.png", tile_size)
        self.tex_holder.load(Textures.WIZARD, "wizard.png", tile_size)
        self.tex_holder.load(Textures.DEMON, "demon.png", tile_size)
        self.tex_holder.load(Textures.AIM, "aim.png", tile_size // 2)
        self.tex_holder.load(Textures.WOUND, "wound.png", tile_size // 2)        

        self.tex_holder.add(Textures.GROUND_LIGHTED,
                            change_color(self.tex_holder.get(Textures.GROUND), *self.light_color))

    def on_cell_click(self, cell):
        tile = self.board.cells[cell[1]][cell[0]]
        if tile.unit:
            self.board.reset_tiles()
            self.board.reset_units()
            if self.selected_unit is tile.unit:
                # selected unit was previously selected
                self.selected_unit = None
            elif tile.unit.turn == self.cur_turn:
                # selected unit is friend
                self.selected_unit = tile.unit
                self.selected_unit.get_enemies()
                self.selected_unit.get_walkable_tiles()
            else:
                # selected unit is enemy
                if self.selected_unit:
                    if tile.unit in self.selected_unit.enemies_in_range:
                        self.selected_unit.attack(tile.unit)
                    self.selected_unit = None
        else:
            if self.board.cells[cell[1]][cell[0]].walkable and self.selected_unit:
                if not self.selected_unit.moved:
                    # moving unit
                    cur_cell = self.board.get_cell(self.selected_unit.rect.center)
                    self.board.cells[cur_cell[1]][cur_cell[0]].unit = None
                    self.board.cells[cell[1]][cell[0]].unit = self.selected_unit
                    # self.selected_unit.move(self.board.get_cell_coords(cell))
                    self.selected_unit.tar_coords = self.board.get_cell_coords(cell)
                    self.selected_unit.moved = True
                    self.selected_unit = None
                    self.board.reset_units()
                    self.board.reset_tiles()

    def on_mouse_button_down(self, event):
        if event.button == 3:
            self.moving = True
            self.prev_pos = event.pos
        elif event.button == 1:    
            cell = self.board.get_cell(self.board.translate_point(*event.pos))
            if cell:
                self.on_cell_click(cell)

    def on_mouse_button_up(self, event):
        if event.button == 3:
            self.moving = False

    def on_mouse_motion(self, event):
        self.board.outlined_cell = self.board.get_cell(self.board.translate_point(*event.pos))
        if self.moving:
            self.board.offset_x -= self.prev_pos[0] - event.pos[0]
            self.board.offset_y -= self.prev_pos[1] - event.pos[1]
            self.prev_pos = event.pos

    def on_mouse_wheel(self, event):
        mp = pygame.mouse.get_pos()
        mp_origin = self.board.translate_point(mp[0], mp[1])
        self.board.scale = max(0.625, min(2., self.board.scale * exp(event.y * 0.1)))
        self.board.offset_x = mp[0] - mp_origin[0] * self.board.scale
        self.board.offset_y = mp[1] - mp_origin[1] * self.board.scale

    def on_key_down(self, event):
        if event.key == pygame.K_SPACE:
            self.end_step()
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_button_down(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.on_mouse_button_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.on_mouse_motion(event)
            if event.type == pygame.MOUSEWHEEL:
                self.on_mouse_wheel(event)
            if event.type == pygame.KEYDOWN:
                self.on_key_down(event)

    def end_step(self):
        self.board.reset_tiles()
        self.selected_unit = None
        if self.cur_turn == 1:
            self.cur_turn = 2
        else:
            self.cur_turn = 1
        for unit in self.board.units:
            unit.moved = False
            unit.under_attack = False
            unit.has_attacked = False

    def start_game(self):
        global DELTATIME
        clock = pygame.time.Clock()
        while self.running:
            DELTATIME = clock.get_time()
            self.process_events()
            self.screen.fill((0, 0, 0))
            self.board.render(self.screen)
            pygame.display.flip()
            pygame.display.set_caption(f'TBS. FPS: {int(clock.get_fps())}')
            clock.tick(FPS)
            
            
class Board:
    def __init__(self, width, height, tex_holder):
        self.width = width
        self.height = height
        self.scale = 1
        self.offset_x = 10
        self.offset_y = 10
        self.cells = [[Tile(TileType.FIELD) for _ in range(width)]
                      for _ in range(height)]
        self.units = pygame.sprite.Group()
        self.outline_width = 2
        self.cell_size = 30
        self.outlined_cell = None
        self.selected_unit = None
        grd_set = Tileset(tex_holder.get(Textures.GROUND), 4)
        grd_lighted_set = Tileset(tex_holder.get(Textures.GROUND_LIGHTED), 4)
        self.ground_images = {
            TileType.FIELD: {ImageType.ORIG: grd_set.tiles[0],
                             ImageType.LIGHTED: grd_lighted_set.tiles[0]},
            TileType.ROCK: {ImageType.ORIG: grd_set.tiles[1],
                            ImageType.LIGHTED: grd_lighted_set.tiles[1]},
            TileType.CASTLE: {ImageType.ORIG: grd_set.tiles[2],
                              ImageType.LIGHTED: grd_lighted_set.tiles[2]},
            TileType.SPIKE: {ImageType.ORIG: grd_set.tiles[3],
                              ImageType.LIGHTED: grd_lighted_set.tiles[3]},
        }
        self.set_view()

    def set_view(self, cell_size=64, outline_width=2):
        self.cell_size = cell_size
        self.outline_width = outline_width

    def render(self, target):
        buffer = pygame.Surface(self.get_total_board_size())
        for row in range(self.height):
            for column in range(self.width):
                x, y = self.get_cell_coords((column, row))
                cell_rect = pygame.Rect((x, y), (self.cell_size, self.cell_size))
                image = self.ground_images[self.cells[row][column].tile_type][ImageType.ORIG]
                if self.cells[row][column].walkable:
                    image = self.ground_images[self.cells[row][column].tile_type][ImageType.LIGHTED]
                if (column, row) == self.outlined_cell:
                    image = pygame.transform.scale(image, (image.get_width() + 5, image.get_height() + 5))
                    buffer.blit(image, cell_rect.move(-2.5, -2.5))
                else:
                    buffer.blit(image, cell_rect)

        for unit in self.units:
            unit.update()
            unit.draw(buffer)

        self.draw_outline(self.outlined_cell, pygame.Color("red"), buffer)
        buffer = pygame.transform.scale(buffer, (buffer.get_width() * self.scale, buffer.get_height() * self.scale))
        target.blit(buffer, (self.offset_x, self.offset_y))
        rendered.set()

    def draw_outline(self, cell, color, surface):
        if cell:
            x = cell[0] * (self.cell_size + self.outline_width * 2)
            y = cell[1] * (self.cell_size + self.outline_width * 2)
            size = self.outline_width + self.cell_size + 2.5
            outline_rect = pygame.Rect((x, y), (size, size))
            pygame.draw.rect(surface, color, outline_rect, width=self.outline_width)

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

    def get_total_board_size(self):
        width = self.outline_width * self.width * 2 + self.cell_size * self.width
        height = self.outline_width * self.height * 2 + self.cell_size * self.height
        return width, height

    def reset_tiles(self):
        for row in range(self.height):
            for column in range(self.width):
                self.cells[row][column].walkable = False

    def reset_units(self):
        for unit in self.units:
            unit.under_attack = False
                
    def get_cell_coords(self, cell):
        x = self.outline_width + cell[0] * (self.cell_size + self.outline_width * 2)
        y = self.outline_width + cell[1] * (self.cell_size + self.outline_width * 2)
        return x, y

    def translate_point(self, x, y):
        return (x - self.offset_x) / self.scale, (y - self.offset_y) / self.scale


if __name__ == '__main__':
    pygame.init()
    game_manager = GameManager("map1.csv")
    game_manager.start_game()
