import pygame


class Titles:
    def __init__(self, text, width, height, directory):
        self.text = text
        self.i = 0
        self.shown = [[]]
        self.width = width
        self.height = height
        self.wait = False
        self.font = directory
        self.play = 0

    def update(self, screen, clock, pressed_enter, color, typing=None, end_typing=None):
        if not self.wait:
            if not self.play and typing:
                typing.play(-1)
                self.play = 1
            self.shown[-1] += self.text[self.i]
            self.i += 1
            if self.shown[-1][-1] == '[':
                del self.shown[-1][-1]
                self.shown[-1] += self.text[self.i]
                self.i += 1
                while self.shown[-1][-1] != ']':
                    self.shown[-1] += self.text[self.i]
                    self.i += 1
                del self.shown[-1][-1]
                self.shown[-1] += self.text[self.i]
            elif self.shown[-1][-1] == '|':
                if typing:
                    typing.stop()
                    self.play = 0
                clock.tick(3)
                del self.shown[-1][-1]
            elif self.shown[-1][-1] == '£':
                pressed_enter = False
                self.wait = True
                del self.shown[-1][-1]
                self.play = 0
                if typing:
                    typing.stop()
                    end_typing.play()
            elif self.shown[-1][-1] == '&':
                del self.shown[-1][-1]
                self.shown.append([])
        else:
            if pressed_enter:
                self.wait = False
                self.shown = [[]]
                if self.i >= len(self.text):
                    return False
        font = pygame.font.Font(self.font, 20)
        if len(self.shown) == 1:
            dp = 0
            place_y = 600
        elif len(self.shown) == 2:
            dp = 35
            place_y = 580
        elif len(self.shown) == 3:
            dp = 35
            place_y = 555
        for line in self.shown:
            text = font.render(''.join(line), True, color)
            text_x = self.width // 2 - text.get_width() // 2
            text_y = place_y
            screen.blit(text, (text_x, text_y))
            place_y += dp
        clock.tick(20)
        if self.i >= len(self.text) and typing:
            self.play = 0
            typing.stop()
        return self.i >= len(self.text), pressed_enter

    def pause(self, typing, end_typing):
        self.play = 0
        typing.stop()
        end_typing.stop()