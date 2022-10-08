import pygame
from pygame import mixer


class BeatGUI:
    __DEF_WIDTH = 1400
    __DEF_HEIGHT = 800
    __DEF_BLACK = (0, 0, 0)
    __DEF_WHITE = (255, 255, 255)
    __DEF_GRAY = (128, 128, 128)
    __DEF_DARKGRAY = (50, 50, 50)
    __DEF_GREEN = (0, 255, 0)
    __DEF_GOLD = (212, 175, 55)
    __DEF_BLUE = (0, 255, 255)
    __DEF_FPS = 60
    __DEF_OFFSET = 100
    __DEF_BEATS = 8

    def __init__(self, width=__DEF_WIDTH, height=__DEF_HEIGHT, fps=__DEF_FPS, beats=__DEF_BEATS):
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__beats = beats
        self.__bpm = 240
        pygame.init()
        self.screen = pygame.display.set_mode([self.__width, self.__height])
        pygame.display.set_caption('Easy Beats Machine')
        self.label_font = pygame.font.Font('Nasa21-l23X.ttf', 32)
        self.medium_font = pygame.font.Font('Nasa21-l23X.ttf', 24)
        self.labels = ['Hi Hat', 'Snare', 'Bass Drum', 'Crash', 'Clap', 'Floor Tom']
        self.timer = pygame.time.Clock()
        self.is_playing = False
        #load sounds - this should be handled differently
        self.__mixdict = {
            'Hi Hat': mixer.Sound('sounds\\hi hat (1).WAV'),
            'Snare': mixer.Sound('sounds\\snare (1).WAV'),
            'Bass Drum': mixer.Sound('sounds\\bass (1).WAV'),
            'Crash': mixer.Sound('sounds\\cymbal (1).WAV'),
            'Clap': mixer.Sound('sounds\\clap (1).WAV'),
            'Floor Tom': mixer.Sound('sounds\\tom (1).WAV')
        }

        pygame.mixer.set_num_channels(len(self.labels * 3)) # three channels per instrument

    def run_gui(self):
        is_running = True
        self.is_playing = True
        clicked = [[-1 for _ in range(self.__beats)] for _ in self.labels]
        active_len = 0
        active_beat = 1
        beat_changed = True

        while is_running:
            self.timer.tick(self.__fps)
            self.screen.fill(BeatGUI.__DEF_BLACK)
            boxes = self.draw_grid(clicked, active_beat)
            play_pause = self.draw_menu()

            if beat_changed:
                self.play_notes(clicked, active_beat)
                beat_changed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for idx, box in enumerate(boxes):
                        print(box)
                        if box[0].collidepoint(event.pos):
                            coords = box[1]
                            clicked[coords[1]][coords[0]] *= -1
                if event.type == pygame.MOUSEBUTTONUP:
                    if play_pause.collidepoint(event.pos):
                        if self.is_playing:
                            self.is_playing = False
                        elif not self.is_playing:
                            self.is_playing=True



            beat_len = BeatGUI.__DEF_FPS * 60 // self.__bpm  # the magic number 60 is to convert frames per second to frames per minute

            if self.is_playing:
                if active_len < beat_len:
                    active_len += 1
                else:
                    active_len = 0
                    if active_beat < self.__beats - 1:
                        active_beat += 1
                        beat_changed = True
                    else:
                        active_beat = 0
                        beat_changed = True

            pygame.display.flip()

        pygame.quit()

    def draw_grid(self, clicks, active_beat):
        left_box = pygame.draw.rect(self.screen, BeatGUI.__DEF_GRAY, [0, 0, 200, self.__height - 200], 5)
        btm_box = pygame.draw.rect(self.screen, BeatGUI.__DEF_GRAY, [0, self.__height - 200, self.__width, 200], 5)
        boxes = []
        colors = [BeatGUI.__DEF_GRAY, BeatGUI.__DEF_WHITE, BeatGUI.__DEF_GRAY]

        label_dict = dict()

        for idx, label in enumerate(self.labels):
            label_dict[label] = self.label_font.render(label, True, BeatGUI.__DEF_WHITE)
            self.screen.blit(label_dict[label], (30, 30 + idx * BeatGUI.__DEF_OFFSET))
            pygame.draw.line(self.screen, BeatGUI.__DEF_GRAY,
                             (0, (idx + 1) * BeatGUI.__DEF_OFFSET), (200, (idx + 1) * BeatGUI.__DEF_OFFSET), 3)

        for beat in range(self.__beats):
            for idx, label in enumerate(self.labels):
                color = BeatGUI.__DEF_GRAY
                if clicks[idx][beat] == 1:
                    color = BeatGUI.__DEF_GREEN

                # three tiered rectangles
                rect = pygame.draw.rect(self.screen, color,
                                        [beat * ((self.__width - 200) // self.__beats) + 205,
                                         idx * BeatGUI.__DEF_OFFSET + 5,
                                         (self.__width - 200) // self.__beats - 10,
                                         (self.__height - 200) // len(self.labels) - 10],
                                        0, 3)
                pygame.draw.rect(self.screen, BeatGUI.__DEF_GOLD,
                                 [beat * ((self.__width - 200) // self.__beats) + 200,
                                  idx * BeatGUI.__DEF_OFFSET,
                                  (self.__width - 200) // self.__beats,
                                  (self.__height - 200) // len(self.labels)],
                                 5, 5)
                pygame.draw.rect(self.screen, BeatGUI.__DEF_BLACK,
                                 [beat * ((self.__width - 200) // self.__beats) + 200,
                                  idx * BeatGUI.__DEF_OFFSET,
                                  (self.__width - 200) // self.__beats,
                                  (self.__height - 200) // len(self.labels)],
                                 2, 5)
                boxes.append((rect, (beat, idx)))

            active = pygame.draw.rect(self.screen, BeatGUI.__DEF_BLUE,
                                          [active_beat * ((self.__width - 200) // self.__beats) + 200,
                                           0,
                                           ((self.__width - 200) // self.__beats),
                                           len(self.labels) * 100],
                                          5, 3)

        return boxes

    def draw_menu(self):
        play_pause = pygame.draw.rect(self.screen, BeatGUI.__DEF_GRAY,
                                      [50,
                                       self.__height - 150,
                                       200,
                                       100
                                      ],
                                      0, 5)
        play_text = self.label_font.render('Play/Pause', True, BeatGUI.__DEF_WHITE)

        bpm_rect = pygame.draw.rect(self.screen, BeatGUI.__DEF_GRAY,
                                    [300,
                                     self.__height - 150,
                                     200,
                                     100
                                    ],
                                    5, 5)
        bpm_text = self.medium_font.render('Beats Per Minute', True, BeatGUI.__DEF_WHITE)
        bp_text2 = self.label_font.render(f'{self.__bpm}', True, BeatGUI.__DEF_WHITE)

        self.screen.blit(play_text, (70, self.__height - 130))
        self.screen.blit(bpm_text, (308, self.__height - 130))
        self.screen.blit(bp_text2, (370, self.__height - 100))
        if self.is_playing:
            lower_play_text = self.medium_font.render('Playing', True, BeatGUI.__DEF_DARKGRAY)
        else:
            lower_play_text = self.medium_font.render('Paused', True, BeatGUI.__DEF_DARKGRAY)
        self.screen.blit(lower_play_text, (80, self.__height - 100))
        return play_pause


    def play_notes(self, clicked, active_beat):
        for idx, val in enumerate(clicked):
            if val[active_beat] == 1:
                cur_mixer = self.__mixdict[self.labels[idx]]
                cur_mixer.play()




