import sqlite3
import pygame
import os
import sys


def show_achievements(width, height, screen, LANGUAGE, user_id):
    global x, outside, inside, show_titles, running
    pygame.display.set_caption('Achievements')
    screen.fill((0, 0, 0))
    FPS = 50
    clock = pygame.time.Clock()
    directory = os.path.join(os.getcwd(), 'data')

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

    class Hero(pygame.sprite.Sprite):
        def __init__(self, x, y, where, *group):
            super().__init__(*group)
            self.i = 0
            self.where = where
            if where == 'right':
                self.image = pygame.transform.scale(stay_right, (100, 163))
            else:
                self.image = pygame.transform.scale(stay_left, (100, 163))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.play = 0
            self.second_room = False
            self.were = [0]

        def update(self, where, move=True):
            global x, outside, inside, show_titles, running
            x_new = x
            if move:
                tm = pygame.time.get_ticks() // 100
                if tm not in self.were:
                    self.i += 1
                    del self.were[-1]
                    self.were.append(tm)
                self.i = self.i % len(walk_right)
                if self.where != where:
                    self.i = 0
                    self.where = where
                if where == 'right':
                    self.image = pygame.transform.scale(walk_right[self.i], (100, 163))
                    x_new += 4
                else:
                    self.image = pygame.transform.scale(walk_left[self.i], (100, 163))
                    x_new -= 4
            else:
                self.i = 0
                if where == 'right':
                    self.image = pygame.transform.scale(stay_right, (100, 163))
                else:
                    self.image = pygame.transform.scale(stay_left, (100, 163))
            self.mask = pygame.mask.from_surface(self.image)
            if x_new < -120:
                running = False
            x_new = min(x_new, 2588)
            return x_new, self.rect.y

    class Picture(pygame.sprite.Sprite):
        def __init__(self, x, y, im, text):
            super().__init__(all_sprites)
            self.place_x = x
            self.image = pygame.transform.scale(load_image(im), (300, 300))
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.text = font.render(text, True, 'black')
            self.text_x = self.place_x - x
            self.text_y = y + 310
            self.add(pictures)

        def update(self):
            global x
            self.rect.x = self.place_x - x
            self.text_x = self.place_x - x
            screen.blit(self.text, (self.text_x, self.text_y))

    walk_left = [load_image('D1.png'), load_image('D2.png'),
                 load_image('D3.png'), load_image('D4.png'), load_image('D5.png'),
                 load_image('D6.png')]
    walk_right = [pygame.transform.flip(load_image('D1.png'), 90, 0),
                  pygame.transform.flip(load_image('D2.png'), 90, 0),
                  pygame.transform.flip(load_image('D3.png'), 90, 0),
                  pygame.transform.flip(load_image('D4.png'), 90, 0),
                  pygame.transform.flip(load_image('D5.png'), 90, 0),
                  pygame.transform.flip(load_image('D6.png'), 90, 0)]
    stay_left = load_image('D2.png')
    stay_right = pygame.transform.flip(load_image('D2.png'), 90, 0)
    bg = pygame.transform.scale(load_image('Achievement room.jpg'), (width, height))
    font = pygame.font.Font(os.path.join(directory, 'CinecavXSans-Regular.ttf'), 20)

    con = sqlite3.connect(os.path.join(directory, 'Users.db'))
    cur = con.cursor()
    achievements_user = list(map(lambda x: x[0], cur.execute(
        f"""SELECT AchId FROM Users_and_Achievements WHERE UserId == {user_id}""").fetchall()))
    all_sprites = pygame.sprite.Group()
    pictures = pygame.sprite.Group()
    y_pictures = 100
    for i in range(8):
        if i == 0:
            if 1 in achievements_user:
                Picture(100 + i * 350, y_pictures, 'Gold medal.png', cur.execute(f"""SELECT {
                'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
                } FROM Achievements WHERE AchId == 1""").fetchall()[0][0])
            elif 2 in achievements_user:
                Picture(100 + i * 350, y_pictures, 'Silver medal.png', cur.execute(f"""SELECT {
                'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
                } FROM Achievements WHERE AchId == 2""").fetchall()[0][0])
            elif 3 in achievements_user:
                Picture(100 + i * 350, y_pictures, 'Bronze medal.png', cur.execute(f"""SELECT {
                'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
                } FROM Achievements WHERE AchId == 3""").fetchall()[0][0])
        if i == 1:
            if 4 in achievements_user:
                Picture(100 + i * 350, y_pictures, 'Gold medal.png', cur.execute(f"""SELECT {
                'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
                } FROM Achievements WHERE AchId == 4""").fetchall()[0][0])
            elif 5 in achievements_user:
                Picture(100 + i * 350, y_pictures, 'Silver medal.png', cur.execute(f"""SELECT {
                'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
                } FROM Achievements WHERE AchId == 5""").fetchall()[0][0])
            elif 6 in achievements_user:
                Picture(100 + i * 350, y_pictures, 'Bronze medal.png', cur.execute(f"""SELECT {
                'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
                } FROM Achievements WHERE AchId == 6""").fetchall()[0][0])
        if i == 2 and 7 in achievements_user:
            Picture(100 + i * 350, y_pictures, 'First Cupcake.png', cur.execute(f"""SELECT {
            'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
            } FROM Achievements WHERE AchId == 7""").fetchall()[0][0])
        elif 7 not in achievements_user and i == 2:
            Picture(100 + i * 350, y_pictures, 'Question mark.png', '???')
        if i == 3 and 8 in achievements_user:
            Picture(100 + i * 350, y_pictures, 'Freddy ach.png', cur.execute(f"""SELECT {
            'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
            } FROM Achievements WHERE AchId == 8""").fetchall()[0][0])
        elif 8 not in achievements_user and i == 3:
            Picture(100 + i * 350, y_pictures, 'Question mark.png', '???')
        if i == 4 and 9 in achievements_user:
            Picture(100 + i * 350, y_pictures, 'Out ach.png', cur.execute(f"""SELECT {
            'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
            } FROM Achievements WHERE AchId == 9""").fetchall()[0][0])
        elif 9 not in achievements_user and i == 4:
            Picture(100 + i * 350, y_pictures, 'Question mark.png', '???')
        if i == 5 and 10 in achievements_user:
            Picture(100 + i * 350, y_pictures, 'Sands.png', cur.execute(f"""SELECT {
            'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
            } FROM Achievements WHERE AchId == 10""").fetchall()[0][0])
        elif 10 not in achievements_user and i == 5:
            Picture(100 + i * 350, y_pictures, 'Question mark.png', '???')
        if i == 6 and 11 in achievements_user:
            Picture(100 + i * 350, y_pictures, 'Knight ach.png', cur.execute(f"""SELECT {
            'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
            } FROM Achievements WHERE AchId == 11""").fetchall()[0][0])
        elif 11 not in achievements_user and i == 6:
            Picture(100 + i * 350, y_pictures, 'Question mark.png', '???')
        if i == 7 and 12 in achievements_user:
            Picture(100 + i * 350, y_pictures, 'Happy end.png', cur.execute(f"""SELECT {
            'ForRussian' * (LANGUAGE == 'Русский') + 'ForEnglish' * (LANGUAGE == 'English')
            } FROM Achievements WHERE AchId == 12""").fetchall()[0][0])
        elif 12 not in achievements_user and i == 7:
            Picture(100 + i * 350, y_pictures, 'Question mark.png', '???')
    x, y = 200, 487
    go_where = 'right'
    hero = Hero(x, y, go_where, all_sprites)
    running = True
    while running:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            go_where = 'left'
            x, y = hero.update(go_where)
        elif keys[pygame.K_RIGHT]:
            go_where = 'right'
            x, y = hero.update(go_where)
        screen.blit(bg, (0, 0))
        for picture in pictures:
            picture.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    return 0