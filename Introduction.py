import pygame
import sys
import os
import turtle
import colorsys
import pygame_gui
from Game_Over import GameOver
from Titles_show import Titles
from Pause import Pause
import zipfile

pygame.init()
size = width, height = 1000, 650
screen = pygame.display.set_mode(size, pygame.HIDDEN)
pygame.display.set_caption('Начало')
screen.fill((0, 0, 0))
FPS = 50
clock = pygame.time.Clock()
directory = os.path.join(os.getcwd(), 'data')
LANGUAGE = 'Русский'
SOUND_TITLES = True

from FNaF_Easter_Egg import easter_egg


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, where):
        super().__init__(where)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.transform.scale(pygame.image.load(image_file), (width, height))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


walkLeft = [load_image('L1_mainhero.png'), load_image('L2_mainhero.png'),
            load_image('L3_mainhero.png'),
            load_image('L4_mainhero.png'), load_image('L5_mainhero.png'),
            load_image('L6_mainhero.png'),
            load_image('L7_mainhero.png'), load_image('L8_mainhero.png'),
            load_image('L9_mainhero.png'),
            load_image('L10_mainhero.png'), load_image('L11_mainhero.png'),
            load_image('L12_mainhero.png')]
walkRight = [pygame.transform.flip(load_image('L1_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L2_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L3_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L4_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L5_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L6_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L7_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L8_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L9_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L10_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L11_mainhero.png'), 90, 0),
             pygame.transform.flip(load_image('L12_mainhero.png'), 90, 0)]
stayLeft = load_image('L5_mainhero.png')
stayRight = pygame.transform.flip(load_image('L5_mainhero.png'), 90, 0)

walkLeftBig = [load_image('L1_mainherobig.png'), load_image('L2_mainherobig.png'),
               load_image('L3_mainherobig.png'),
               load_image('L4_mainherobig.png'), load_image('L5_mainherobig.png'),
               load_image('L6_mainherobig.png'),
               load_image('L7_mainherobig.png'), load_image('L8_mainherobig.png'),
               load_image('L9_mainherobig.png'),
               load_image('L10_mainherobig.png'), load_image('L11_mainherobig.png'),
               load_image('L12_mainherobig.png')]
walkRightBig = [pygame.transform.flip(load_image('L1_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L2_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L3_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L4_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L5_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L6_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L7_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L8_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L9_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L10_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L11_mainherobig.png'), 90, 0),
                pygame.transform.flip(load_image('L12_mainherobig.png'), 90, 0)]
stayLeftBig = load_image('L5_mainherobig.png')
stayRightBig = pygame.transform.flip(load_image('L5_mainherobig.png'), 90, 0)

snowdrift = pygame.transform.flip(load_image('Snowdrift.png'), 90, 0)
bg = load_image('bg_start.png')
road = pygame.transform.scale(load_image('Road.png'), (450, 900))
house = pygame.transform.scale(load_image('House outside.png'), (1000, 900))
lobby = pygame.transform.scale(load_image('Lobby.jpg'), (1000, 650))
kitchen = pygame.transform.scale(load_image('Kitchen.jpg'), (1000, 650))
cupcake = pygame.transform.scale(load_image('First Cupcake.png'), (25, 25))
death = pygame.transform.flip(pygame.transform.scale(load_image('Death.png'), (500, 650)), 90, 0)

fname = os.path.join(os.getcwd(), 'data', 'FnafJump2.zip')
directory = os.path.join(os.getcwd(), 'data')
with zipfile.ZipFile(fname, "r") as f:
    names_freddy = sorted(f.namelist())
    f.extractall(directory)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, where, *group):
        super().__init__(*group)
        self.i = 0
        self.where = where
        if where == 'right':
            self.image = pygame.transform.scale(stayRight, (100, 163))
        else:
            self.image = pygame.transform.scale(stayLeft, (100, 163))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.play = 0
        self.second_room = False

    def update(self, where, move=True):
        global x, outside, inside, show_titles
        x_new = x
        if move:
            self.i += 1
            self.i = self.i % len(walkRight)
            if self.where != where:
                self.i = 0
                self.where = where
            if outside:
                if not self.play and -150 <= x <= 900:
                    snow.play(-1)
                    self.play = 1
                elif not (-150 <= x <= 850):
                    snow.stop()
                    self.play = 0
                if where == 'right':
                    self.image = pygame.transform.scale(walkRight[self.i], (100, 163))
                    x_new += 4
                else:
                    self.image = pygame.transform.scale(walkLeft[self.i], (100, 163))
                    x_new -= 4
            else:
                if where == 'right':
                    self.image = walkRightBig[self.i]
                    self.rect.x += 4
                else:
                    self.image = walkLeftBig[self.i]
                    self.rect.x -= 4
        else:
            if outside:
                snow.stop()
                self.play = 0
            self.i = 0
            if outside:
                if where == 'right':
                    self.image = pygame.transform.scale(stayRight, (100, 163))
                else:
                    self.image = pygame.transform.scale(stayLeft, (100, 163))
            elif inside:
                if where == 'right':
                    self.image = stayRightBig
                else:
                    self.image = stayLeftBig
        self.mask = pygame.mask.from_surface(self.image)
        if outside:
            x_new = max(-150, x_new)
            if x_new >= 930:
                return self.change_state()
        elif inside:
            if self.rect.x >= 1001 and not self.second_room:
                self.second_room = True
                self.rect.x = 1
            elif self.second_room and self.rect.x >= 865:
                self.rect.x = 865
            elif self.second_room and self.rect.x <= -20:
                self.rect.x = 950
                self.second_room = False
            elif not self.second_room and self.rect.x <= 0:
                self.rect.x = 0
            x_new = self.rect.x
        if (outside and 300 <= x_new <= 400 and not first_titles_shown) or \
                (outside and -150 <= x_new <= -80 and not additional_titles_shown) or \
                (inside and self.second_room and 100 <= x_new <= 200 and not kitchen_titles_shown) \
                or (inside and self.second_room and 100 <= x_new <= 200 and kitchen_titles_shown
                    and not kitchen_titles_second_shown) or \
                (inside and 800 <= x_new <= 900 and not self.second_room and
                 kitchen_titles_second_shown and not lobby_titles_shown) or \
                (inside and 0 <= x_new <= 250 and lobby_titles_shown and not self.second_room):
            show_titles = True
        return x_new, self.rect.y

    def change_state(self):
        global x, outside, inside, all_sprites, hero, y
        x = 200
        y = 350
        screen.fill('black')
        pygame.display.flip()
        snow.stop()
        outside, inside = inside, outside
        house_door_open.play()
        house_door_close.play()
        clock.tick(0.5)
        all_sprites = pygame.sprite.Group()
        hero = Hero(x, y, go_where, all_sprites)
        return x, self.rect.y

    def pause(self):
        self.play = 0
        snow.stop()


all_sprites = pygame.sprite.Group()
portal = pygame.sprite.Group()
portal_blue = AnimatedSprite(pygame.transform.scale(load_image('Mirror portal.png'),
                                                    (1000, 1000)), 8, 3, 100, 200, portal)
portal_breaks = pygame.sprite.Group()
portal_breaks_blue = AnimatedSprite(pygame.transform.scale(load_image('Mirror portal breaks.png'),
                                                           (1500, 1500)), 8, 6, 100, 200,
                                    portal_breaks)
snow = pygame.mixer.Sound(os.path.join(directory, 'Snowfootsteps.mp3'))
car_door_open = pygame.mixer.Sound(os.path.join(directory, 'Car door open.mp3'))
car_door_close = pygame.mixer.Sound(os.path.join(directory, 'Car door close.mp3'))
car_ride_away = pygame.mixer.Sound(os.path.join(directory, 'Car ride away.mp3'))
house_door_close = pygame.mixer.Sound(os.path.join(directory, 'House door closing.wav'))
house_door_open = pygame.mixer.Sound(os.path.join(directory, 'House door open.wav'))
portal_enter = pygame.mixer.Sound(os.path.join(directory, 'Portal enter.mp3'))
typing = pygame.mixer.Sound(os.path.join(directory, 'Typing.mp3'))
end_typing = pygame.mixer.Sound(os.path.join(directory, 'End typing.mp3'))
mirror_breaks = pygame.mixer.Sound(os.path.join(directory, 'Mirror breaks.mp3'))
before_screamer = pygame.mixer.Sound(os.path.join(directory, 'Music before freddy.mp3'))
screamer_freddy = pygame.mixer.Sound(os.path.join(directory, 'Freddy screamer.mp3'))
before_screamer.set_volume(0.5)
screamer_freddy.set_volume(0.45)
outside = True
inside = False
start_level = False
dead = False
show_titles = False
pressed_enter = False
pause = False
end_scene = False
freddy_scene = False
deleted_files = False
first_titles = Titles(
    '[Главный герой:] Чёртовы таксисты!|| &Из-за дурацких праздников они решили, что можно '
    'повысить цены в два раза!£ ' * (
            LANGUAGE == 'Русский') +
    "[Main hero:] Bloody taxi drivers!|| &They've decided that it's OK to double the price because "
    "of stupid holidays!£ " * (
            LANGUAGE == 'English'), width, height,
    os.path.join(directory, 'CinecavXSans-Regular.ttf'))
first_titles_shown = False
additional_titles = Titles(
    '[Главный герой:] Нет.| Я устал и мне пора домой.£ ' * (
            LANGUAGE == 'Русский') +
    "[Main hero:] No.| I'm tired so I need to go home.£ " * (
            LANGUAGE == 'English'), width, height,
    os.path.join(directory, 'CinecavXSans-Regular.ttf'))
additional_titles_shown = False
kitchen_titles = Titles(
    '[Главный герой:] Пожалуй, кофе на ужин будет достаточно.| &Главное выключить телефон, '
    'чтобы люди не надоедали с поздравлениями.£ ' * (
            LANGUAGE == 'Русский') +
    "[Main hero:] Well, one cup of coffee will be enough for dinner.| &The main thing is to turn "
    "off my phone so that people don't get me bored with congratulations.£ " * (
            LANGUAGE == 'English'), width, height,
    os.path.join(directory, 'CinecavXSans-Regular.ttf'))
kitchen_titles_shown = False
kitchen_titles_second = Titles(
    '[Главный герой:] Кого там еще принесло?£ ' * (
            LANGUAGE == 'Русский') +
    "[Main hero:] Who's that?£ " * (
            LANGUAGE == 'English'), width, height,
    os.path.join(directory, 'CinecavXSans-Regular.ttf'))
kitchen_titles_second_shown = False
lobby_titles = Titles(
    '[Главный герой:] Ты кто?| И что ты делаешь в моей квартире?£ '
    '[Смерть:] Я Смерть.|| Ты пожил достаточно и я пришел за тобой.£ '
    '[Главный герой:] Как?|| &Я ведь так многого еще не сделал!£ '
    '[Смерть:] Ты прожил скучную жизнь и не принес пользу никому.£ '
    '[Главный герой:] Пощади!£ '
    '[Смерть:] Хм|.|.|.||| Ладно, я позволю тебе жить, если ты исправишься и пройдешь испытания.£ '
    '[Главный герой:] Так что мне делать?£ '
    '[Смерть:] Заходи в портал.£ ' * (
            LANGUAGE == 'Русский') +
    "[Main hero:] Who are you?| What are you doing in my house?£ "
    "[Death:] I'm Death.|| You've lived long enough and I've come for you.£ "
    "[Main hero:] What?|| &I had no time and I've done nothing.£ "
    "[Death:] You have lived a boring life and have not benefited anyone.£ "
    "[Main hero:] Have mercy on me!£ "
    "[Death:] Hmm|.|.|.||| Ok, I will let you live if you improve and go through the trials.£ "
    "[Main hero:] So what should i do?£ "
    "[Смерть:] Enter the portal.£ " * (
            LANGUAGE == 'English'), width, height,
    os.path.join(directory, 'CinecavXSans-Regular.ttf'))
lobby_titles_shown = False
x, y = 200, 487
go_where = 'right'
hero = Hero(x, y, go_where, all_sprites)
end_screen = GameOver(width, height)
pause_screen = Pause(width, height)
manager_game_over = pygame_gui.UIManager((width, height))
manager_pause = pygame_gui.UIManager((width, height))
button_back_main_window = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 355, 200, 50)),
    text='На главный экран' * (LANGUAGE == 'Русский') + 'Main Window' * (LANGUAGE == 'English'),
    manager=manager_game_over
)
button_last_save = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 300, 200, 50)),
    text='К последнему сохранению' * (LANGUAGE == 'Русский') + 'Last checkpoint' * (
            LANGUAGE == 'English'),
    manager=manager_game_over
)

button_back_main_window_pause = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((25, 575, 200, 50)),
    text='На главный экран' * (LANGUAGE == 'Русский') + 'Main Window' * (LANGUAGE == 'English'),
    manager=manager_pause
)
button_last_save_pause = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((400, 270, 200, 50)),
    text='К последнему сохранению' * (LANGUAGE == 'Русский') + 'Last checkpoint' * (
            LANGUAGE == 'English'),
    manager=manager_pause
)
if SOUND_TITLES:
    button_sound_titles = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((775, 575, 200, 50)),
        text='Звук титров: включён' * (LANGUAGE == 'Русский') + 'Caption sound: on' * (
                LANGUAGE == 'English'),
        manager=manager_pause
    )
else:
    button_sound_titles = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((775, 575, 200, 50)),
        text='Звук титров: выключен' * (LANGUAGE == 'Русский') + 'Caption sound: off' * (
                LANGUAGE == 'English'),
        manager=manager_pause
    )
running = True
t = turtle.Turtle()
s = turtle.Screen()
turtle.setup(width, height)
s.bgcolor('black')
t.speed(0)
n = 200
h = 0
for j in range(185):
    t.begin_fill()
    for i in range(2):
        c = colorsys.hsv_to_rgb(h, 1, 0.8)
        h += 1 / n
        t.color(c)
        t.left(20)
        t.forward(j - i)
    t.end_fill()
turtle.bye()
screen = pygame.display.set_mode(size, pygame.SHOWN, pygame.NOFRAME)
while running:
    if freddy_scene:
        i = 0
        screen.fill('black')
        screen.blit(kitchen, (0, 0))
        screen.blit(cupcake, (975, 250))
        all_sprites.draw(screen)
        before_screamer.play()
        clock.tick(0.01894)
        screamer_freddy.play()
        while i < len(names_freddy):
            BackGround = Background(os.path.join(directory, names_freddy[i]), [0, 0])
            screen.fill([255, 255, 255])
            screen.blit(BackGround.image, BackGround.rect)
            i += 1
            pygame.display.flip()
            clock.tick(10)
        freddy_scene = False
        dead = True
        deleted_files = True
        for name in names_freddy:
            os.remove(os.path.join(directory, name))
    else:
        if not start_level:
            transparency = 0
            car_door_open.play()
            while transparency <= 300:
                if 130 < transparency < 132:
                    car_door_close.play()
                if 250 <= transparency <= 251:
                    car_ride_away.play()
                screen.fill((0, 0, 0))
                font = pygame.font.Font(None, 100)
                text = font.render("Иногда в Рождество..." * (LANGUAGE == 'Русский') +
                                   "Sometimes at Christmas..." * (LANGUAGE == 'English'), True,
                                   "white")
                text_x = width // 2 - text.get_width() // 2
                text_y = height // 2 - text.get_height() // 2 - 150
                text.set_alpha(transparency)
                screen.blit(text, (text_x, text_y))
                transparency += 1.5
                pygame.display.flip()
                clock.tick(FPS)
            transparency = 0
            while transparency <= 300:
                screen.fill((0, 0, 0))
                font = pygame.font.Font(None, 100)
                text = font.render("Иногда в Рождество..." * (LANGUAGE == 'Русский') +
                                   "Sometimes at Christmas..." * (LANGUAGE == 'English'), True,
                                   "white")
                text_x = width // 2 - text.get_width() // 2
                text_y = height // 2 - text.get_height() // 2 - 150
                text.set_alpha(250)
                screen.blit(text, (text_x, text_y))
                text = font.render("Случаются чудеса" * (LANGUAGE == 'Русский') +
                                   'Miracles happen' * (LANGUAGE == 'English'), True, "white")
                text_x = width // 2 - text.get_width() // 2
                text_y = height // 2 - text.get_height() // 2 + 100
                text.set_alpha(transparency)
                screen.blit(text, (text_x, text_y))
                transparency += 1.5
                pygame.display.flip()
                clock.tick(FPS)
            start_level = True
        if end_scene:
            running = False
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):
                pause = not pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pressed_enter = True
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element in (
                            button_back_main_window, button_last_save,
                            button_back_main_window_pause,
                            button_last_save_pause):
                        running = False
                    if event.ui_element == button_sound_titles:
                        SOUND_TITLES = not SOUND_TITLES
                        button_sound_titles.kill()
                        if SOUND_TITLES:
                            button_sound_titles = pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((775, 575, 200, 50)),
                                text='Звук титров: включён' * (
                                        LANGUAGE == 'Русский') + 'Caption sound: on' * (
                                             LANGUAGE == 'English'),
                                manager=manager_pause
                            )
                        else:
                            button_sound_titles = pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((775, 575, 200, 50)),
                                text='Звук титров: выключен' * (
                                        LANGUAGE == 'Русский') + 'Caption sound: off' * (
                                             LANGUAGE == 'English'),
                                manager=manager_pause
                            )
            manager_game_over.process_events(event)
            manager_pause.process_events(event)
        if dead:
            end_screen.update(time_delta, screen, manager_game_over)
        elif not pause:
            if not show_titles:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    go_where = 'left'
                    x, y = hero.update(go_where)
                elif keys[pygame.K_RIGHT]:
                    go_where = 'right'
                    x, y = hero.update(go_where)
                elif keys[pygame.K_e] and hero.second_room and 800 <= hero.rect.x <= 865:
                    result = easter_egg(screen, width, height)
                    if result == 1:
                        dead = True
                    if result == 2:
                        freddy_scene = True
                else:
                    x, y = hero.update(go_where, move=False)
                if outside:
                    screen.fill('black')
                    screen.blit(bg, (0, 0))
                    screen.blit(snowdrift, (50 - x, 525))
                    screen.blit(road, (-300 - x, 0))
                    screen.blit(house, (910 - x, -100))
                    all_sprites.draw(screen)
                elif inside:
                    screen.fill('black')
                    if not hero.second_room:
                        screen.blit(lobby, (0, 0))
                        if kitchen_titles_second_shown and not lobby_titles_shown:
                            screen.blit(death, (0, 0))
                        elif lobby_titles_shown:
                            portal.draw(screen)
                            portal.update()
                    else:
                        screen.blit(kitchen, (0, 0))
                        screen.blit(cupcake, (975, 250))
                    all_sprites.draw(screen)
            else:
                if outside:
                    x, y = hero.update(go_where, move=False)
                    screen.fill('black')
                    screen.blit(bg, (0, 0))
                    screen.blit(snowdrift, (50 - x, 525))
                    screen.blit(road, (-300 - x, 0))
                    screen.blit(house, (910 - x, -100))
                    all_sprites.draw(screen)
                    if 300 <= x <= 400 and not first_titles_shown:
                        if SOUND_TITLES:
                            first_titles_shown, pressed_enter = first_titles.update(screen, clock,
                                                                                    pressed_enter,
                                                                                    typing,
                                                                                    end_typing)
                        else:
                            first_titles_shown, pressed_enter = first_titles.update(screen, clock,
                                                                                    pressed_enter)
                        if first_titles_shown:
                            show_titles = False
                            pressed_enter = False
                    if -150 <= x <= -80 and not additional_titles_shown:
                        if SOUND_TITLES:
                            additional_titles_shown, pressed_enter = \
                                additional_titles.update(screen,
                                                         clock,
                                                         pressed_enter,
                                                         typing,
                                                         end_typing)
                        else:
                            additional_titles_shown, pressed_enter = additional_titles.update(
                                screen,
                                clock,
                                pressed_enter)
                        if additional_titles_shown:
                            show_titles = False
                            pressed_enter = False
                elif inside:
                    screen.fill('black')
                    if not hero.second_room and 0 <= x <= 250 and lobby_titles_shown:
                        portal_enter.play()
                        for i in range(43):
                            if i == 35:
                                mirror_breaks.play()
                            screen.blit(lobby, (0, 0))
                            portal_breaks.draw(screen)
                            portal_breaks.update()
                            pygame.display.flip()
                            clock.tick(10)
                        end_scene = True
                    else:
                        x, y = hero.update(go_where, move=False)
                        if not hero.second_room:
                            screen.blit(lobby, (0, 0))
                            if kitchen_titles_second_shown and not lobby_titles_shown:
                                screen.blit(death, (0, 0))
                            elif lobby_titles_shown:
                                portal.draw(screen)
                                portal.update()
                        else:
                            screen.blit(kitchen, (0, 0))
                            screen.blit(cupcake, (975, 250))
                        all_sprites.draw(screen)
                        if hero.second_room and 100 <= x <= 200 and not kitchen_titles_shown:
                            if SOUND_TITLES:
                                kitchen_titles_shown, pressed_enter = \
                                    kitchen_titles.update(screen,
                                                          clock,
                                                          pressed_enter,
                                                          typing,
                                                          end_typing)
                            else:
                                kitchen_titles_shown, pressed_enter = \
                                    kitchen_titles.update(screen,
                                                          clock,
                                                          pressed_enter)
                            if kitchen_titles_shown:
                                show_titles = False
                                pressed_enter = False
                                house_door_open.play()
                                house_door_close.play()
                                clock.tick(0.5)
                        if hero.second_room and 100 <= x <= 200 and kitchen_titles_shown and \
                                not kitchen_titles_second_shown:
                            if SOUND_TITLES:
                                kitchen_titles_second_shown, pressed_enter = \
                                    kitchen_titles_second.update(
                                        screen,
                                        clock,
                                        pressed_enter,
                                        typing,
                                        end_typing)
                            else:
                                kitchen_titles_second_shown, pressed_enter = \
                                    kitchen_titles_second.update(
                                        screen,
                                        clock,
                                        pressed_enter)
                            if kitchen_titles_second_shown:
                                show_titles = False
                                pressed_enter = False
                        if not hero.second_room and kitchen_titles_second_shown and 800 <= x <= 900 \
                                and not lobby_titles_shown:
                            if SOUND_TITLES:
                                lobby_titles_shown, pressed_enter = lobby_titles.update(
                                    screen,
                                    clock,
                                    pressed_enter,
                                    typing,
                                    end_typing)
                            else:
                                lobby_titles_shown, pressed_enter = lobby_titles.update(
                                    screen,
                                    clock,
                                    pressed_enter)
                            if lobby_titles_shown:
                                show_titles = False
                                pressed_enter = False
        else:
            hero.pause()
            for elem in [first_titles, additional_titles, kitchen_titles, kitchen_titles_second,
                         lobby_titles]:
                elem.pause(typing, end_typing)
            pause_screen.update(time_delta, screen, manager_pause)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
if not deleted_files:
    for name in names_freddy:
        os.remove(os.path.join(directory, name))
