import pygame
import sys
import os
import pygame_gui
from Titles_show import Titles
from Pause import Pause


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


def final_level(LANGUAGE, size, width, height):
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('The end')
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    directory = os.path.join(os.getcwd(), 'data')
    SOUND_TITLES = True
    stayLeft = pygame.transform.scale(load_image('L5_mainhero.png'), (180, 330))
    kitchen = pygame.transform.scale(load_image('Christmas Night.jpg'), (width, height))
    fireworks = pygame.transform.scale(load_image('Fireworks.png'), (width, height))
    phone = pygame.mixer.Sound(os.path.join(directory, 'RingRang.mp3'))
    fireworks_sound = pygame.mixer.Sound(os.path.join(directory, 'Fireworks_sound.mp3'))
    manager_pause = pygame_gui.UIManager((width, height))
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

    end_titles = Titles(
        '[Главный герой:] Что произошло?£ '
        '[Смерть:] Я все-таки смог перенести тебя обратно. &Ты усвоил много уроков и я решил в подарок '
        'немного поменять обстановку в доме.£ ' * (
                LANGUAGE == 'Русский') +
        "[Main hero:] What happened?£ "
        "[Death:] Finally, I teleported you back. &You've learned a lot and I decided to change the "
        "situation in the house a little as a gift.£ " * (
                LANGUAGE == 'English'), width, height,
        os.path.join(directory, 'CinecavXSans-Regular.ttf'))
    end_titles_shown = False
    final_titles = Titles(
        '[Главный герой:] Алло?£ '
        '[Дочь:] Привет, пап, с Рождеством! До тебя не доходили сообщения, вот я и решила позвонить. &'
        'Я сейчас в отпуске, может мне заехать к тебе на пару деньков?£ '
        '[Главный герой:] Да, да, конечно, я буду рад провести с тобой время!£ ' * (
                LANGUAGE == 'Русский') +
        "[Main hero:] Hello?£ "
        "[Daughter:] Hi, dad, Merry Christmas! You didn't get the messages, so I decided to call. &"
        "I'm on vacation now, maybe I could stop by for a couple of days?£ "
        "[Main hero:] Oh, yes, of course, I will be glad to spend time with you!£ " * (
                LANGUAGE == 'English'), width, height,
        os.path.join(directory, 'CinecavXSans-Regular.ttf'))
    final_titles_shown = False
    typing = pygame.mixer.Sound(os.path.join(directory, 'Typing.mp3'))
    end_typing = pygame.mixer.Sound(os.path.join(directory, 'End typing.mp3'))
    pressed_enter = False
    pause = False
    x, y = 200, 487
    running = True
    FPS = 50
    x, y = 350, 300
    pause_screen = Pause(width, height)
    place = 0
    transparency = 0
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             event.key == pygame.K_ESCAPE):
                pause = not pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pressed_enter = True
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button_back_main_window_pause:
                        return 0
                    elif event.ui_element == button_last_save_pause:
                        return 1
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
            manager_pause.process_events(event)
        if pause:
            for elem in [end_titles, final_titles]:
                elem.pause(typing, end_typing)
            pause_screen.update(time_delta, screen, manager_pause)
        else:
            if not end_titles_shown:
                screen.fill('black')
                screen.blit(kitchen, (0, 0))
                screen.blit(stayLeft, (x, y))
                if SOUND_TITLES:
                    end_titles_shown, pressed_enter = end_titles.update(screen,
                                          clock, pressed_enter, 'white', typing, end_typing)
                else:
                    end_titles_shown, pressed_enter = end_titles.update(
                        screen, clock, pressed_enter, 'white')
                if end_titles_shown:
                    pressed_enter = False
                    phone.play()
                    clock.tick(1)
            elif not final_titles_shown:
                screen.fill('black')
                screen.blit(kitchen, (0, 0))
                screen.blit(stayLeft, (x, y))
                if SOUND_TITLES:
                    final_titles_shown, pressed_enter = final_titles.update(screen,
                                          clock, pressed_enter, 'white', typing, end_typing)
                else:
                    final_titles_shown, pressed_enter = final_titles.update(
                        screen, clock, pressed_enter, 'white')
                if final_titles_shown:
                    pressed_enter = False
            else:
                while place <= 650:
                    screen.fill('black')
                    screen.blit(kitchen, (0, place))
                    screen.blit(stayLeft, (x, y))
                    pygame.display.flip()
                    clock.tick(50)
                    y += 1
                    place += 1
                fireworks_sound.play()
                while transparency < 500:
                    screen.blit(fireworks, (0, 0))
                    font = pygame.font.Font(None, 90 - 15 * (LANGUAGE == 'English'))
                    text = font.render("С Новым Годом и Рождеством!" * (LANGUAGE == 'Русский') +
                                       "Happy New Year and Merry Christmas!" * (
                                               LANGUAGE == 'English'), True, "white")
                    text_x = width // 2 - text.get_width() // 2
                    text_y = (height // 2 - text.get_height() // 2)
                    text.set_alpha(transparency)
                    screen.blit(text, (text_x, text_y))
                    pygame.display.flip()
                    clock.tick(25)
                    transparency += 2
                clock.tick(0.3)
                return 3
        pygame.display.flip()
        clock.tick(FPS)