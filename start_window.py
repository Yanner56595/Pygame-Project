import pygame
import zipfile
import os
import pygame_gui
import sqlite3
from Level3 import level3
from Ending import final_level
from Introduction import introduction_level
from Nicol import level2
from Oleg import level1
from Achievements_room import show_achievements

# Инициализация
pygame.init()
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Introduction')
screen.fill((0, 0, 0))
LANGUAGE = 'Русский'

# Открытие файла с картинками для заставки
fname = os.path.join(os.getcwd(), 'data', 'Snow.zip')
directory = os.path.join(os.getcwd(), 'data')
with zipfile.ZipFile(fname, "r") as f:
    names = f.namelist()
    f.extractall(directory)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def draw_name():
    font = pygame.font.Font(None, 85)
    text = font.render("Однажды в Рождество" * (LANGUAGE == 'Русский') +
                       "One Christmas Eve" * (LANGUAGE == 'English'), True, "#84DFFF")
    text_x = width // 2 - text.get_width() // 2
    text_y = (height // 2 - text.get_height() // 2) // 2
    screen.blit(text, (text_x, text_y))


def update_results():
    global result, name_users
    result = cur.execute("""SELECT UserId FROM Name_users""").fetchall()
    name_users = cur.execute("""SELECT NameUser FROM Name_users""").fetchall()


def game(place, nowuser):
    global size, screen, width, height
    if place == 1:
        result, achievements = introduction_level(LANGUAGE, size, width, height)
        if achievements:
            pass
        while result == 1:
            result, achievements = introduction_level(LANGUAGE, size, width, height)
            if achievements:
                pass
        if result == 3:
            userid = cur.execute(f"""SELECT UserId FROM Name_users WHERE NameUser == '{
            nowuser}'""").fetchall()[0][0]
            cur.execute(
                f"""INSERT INTO Users_and_Saves(UserId, SaveId) VALUES({
                userid}, 2)""").fetchall()
            con.commit()
            place += 1
    if place == 2:
        userid = cur.execute(f"""SELECT UserId FROM Name_users WHERE NameUser == '{
        nowuser}'""").fetchall()[0][0]
        result = level1(LANGUAGE, userid)
        if result in (2, 3):
            cur.execute(
                f"""INSERT INTO Users_and_Saves(UserId, SaveId) VALUES({
                userid}, 3)""").fetchall()
            con.commit()
            if result == 3:
                place += 1
        screen = pygame.display.set_mode(size)
    if place == 3:
        pygame.display.set_caption('Level 2')
        result = level2(LANGUAGE)
        if result in (2, 3):
            userid = cur.execute(f"""SELECT UserId FROM Name_users WHERE NameUser == '{
            nowuser}'""").fetchall()[0][0]
            cur.execute(
                f"""INSERT INTO Users_and_Saves(UserId, SaveId) VALUES({
                userid}, 4)""").fetchall()
            con.commit()
            if result == 3:
                place += 1
        size = width, height = 1000, 650
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Introduction')
    if place == 4:
        result, achievements = level3(LANGUAGE, size, width, height)
        if achievements:
            pass
        while result == 1:
            result, achievements = level3(LANGUAGE, size, width, height)
            if achievements:
                pass
        if result == 3:
            userid = cur.execute(f"""SELECT UserId FROM Name_users WHERE NameUser == '{
            nowuser}'""").fetchall()[0][0]
            cur.execute(
                f"""INSERT INTO Users_and_Saves(UserId, SaveId) VALUES({
                userid}, 5)""").fetchall()
            con.commit()
            place += 1
    if place == 5:
        result = final_level(LANGUAGE, size, width, height)
        while result == 1:
            result = level3(LANGUAGE, size, width, height)
        if result == 3:
            userid = cur.execute(f"""SELECT UserId FROM Name_users WHERE NameUser == '{
            nowuser}'""").fetchall()[0][0]
            cur.execute(
                f"""INSERT INTO Users_and_Saves(UserId, SaveId) VALUES({
                userid}, 6)""").fetchall()
            con.commit()
            place += 1


# Настройка кнопок
manager = pygame_gui.UIManager((width, height))
new_game_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((75, (height - 50) / 2, 250, 50)),
    text='Начать новую игру' * (LANGUAGE == 'Русский') + "Start new game" * (LANGUAGE == 'English'),
    manager=manager
)
choose_language = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['Русский', 'English'], starting_option='Русский',
    relative_rect=pygame.Rect(900, 582, 100, 25), manager=manager
)
continue_game_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, (height - 50) / 2, 300, 50)),
    text='Продолжить с последнего сохранения' * (LANGUAGE == 'Русский') + "Continue game" * (
            LANGUAGE == 'English'),
    manager=manager
)
ach_game_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((675, (height - 50) / 2, 250, 50)),
    text='Зал достижений' * (LANGUAGE == 'Русский') + "Hall of Achievements" * (
            LANGUAGE == 'English'),
    manager=manager
)
# Музыка
sound_main_button = pygame.mixer.Sound(os.path.join(directory, 'Start game.wav'))
window_sound = pygame.mixer.Sound(os.path.join(directory, 'Main window music.mp3'))
window_sound.play(-1)
con = sqlite3.connect(os.path.join(directory, 'Users.db'))
cur = con.cursor()
result = list(map(lambda x: x[0], cur.execute("""SELECT UserId FROM Name_users""").fetchall()))
name_users = list(map(lambda x: x[0], cur.execute("""SELECT NameUser FROM Name_users"""
                                                  ).fetchall()))
if len(result) == 0:
    continue_game_button.disable()
    ach_game_button.disable()
    choose_user = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['No user'], starting_option='No user',
        relative_rect=pygame.Rect(350, (height - 50) / 2 + 70, 575, 30), manager=manager
    )
else:
    choose_user = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['No user'] + name_users, starting_option='No user',
        relative_rect=pygame.Rect(350, (height - 50) / 2 + 70, 575, 30), manager=manager
    )
entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(75, (height - 50) / 2 + 70, 250, 30), manager=manager
)
new_user_name = ''
now_user = 'No user'
continue_game_button.disable()
ach_game_button.disable()
i = 0
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                rect=pygame.Rect(width / 2 - 150, height / 2 - 100, 300, 200),
                manager=manager,
                window_title='Подтверждение' * (LANGUAGE == 'Русский') +
                             'Confirmation' * (LANGUAGE == 'English'),
                action_long_desc='Вы уверены, что хотите выйти?' * (LANGUAGE == 'Русский') +
                                 'Are you sure you want to leave?' * (LANGUAGE == 'English'),
                action_short_name='OK',
                blocking=True
            )
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                running = False
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                new_user_name = event.text
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.text in ('Русский', 'English'):
                    LANGUAGE = event.text
                    new_game_button.kill()
                    new_game_button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((75, (height - 50) / 2, 250, 50)),
                        text='Начать новую игру' * (LANGUAGE == 'Русский') + "Start new game" * (
                                    LANGUAGE == 'English'),
                        manager=manager
                    )
                    continue_game_button.kill()
                    continue_game_button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((350, (height - 50) / 2, 300, 50)),
                        text='Продолжить с последнего сохранения' * (
                                    LANGUAGE == 'Русский') + "Continue game" * (
                                         LANGUAGE == 'English'),
                        manager=manager
                    )
                    ach_game_button.kill()
                    ach_game_button = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((675, (height - 50) / 2, 250, 50)),
                        text='Зал достижений' * (LANGUAGE == 'Русский') + "Hall of Achievements" * (
                                    LANGUAGE == 'English'),
                        manager=manager
                    )
                    if len(result) == 0:
                        continue_game_button.disable()
                        ach_game_button.disable()
                else:
                    now_user = event.text
                    if now_user == 'No user':
                        continue_game_button.disable()
                        ach_game_button.disable()
                    elif 6 in list(map(lambda x: x[0], cur.execute(
                            f"""SELECT SaveId FROM Users_and_Saves WHERE UserId == {
                            cur.execute(f"SELECT UserId FROM Name_users WHERE NameUser == '"
                                        f"{now_user}'").fetchall()[0][0]}""").fetchall())):
                        continue_game_button.disable()
                        ach_game_button.enable()
                    else:
                        continue_game_button.enable()
                        ach_game_button.enable()
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in (continue_game_button, ach_game_button):
                    window_sound.stop()
                    sound_main_button.play()
                if event.ui_element == continue_game_button:
                    userid = cur.execute(f"""SELECT UserId FROM Name_users WHERE NameUser == '{
                    now_user}'""").fetchall()[0][0]
                    game(max(list(map(lambda x: x[0], cur.execute(
                        f"""SELECT SaveId FROM Users_and_Saves WHERE UserId == {userid}"""
                    ).fetchall()))), now_user)
                    window_sound.play()
                    i = 0
                    pygame.display.set_caption('Introduction')
                if event.ui_element == ach_game_button:
                    show_achievements(width, height, screen, LANGUAGE, cur.execute(
                        f"""SELECT UserId FROM Name_users WHERE NameUser == '{now_user}'"""
                    ).fetchall()[0][0])
                    window_sound.play()
                    i = 0
                    pygame.display.set_caption('Introduction')
                if event.ui_element == new_game_button and new_user_name != '' and new_user_name \
                        not in name_users:
                    window_sound.stop()
                    sound_main_button.play()
                    if not result:
                        new_id = 1
                    else:
                        new_id = max(result) + 1
                    cur.execute(f"""INSERT INTO Name_users(NameUser, UserId) VALUES('{
                    new_user_name}', {new_id})""").fetchall()
                    new_usedid = cur.execute(f"""SELECT UserId FROM Name_users WHERE NameUser == '{
                    new_user_name}'""").fetchall()[0][0]
                    cur.execute(
                        f"""INSERT INTO Users_and_Saves(UserId, SaveId) VALUES({
                        new_id}, 1)""").fetchall()
                    con.commit()
                    update_results()
                    entry.kill()
                    choose_user.kill()
                    if len(result) == 0:
                        continue_game_button.disable()
                        ach_game_button.disable()
                        choose_user = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
                            options_list=['No user'], starting_option='No user',
                            relative_rect=pygame.Rect(350, (height - 50) / 2 + 70, 575, 30),
                            manager=manager
                        )
                    else:
                        choose_user = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
                            options_list=['No user'] + name_users, starting_option='No user',
                            relative_rect=pygame.Rect(350, (height - 50) / 2 + 70, 575, 30),
                            manager=manager
                        )
                    entry = pygame_gui.elements.UITextEntryLine(
                        relative_rect=pygame.Rect(75, (height - 50) / 2 + 70, 250, 30),
                        manager=manager
                    )
                    game(max(list(map(lambda x: x[0], cur.execute(
                        f"""SELECT SaveId FROM Users_and_Saves WHERE UserId == {new_usedid}"""
                    ).fetchall()))),
                         now_user)
                    window_sound.play()
                    i = 0
        manager.process_events(event)
    manager.update(time_delta)
    BackGround = Background(os.path.join(directory, names[i]), [0, 0])
    i += 1
    if i == len(names):
        i = 0
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    draw_name()
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
con.close()
for name in names:
    os.remove(os.path.join(directory, name))