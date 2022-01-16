#!usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame
import pygame_gui
import os
import random
from csv import reader
from enum import IntEnum
from math import exp


class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class ResType(IntEnum):
    TEXTURE = 0
    SOUND = 1


class UnitType(IntEnum):
    ELF = 0
    MAG = 1
    KNIGHT = 2
    GOBLIN = 3
    SCULL = 4
    WIZARD = 5
    DEMON = 6
    HERO = 7


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
    BLOOD = 11
    HERO = 12
    MEDALS = 13
    SATAN = 14
    SCROOGE = 15
    VS = 16
    BACKGROUND = 17


class Sounds(IntEnum):
    TYPING = 0
    BREAK = 1


class TileType(IntEnum):
    FIELD = 0
    ROCK = 1
    CASTLE = 2
    SPIKE = 3


class ImageType(IntEnum):
    ORIG = 0
    LIGHTED = 1


class AIStepType(IntEnum):
    MOVE = 0
    ATTACK = 1


class StepData:
    def __init__(self, type, orig, dest, etc):
        self.type = type
        self.orig = orig
        self.dest = dest
        self.etc = etc


FPS = 60
TILE_DEFENCE = {
    TileType.FIELD: 0,
    TileType.CASTLE: 3,
    TileType.SPIKE: -3,
}
TILE_COEFF = {
    TileType.FIELD: 1,
    TileType.CASTLE: 1.2,
    TileType.SPIKE: 0.6,
}
UNIT_SIG = {
    UnitType.ELF: 10,
    UnitType.MAG: 15,
    UnitType.KNIGHT: 12,
    UnitType.GOBLIN: 12,
    UnitType.SCULL: 7,
    UnitType.WIZARD: 15,
    UnitType.DEMON: 30,
    UnitType.HERO: 90,
}


def val_to_coeff(val, max_val, min_val, max_coeff, min_coeff):
    return (val - min_val) / (max_val - min_val) * (max_coeff - min_coeff) + min_coeff


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


def create_hero(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.HERO, Textures.HERO, tex_holder,
                5, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 1, 1, 50, 15, 4, board, canvas)
    return unit


def create_elf(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.ELF, Textures.ELF, tex_holder,
                4, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 2, 2, 15, 5, 1, board, canvas)
    return unit


def create_knight(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.KNIGHT, Textures.KNIGHT, tex_holder,
                4, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 1, 1, 20, 10, 3, board, canvas)
    return unit


def create_mag(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.MAG, Textures.MAG, tex_holder,
                5, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 2, 2, 5, 10, 0, board, canvas)
    return unit


def create_goblin(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.GOBLIN, Textures.GOBLIN, tex_holder,
                4, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 1, 1, 20, 10, 3, board, canvas)
    return unit


def create_scull(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.SCULL, Textures.SCULL, tex_holder,
                3, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 3, 1, 7, 3, 0, board, canvas)
    return unit


def create_wizard(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.WIZARD, Textures.WIZARD, tex_holder,
                4, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 2, 2, 5, 10, 0, board, canvas)
    return unit


def create_demon(board, unit_coords, tex_holder, canvas, turn):
    unit = Unit(UnitType.DEMON, Textures.DEMON, tex_holder,
                4, 0.1, 0, *board.get_cell_coords(unit_coords), turn, 1, 1, 50, 10, 4, board, canvas)
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
                    unit = create_elf(board, unit_coords, tex_holder, board.canvas, 1)
                elif int(unit_data[0]) == UnitType.MAG:
                    unit = create_mag(board, unit_coords, tex_holder, board.canvas, 1)
                elif int(unit_data[0]) == UnitType.KNIGHT:
                    unit = create_knight(board, unit_coords, tex_holder, board.canvas, 1)
                elif int(unit_data[0]) == UnitType.GOBLIN:
                    unit = create_goblin(board, unit_coords, tex_holder, board.canvas, 2)
                elif int(unit_data[0]) == UnitType.SCULL:
                    unit = create_scull(board, unit_coords, tex_holder, board.canvas, 2)
                elif int(unit_data[0]) == UnitType.WIZARD:
                    unit = create_wizard(board, unit_coords, tex_holder, board.canvas, 2)
                elif int(unit_data[0]) == UnitType.DEMON:
                    unit = create_demon(board, unit_coords, tex_holder, board.canvas, 2)
                elif int(unit_data[0]) == UnitType.HERO:
                    unit = create_hero(board, unit_coords, tex_holder, board.canvas, 1)
                board.cells[unit_coords[1]][unit_coords[0]].unit = unit
        return board


def create_particle(pos, tileset, dx_min, dx_max, dy_min, dy_max,
                    time_min, time_max, count, *group):
    for i in range(count):
        Particle(pos, tileset, dx_min, dx_max, dy_min, dy_max,
                 time_min, time_max, *group)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, tileset, dx_min, dx_max, dy_min, dy_max,
                 time_min, time_max, *group):
        super().__init__(*group)
        self.image = random.choice(tileset.tiles)
        self.rect = self.image.get_rect()
        self.velocity = [random.uniform(dx_min, dx_max),
                         random.uniform(dy_min, dy_max)]
        self.time = random.uniform(time_min, time_max)
        self.rect.x, self.rect.y = pos
        self.coords = list(pos)

    def update(self, time_delta):
        self.coords[0] += self.velocity[0]
        self.coords[1] += self.velocity[1]
        self.rect.x = round(self.coords[0])
        self.rect.y = round(self.coords[1])
        self.time -= time_delta
        if self.time < 0:
            self.kill()


class ResourceHolder:
    def __init__(self, res_type=ResType.TEXTURE):
        self.res = {}
        self.res_type = res_type

    def load(self, iden, filename, tile_size=0):
        if self.res_type == ResType.TEXTURE:
            img = load_image(filename)
            if tile_size:
                self.res[iden] = pygame.transform.scale(img, (img.get_width() *
                                                              int(tile_size / img.get_height()), tile_size))
            else:
                self.res[iden] = img

        if self.res_type == ResType.SOUND:
            self.res[iden] = pygame.mixer.Sound(os.path.join('data', filename))

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
    def __init__(self, sheet, columns, frame_time, time_before_loop, x, y, *group):
        pygame.sprite.Sprite.__init__(self, *group)
        Tileset.__init__(self, sheet, columns)
        self.frame_time = frame_time
        self.cur_time = frame_time
        self.cur_frame = 0
        self.time_before_loop = time_before_loop
        self.cur_time_before_loop = time_before_loop
        self.image = self.tiles[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)

    def update(self, time_delta):
        self.cur_time -= time_delta
        self.cur_time_before_loop -= time_delta
        if self.cur_time < 0:
            if self.cur_time_before_loop < 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.tiles)
                self.cur_time = self.frame_time
                self.image = self.tiles[self.cur_frame]
                if self.cur_frame == 0:
                    self.cur_time_before_loop = self.time_before_loop


class Tile:
    def __init__(self, tile_type=TileType.FIELD):
        self.tile_type = tile_type
        self.unit = None
        self.walkable = False


class Unit(AnimatedSprite):
    def __init__(self, unit_type, tex_type, tex_holder, columns, frame_time, tbl, x, y,
                 turn, tile_speed, attack_range, hp, attack_dmg, armor, board, canvas):
        AnimatedSprite.__init__(self, tex_holder.get(tex_type), columns, frame_time, tbl, x, y, board.units)
        self.unit_type = unit_type

        self.wound_img = tex_holder.get(Textures.WOUND)
        self.wound_rect = self.wound_img.get_rect()

        self.aim_img = tex_holder.get(Textures.AIM)
        self.aim_rect = self.aim_img.get_rect()

        blood_img = tex_holder.get(Textures.BLOOD)
        self.blood_set = Tileset(blood_img, 3)

        self.board = board

        self.wound_time = 1.5
        self.wound_cur = self.wound_time
        self.rec_dmg = 0

        self.tar_coords = (x, y)

        self.tile_speed = tile_speed
        self.moving_speed = 250
        self.turn = turn
        self.moved = False
        self.attack_range = attack_range
        self.has_attacked = False
        self.under_attack = False

        self.health_capacity = hp
        self.current_health = self.health_capacity
        hp_bar_rect = pygame.Rect((0, 0), (65, 10))
        self.hp_bar = pygame_gui.elements.UIWorldSpaceHealthBar(relative_rect=hp_bar_rect,
                                                                sprite_to_monitor=self,
                                                                manager=canvas)
        self.attack_dmg = attack_dmg
        self.armor = armor

        self.enemies_in_range = []
        self.walkable_tiles = []

    def light_walkable_tiles(self):
        if self.moved:
            return
        self.get_walkable_tiles()
        for tile in self.walkable_tiles:
            self.board.cells[tile[1]][tile[0]].walkable = True

    def get_walkable_tiles(self):
        self.walkable_tiles.clear()
        unit_pos = self.board.get_cell(self.tar_coords)
        for row in range(self.board.height):
            for column in range(self.board.width):
                dis_x = abs(unit_pos[0] - column)
                dis_y = abs(unit_pos[1] - row)
                if dis_x + dis_y <= self.tile_speed:
                    if self.board.cells[row][column].tile_type != TileType.ROCK and not \
                            self.board.cells[row][column].unit:
                        self.walkable_tiles.append((column, row))

    def get_enemies(self, unit_pos=None):
        self.enemies_in_range.clear()
        if self.has_attacked:
            return
        if not unit_pos:
            unit_pos = self.board.get_cell(self.tar_coords)
        for target in self.board.units:
            if target.turn != self.turn:
                target_pos = self.board.get_cell(target.tar_coords)
                dis_x = abs(unit_pos[0] - target_pos[0])
                dis_y = abs(unit_pos[1] - target_pos[1])
                if dis_x + dis_y <= self.attack_range:
                    self.enemies_in_range.append(target)
                    target.under_attack = True

    def attack(self, tar, show_effects=True):
        self.has_attacked = True
        tar_cell = tar.board.get_cell(tar.tar_coords)
        tar_tile = tar.board.cells[tar_cell[1]][tar_cell[0]]

        dmg = self.attack_dmg - tar.armor - TILE_DEFENCE[tar_tile.tile_type]

        if dmg >= 1:
            tar.current_health -= dmg
            if show_effects:
                tar.rec_dmg = dmg

        if tar.current_health <= 0:
            tar.kill()
            tar_tile.unit = None
            if show_effects:
                tar.hp_bar.hide()
                create_particle(tar.tar_coords, self.blood_set, -2, 2, -2, 2, 1, 2, 20, self.board.particles)

    def update(self, time_delta):
        self.cur_time -= time_delta
        self.cur_time_before_loop -= time_delta
        if self.cur_time < 0:
            if self.cur_time_before_loop < 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.tiles)
                self.cur_time = self.frame_time
                self.image = self.tiles[self.cur_frame]
                if self.cur_frame == 0:
                    self.cur_time_before_loop = self.time_before_loop

        if self.rec_dmg:
            self.wound_cur -= time_delta
            if self.wound_cur < 0:
                self.wound_cur = self.wound_time
                self.rec_dmg = 0
                create_particle(self.rect.center, self.blood_set, -2, 2, -2, 2, 1, 2, 10, self.board.particles)

        if self.rect.x != self.tar_coords[0]:
            self.rect.x = round(move_towards(self.rect.x, self.tar_coords[0], self.moving_speed * time_delta))

        elif self.rect.y != self.tar_coords[1]:
            self.rect.y = round(move_towards(self.rect.y, self.tar_coords[1], self.moving_speed * time_delta))

    def draw(self, target):
        target.blit(self.image, self.rect)
        if self.rec_dmg:
            self.wound_rect.center = self.rect.center
            target.blit(self.wound_img, self.wound_rect)
            wound_lvl_f = pygame.font.Font(None, 32)
            wound_lvl_t = wound_lvl_f.render(str(self.rec_dmg), True, pygame.Color("red"))
            target.blit(wound_lvl_t, (self.rect.topleft[0], self.rect.topleft[1] + 6))
        if self.under_attack:
            self.aim_rect.center = self.rect.center
            target.blit(self.aim_img, self.aim_rect)


class Titles:
    def __init__(self, text, delay, snd_holder):
        self.typing_sound = snd_holder.get(Sounds.TYPING)
        self.text = text
        self.delay = delay
        self.cur_time = 0
        self.pointer = 0
        self.lines = [""]
        self.font = pygame.font.Font(None, 30)
        self.stop = False
        self.shown = False

    def update(self, time_delta):
        if not self.stop:
            self.cur_time += time_delta
            if self.cur_time >= self.delay:
                if self.pointer < len(self.text):
                    if self.text[self.pointer] == '\n':
                        self.lines.append("")
                    elif self.text[self.pointer] == '@':
                        self.stop = True
                        self.pointer += 1
                    else:
                        self.typing_sound.play()
                        self.lines[-1] += self.text[self.pointer]
                        self.cur_time = 0
                    self.pointer += 1

    def render(self, screen):
        if not self.shown:
            height = screen.get_height() // 4 + 20 * len(self.lines)
            surf = pygame.Surface((screen.get_width(), height))
            for i, line in enumerate(self.lines):
                txt_surf = self.font.render(line, True, pygame.Color("white"))
                txt_rect = txt_surf.get_rect()
                txt_rect.center = (surf.get_width() // 2, 50 + i * 30)
                surf.blit(txt_surf, txt_rect)
            screen.blit(surf, (0, screen.get_height() - height))

    def next_page(self):
        if self.stop:
            if self.pointer >= len(self.text) - 1:
                self.shown = True
            else:
                self.stop = False
                self.lines = [""]


class Intro:
    def __init__(self, tex_holder, snd_holder, lang="ru"):
        with open(f"data/intro_titles_{lang}.txt", encoding='utf8') as file:
            titles_text = file.read()[:-1]
        self.titles = Titles(titles_text, 0.1, snd_holder)
        self.break_sound = snd_holder.get(Sounds.BREAK)
        self.show_intro = False
        self.satan_img = tex_holder.get(Textures.SATAN)
        self.satan_img = pygame.transform.scale(self.satan_img, (self.satan_img.get_width() * 0.7,
                                                                 self.satan_img.get_height() * 0.7))
        self.satan_rect = self.satan_img.get_rect()
        self.background_img = tex_holder.get(Textures.BACKGROUND)
        self.background_rect = self.background_img.get_rect()
        self.scrooge_img = tex_holder.get(Textures.SCROOGE)
        self.scrooge_img = pygame.transform.scale(self.scrooge_img, (self.scrooge_img.get_width() * 0.7,
                                                                     self.scrooge_img.get_height() * 0.7))
        self.scrooge_rect = self.scrooge_img.get_rect()
        self.vs_img = tex_holder.get(Textures.VS)
        self.vs_img = pygame.transform.scale(self.vs_img, (self.vs_img.get_width() * 0.7,
                                                           self.vs_img.get_height() * 0.7))
        self.vs_rect = self.vs_img.get_rect()

        self.background_rect.center = (400, -self.background_rect.height // 2)
        self.scrooge_rect.bottomleft = (-self.scrooge_rect.width, 600)
        self.satan_rect.bottomright = (800 + self.scrooge_rect.width, 600)
        self.vs_rect.center = (400, -self.vs_rect.height // 2)

        self.shown = False
        self.hide = False

    def update(self, time_delta):
        if not self.shown:
            self.titles.update(time_delta)
            if self.titles.shown:
                self.show_intro = True
                if self.show_intro:
                    if self.background_rect.center[1] < 300:
                        self.background_rect.y += 1000 * time_delta
                    elif self.scrooge_rect.left < -20 or self.satan_rect.right > 820:
                        if self.scrooge_rect.left < -20:
                            self.scrooge_rect.x += 1000 * time_delta
                        if self.satan_rect.right > 820:
                            self.satan_rect.x -= 1000 * time_delta
                    elif self.vs_rect.center[1] < 300:
                        self.vs_rect.y += 1000 * time_delta
                    else:
                        self.shown = True
                        self.break_sound.play()

    def render(self, screen):
        if not self.hide:
            self.titles.render(screen)
            screen.blit(self.background_img, self.background_rect)
            screen.blit(self.scrooge_img, self.scrooge_rect)
            screen.blit(self.satan_img, self.satan_rect)
            screen.blit(self.vs_img, self.vs_rect)


class OverScreen:
    def __init__(self, manager):
        panel_rect = pygame.Rect((100, 50), (600, 500))
        self.panel = pygame_gui.elements.UIPanel(relative_rect=panel_rect, starting_layer_height=0,
                                                 manager=manager)
        new_game_rect = pygame.Rect((200, 300), (200, 40))
        self.new_game = pygame_gui.elements.UIButton(relative_rect=new_game_rect, container=self.panel,
                                                     manager=manager, text="lang.new_game")
        self.exit_game = pygame_gui.elements.UIButton(relative_rect=new_game_rect.move(0, 40), container=self.panel,
                                                      manager=manager, text="lang.exit")
        self.game_over = pygame_gui.elements.UILabel(relative_rect=new_game_rect.move(0, -200), container=self.panel,
                                                     manager=manager, text="lang.over")

    def hide(self):
        self.panel.hide()

    def show(self):
        self.panel.show()


class VictoryScreen:
    def __init__(self, manager, tex_holder):
        self.medals = Tileset(tex_holder.get(Textures.MEDALS), 3)

        panel_rect = pygame.Rect((100, 50), (600, 500))
        self.panel = pygame_gui.elements.UIPanel(relative_rect=panel_rect, starting_layer_height=0,
                                                 manager=manager)
        new_game_rect = pygame.Rect((200, 300), (200, 40))
        self.next_level = pygame_gui.elements.UIButton(relative_rect=new_game_rect.move(0, -40), container=self.panel,
                                                       manager=manager, text="lang.next_lvl")
        self.new_game = pygame_gui.elements.UIButton(relative_rect=new_game_rect, container=self.panel,
                                                     manager=manager, text="lang.new_game")
        self.exit_game = pygame_gui.elements.UIButton(relative_rect=new_game_rect.move(0, 40), container=self.panel,
                                                      manager=manager, text="lang.exit")
        self.victory = pygame_gui.elements.UILabel(relative_rect=new_game_rect.move(0, -200), container=self.panel,
                                                   manager=manager, text="lang.victory")
        self.losses = pygame_gui.elements.UILabel(relative_rect=new_game_rect.move(-100, -160), container=self.panel,
                                                  manager=manager, text="lang.losses")
        self.time = pygame_gui.elements.UILabel(relative_rect=new_game_rect.move(100, -160), container=self.panel,
                                                manager=manager, text="lang.time")
        medal_rect = pygame.Rect((160, 170), (80, 80))
        self.losses_medal = pygame_gui.elements.UIImage(relative_rect=medal_rect, image_surface=self.medals.tiles[2],
                                                        container=self.panel, manager=manager)
        self.time_medal = pygame_gui.elements.UIImage(relative_rect=medal_rect.move(200, 0),
                                                      image_surface=self.medals.tiles[1],
                                                      container=self.panel, manager=manager)

        self.time_rate = 0
        self.losses_rate = 0

    def hide(self):
        self.panel.hide()

    def show(self):
        self.panel.show()

    def update_rates(self, losses, time):
        if losses == 0:
            self.losses_rate = 2
        elif losses < 3:
            self.losses_rate = 1
        else:
            self.losses_rate = 0

        if time <= 3:
            self.time_rate = 2
        elif time <= 6:
            self.time_rate = 1
        else:
            self.time_rate = 0

        self.losses_medal.set_image(self.medals.tiles[self.losses_rate])
        self.time_medal.set_image(self.medals.tiles[self.time_rate])


class GameUI:
    def __init__(self, manager):
        end_turn_btn_rect = pygame.Rect((800 - 100, 600 - 50), (100, 50))
        self.end_turn_btn = pygame_gui.elements.UIButton(relative_rect=end_turn_btn_rect, text='lang.finish',
                                                         manager=manager)
        cur_turn_label_rect = pygame.Rect((800 // 2 - 100, 0), (200, 20))
        self.cur_turn = pygame_gui.elements.UILabel(relative_rect=cur_turn_label_rect,
                                                    text="lang.current_turn",
                                                    manager=manager)
        self.cur_turn_num = pygame_gui.elements.UILabel(relative_rect=cur_turn_label_rect.move(0, 20),
                                                        text="1",
                                                        manager=manager)

        game_dur_label_rect = pygame.Rect((0, 0), (200, 20))
        self.game_dur_label = pygame_gui.elements.UILabel(relative_rect=game_dur_label_rect,
                                                          text="lang.game_duration",
                                                          manager=manager)
        self.game_dur = pygame_gui.elements.UILabel(relative_rect=game_dur_label_rect.move(0, 20),
                                                    text="1",
                                                    manager=manager)


class AI:
    def __init__(self, game_manager, turn):
        self.gm = game_manager
        self.turn = turn
        self.brd_width = self.gm.board.width
        self.brd_height = self.gm.board.height
        self.brd_center = (self.brd_width // 2, self.brd_height // 2)

    def minimax(self, deph, is_max, alpha, beta):
        if not deph:
            return -self.weight_board()
        if is_max:
            turn = self.turn
        else:
            turn = 1
        for unit in self.gm.board.units:
            if unit.turn == turn:
                steps_stack = self.get_all_moves(unit)
                if is_max:
                    best_weight = -self.weight_board()
                    for i in range(len(steps_stack)):
                        new_move = steps_stack.pop()
                        self.do_step(new_move)
                        best_weight = max(best_weight, self.minimax(deph - 1, not is_max, alpha, beta))
                        self.undo_step(new_move)
                        alpha = max(alpha, best_weight)
                        if beta <= alpha:
                            return best_weight
                else:
                    best_weight = self.weight_board()
                    for i in range(len(steps_stack)):
                        new_move = steps_stack.pop()
                        self.do_step(new_move)
                        best_weight = min(best_weight, self.minimax(deph - 1, not is_max, alpha, beta))
                        self.undo_step(new_move)
                        beta = min(beta, best_weight)
                        if beta <= alpha:
                            return best_weight
                return best_weight
        return self.weight_board()

    def step(self):
        for unit in self.gm.board.units:
            if unit.turn == self.turn:
                steps_stack = self.get_all_moves(unit)
                best_move = None
                best_weight = -self.weight_board()
                for i in range(len(steps_stack)):
                    new_move = steps_stack.pop()
                    self.do_step(new_move)
                    brd_weight = self.minimax(3, True, -10000, 10000)
                    self.undo_step(new_move)
                    if brd_weight > best_weight:
                        best_move = new_move
                        best_weight = brd_weight
                if best_move:
                    best_move.etc.is_final = True
                    if best_move.etc.attack_step:
                        best_move.etc.attack_step.etc.is_final = True
                    self.do_step(best_move)
        self.gm.end_step()

    def get_all_moves(self, unit):
        steps_stack = []
        cell = self.gm.board.get_cell(unit.tar_coords)
        unit.get_walkable_tiles()
        for move in unit.walkable_tiles:
            move_info = DotDict()
            move_info.is_final = False
            move_info.attack_step = None
            new_move = StepData(AIStepType.MOVE, cell, move, move_info)
            steps_stack.append(new_move)
            unit.get_enemies(move)
            for enemy in unit.enemies_in_range:
                attack_info = DotDict()
                attack_info.tar = enemy
                attack_info.is_final = False
                attack_move = StepData(AIStepType.ATTACK, move,
                                       self.gm.board.get_cell(enemy.tar_coords), attack_info)
                new_move.etc.attack_step = attack_move
                steps_stack.append(new_move)
        unit.get_enemies()
        for enemy in unit.enemies_in_range:
            attack_info = DotDict()
            attack_info.tar = enemy
            attack_info.is_final = False
            new_move = StepData(AIStepType.ATTACK, cell,
                                self.gm.board.get_cell(enemy.tar_coords), attack_info)
            steps_stack.append(new_move)
        return steps_stack

    def weight_board(self):
        weight = 0
        max_center_dis = self.brd_center[0] + self.brd_center[1]
        for row in range(self.brd_height):
            for column in range(self.brd_width):
                tile = self.gm.board.cells[row][column]
                unit = tile.unit
                if unit:
                    center_dis = (abs(column - self.brd_center[0]) +
                                  abs(row - self.brd_center[1]))
                    unit_hp_coeff = val_to_coeff(unit.current_health, 0,
                                                 unit.health_capacity, 0.2, 2)
                    unit_pos_coeff = val_to_coeff(max_center_dis - center_dis, 0,
                                                  max_center_dis, 1., 1.1)
                    unit_weight = (TILE_COEFF[tile.tile_type] * unit_hp_coeff *
                                   unit_pos_coeff * UNIT_SIG[unit.unit_type])
                    if unit.turn == self.turn:
                        weight -= unit_weight
                    else:
                        weight += unit_weight
        return weight

    def do_step(self, step):
        unit = self.gm.board.cells[step.orig[1]][step.orig[0]].unit
        if step.type == AIStepType.MOVE:
            self.gm.board.cells[step.orig[1]][step.orig[0]].unit = None
            self.gm.board.cells[step.dest[1]][step.dest[0]].unit = unit
            unit.tar_coords = self.gm.board.get_cell_coords(step.dest)
            unit.moved = True
            if step.etc.attack_step:
                if step.etc.is_final:
                    step.etc.attack_step.is_final = True
                self.do_step(step.etc.attack_step)
        if step.type == AIStepType.ATTACK:
            orig_hp = step.etc.tar.current_health
            unit.attack(step.etc.tar, show_effects=step.etc.is_final)
            dmg = orig_hp - step.etc.tar.current_health
            step.etc.dmg = dmg

    def undo_step(self, step):
        if step.type == AIStepType.MOVE:
            unit = self.gm.board.cells[step.dest[1]][step.dest[0]].unit
            self.gm.board.cells[step.dest[1]][step.dest[0]].unit = None
            self.gm.board.cells[step.orig[1]][step.orig[0]].unit = unit
            unit.tar_coords = self.gm.board.get_cell_coords(step.orig)
            unit.moved = False
            if step.etc.attack_step:
                self.undo_step(step.etc.attack_step)
        if step.type == AIStepType.ATTACK:
            step.etc.tar.current_health += step.etc.dmg
            if not step.etc.tar.alive():
                self.gm.board.units.add(step.etc.tar)
                self.gm.board.cells[step.dest[1]][step.dest[0]].unit = step.etc.tar


class GameManager:
    def __init__(self, map_name, lang='ru'):
        self.map_name = map_name
        self.screen_sizes = 800, 600
        self.screen = pygame.display.set_mode(self.screen_sizes)
        self.selected_unit = None
        self.moving = False
        self.running = True
        self.is_game = False
        self.is_intro = True
        self.prev_pos = 0, 0
        self.light_color = (128, 128, 255, 255)

        self.tex_holder = ResourceHolder(ResType.TEXTURE)
        self.snd_holder = ResourceHolder(ResType.SOUND)
        self.load_textures(tile_size=64)
        self.load_sounds()

        self.ui_manager = pygame_gui.UIManager(self.screen_sizes, starting_language=lang,
                                               translation_directory_paths=["data/translations/"])
        self.game_ui = GameUI(self.ui_manager)
        self.over_screen = OverScreen(self.ui_manager)
        self.over_screen.hide()
        self.victory_screen = VictoryScreen(self.ui_manager, self.tex_holder)
        self.victory_screen.hide()
        self.board = load_board(map_name, self.tex_holder)
        self.cur_turn = 1
        self.player_units_count = 6

        self.game_duration = 0

        self.ai = AI(self, 2)

        self.intro = Intro(self.tex_holder, self.snd_holder, lang)

    def load_textures(self, tile_size=64):
        self.tex_holder.load(Textures.GROUND, "ground.png", tile_size)
        self.tex_holder.load(Textures.ELF, "elf.png", tile_size)
        self.tex_holder.load(Textures.KNIGHT, "knight.png", tile_size)
        self.tex_holder.load(Textures.MAG, "mag.png", tile_size)
        self.tex_holder.load(Textures.GOBLIN, "goblin.png", tile_size)
        self.tex_holder.load(Textures.SCULL, "scull.png", tile_size)
        self.tex_holder.load(Textures.WIZARD, "wizard.png", tile_size)
        self.tex_holder.load(Textures.DEMON, "demon.png", tile_size)
        self.tex_holder.load(Textures.HERO, "hero.png", tile_size)
        self.tex_holder.load(Textures.AIM, "aim.png", tile_size // 2)
        self.tex_holder.load(Textures.WOUND, "wound.png", tile_size // 2)
        self.tex_holder.load(Textures.BLOOD, "blood.png", tile_size // 4)
        self.tex_holder.load(Textures.MEDALS, "medals.png", tile_size)
        self.tex_holder.load(Textures.SATAN, "satan.png"),
        self.tex_holder.load(Textures.SCROOGE, "scrooge.png"),
        self.tex_holder.load(Textures.VS, "vs.png"),
        self.tex_holder.load(Textures.BACKGROUND, "background.png")

        self.tex_holder.add(Textures.GROUND_LIGHTED,
                            change_color(self.tex_holder.get(Textures.GROUND), *self.light_color))

    def load_sounds(self):
        self.snd_holder.load(Sounds.TYPING, "typing.mp3")
        self.snd_holder.load(Sounds.BREAK, "break.flac")

    def on_cell_click(self, cell):
        if self.is_game:
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
                    self.selected_unit.light_walkable_tiles()
                else:
                    # selected unit is enemy
                    if self.selected_unit:
                        if tile.unit in self.selected_unit.enemies_in_range:
                            self.selected_unit.attack(tile.unit)
                            self.selected_unit.moved = True
                        self.selected_unit = None
            else:
                if self.board.cells[cell[1]][cell[0]].walkable and self.selected_unit:
                    if not self.selected_unit.moved:
                        # moving unit
                        cur_cell = self.board.get_cell(self.selected_unit.tar_coords)
                        self.board.cells[cur_cell[1]][cur_cell[0]].unit = None
                        self.board.cells[cell[1]][cell[0]].unit = self.selected_unit
                        # self.selected_unit.move(self.board.get_cell_coords(cell))
                        self.selected_unit.tar_coords = self.board.get_cell_coords(cell)
                        self.selected_unit.moved = True
                        self.selected_unit = None
                        self.board.reset_units()
                        self.board.reset_tiles()

    def on_mouse_button_down(self, event):
        if self.is_game:
            if event.button == 3:
                self.moving = True
                self.prev_pos = event.pos
            elif event.button == 1:
                cell = self.board.get_cell(self.board.translate_point(*event.pos))
                if cell:
                    self.on_cell_click(cell)

    def on_mouse_button_up(self, event):
        if self.is_game:
            if event.button == 3:
                self.moving = False

    def on_mouse_motion(self, event):
        if self.is_game:
            self.board.outlined_cell = self.board.get_cell(self.board.translate_point(*event.pos))
            if self.moving:
                self.board.offset_x -= self.prev_pos[0] - event.pos[0]
                self.board.offset_y -= self.prev_pos[1] - event.pos[1]
                self.prev_pos = event.pos

    def on_mouse_wheel(self, event):
        if self.is_game:
            mp = pygame.mouse.get_pos()
            mp_origin = self.board.translate_point(*mp)
            self.board.scale = max(0.625, min(2., self.board.scale * exp(event.y * 0.1)))
            self.board.offset_x = mp[0] - mp_origin[0] * self.board.scale
            self.board.offset_y = mp[1] - mp_origin[1] * self.board.scale

    def on_key_down(self, event):
        if event.key == pygame.K_SPACE:
            if self.is_game:
                self.end_step()
            if self.is_intro:
                self.intro.titles.next_page()
                if self.intro.shown:
                    self.intro.hide = True
                    self.is_game = True

    def on_ui_button_pressed(self, event):
        if event.ui_element == self.game_ui.end_turn_btn and self.is_game:
            self.end_step()

        if event.ui_element in (self.victory_screen.exit_game, self.over_screen.exit_game):
            self.running = False

        if event.ui_element in (self.victory_screen.new_game, self.over_screen.new_game):
            self.board = load_board(self.map_name, self.tex_holder)
            self.cur_turn = 1
            self.selected_unit = None
            self.game_duration = 0
            self.is_game = True
            self.victory_screen.hide()
            self.over_screen.hide()

        if event.ui_element == self.victory_screen.next_level:
            pass

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
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.on_ui_button_pressed(event)
            self.ui_manager.process_events(event)

    def end_step(self):
        self.board.reset_tiles()
        self.selected_unit = None
        if self.cur_turn == 1:
            self.cur_turn = 2
            self.ai.step()
        else:
            self.cur_turn = 1
        for unit in self.board.units:
            unit.moved = False
            unit.under_attack = False
            unit.has_attacked = False
        self.game_ui.cur_turn_num.set_text(str(self.cur_turn))

    def calc_losses(self):
        alive = 0
        for unit in self.board.units:
            if unit.turn == 1:
                alive += 1
        return self.player_units_count - alive

    def start_game(self):
        clock = pygame.time.Clock()
        while self.running:
            time_delta = clock.tick(FPS) / 1000.
            if self.is_game:
                self.game_duration += time_delta
            if self.is_over():
                self.over_screen.show()
                self.is_game = False
            elif self.is_victory():
                self.victory_screen.show()
                self.is_game = False
                self.victory_screen.update_rates(self.calc_losses(), int(self.game_duration // 60))
            self.game_ui.game_dur.set_text(str(int(self.game_duration // 60)))
            self.process_events()
            self.screen.fill((0, 0, 0))
            self.board.update(time_delta)
            self.board.render(self.screen)
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            self.intro.update(time_delta)
            self.intro.render(self.screen)
            pygame.display.flip()
            pygame.display.set_caption(f'TBS. FPS: {int(clock.get_fps())}')

    def is_over(self):
        is_over = True
        for unit in self.board.units:
            if unit.unit_type == UnitType.HERO:
                is_over = False
                break
        return is_over

    def is_victory(self):
        is_victory = True
        for unit in self.board.units:
            if unit.unit_type == UnitType.DEMON:
                is_victory = False
                break
        return is_victory


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
        self.particles = pygame.sprite.Group()
        self.outline_width = 2
        self.cell_size = 30
        self.outlined_cell = None
        self.selected_unit = None
        self.canvas = pygame_gui.UIManager(self.get_total_board_size())
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

    def update(self, time_delta):
        self.units.update(time_delta)
        self.particles.update(time_delta)
        self.canvas.update(time_delta)

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
            unit.draw(buffer)
        self.particles.draw(buffer)
        self.draw_outline(self.outlined_cell, pygame.Color("red"), buffer)
        self.canvas.draw_ui(buffer)
        buffer = pygame.transform.scale(buffer, (buffer.get_width() * self.scale, buffer.get_height() * self.scale))
        target.blit(buffer, (self.offset_x, self.offset_y))

    def draw_outline(self, cell, color, surface):
        if cell:
            x, y = self.get_cell_coords(cell)
            size = self.outline_width + self.cell_size + 2.5
            outline_rect = pygame.Rect((x, y), (size, size)).move(-2.5, -2.5)
            pygame.draw.rect(surface, color, outline_rect, width=self.outline_width)

    def get_cell(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        column = mouse_x // (self.cell_size + self.outline_width * 2)
        row = mouse_y // (self.cell_size + self.outline_width * 2)
        if (0 <= column < self.width and 0 <= row < self.height and
                0 <= mouse_x - column * (
                        self.cell_size + 2 * self.outline_width) - self.outline_width <= self.cell_size and
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
    game_manager = GameManager("map1.csv", lang="ru")
    game_manager.start_game()
