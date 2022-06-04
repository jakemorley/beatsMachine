import pygame


class BeatGUI:
    __DEF_WIDTH = 1400
    __DEF_HEIGHT = 800
    __DEF_BLACK = (0, 0, 0)
    __DEF_WHITE = (255, 255, 255)
    __DEF_GRAY = (128, 128, 128)
    __DEF_GREEN = (0, 255, 0)
    __DEF_GOLD = (212, 175, 55)
    __DEF_FPS = 60
    __DEF_OFFSET = 100
    __DEF_BEATS = 8

    def __init__(self, width=__DEF_WIDTH, height=__DEF_HEIGHT, fps=__DEF_FPS, beats=__DEF_BEATS):
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__beats = beats
        pygame.init()
        self.screen = pygame.display.set_mode([self.__width, self.__height])
        pygame.display.set_caption('Easy Beats Machine')
        self.label_font = pygame.font.Font('Nasa21-l23X.ttf', 32)
        self.labels = ['Hi Hat', 'Snare', 'Bass Drum', 'Crash', 'Clap', 'Floor Tom']
        self.timer = pygame.time.Clock()

    def run_gui(self):
        is_running = True
        clicked = [[-1 for _ in range(self.__beats)] for _ in self.labels]

        while is_running:
            self.timer.tick(self.__fps)
            self.screen.fill(BeatGUI.__DEF_BLACK)
            boxes = self.draw_grid(clicked)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for idx, box in enumerate(boxes):
                        print(box)
                        if box[0].collidepoint(event.pos):
                            coords = box[1]
                            clicked[coords[1]][coords[0]] *= -1

            pygame.display.flip()

        pygame.quit()

    def draw_grid(self, clicks):
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

        return boxes
