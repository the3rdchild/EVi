import time
import audioop
import math
import yaml
import pygame
import os
import sys
import pyaudio
from pygame import font as pygame_font

rec_dir = os.path.dirname(os.path.abspath(__file__))
EVi = os.path.join(rec_dir, '..')
sys.path.append(EVi)

from path import config, logos

print(config)

with open(config, 'r') as ymlfile:
    CFG = yaml.load(ymlfile, Loader=yaml.SafeLoader)

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                frames_per_buffer=CHUNK)

pygame.init()
screensize = (CFG['screen']['width'],
              CFG['screen']['height'])

if CFG['screen']['fullscreen'] == True:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(screensize)

pygame.display.set_caption(CFG['appName'])

pygame_font.init()
f = pygame_font.SysFont(CFG['text']['default']['font'],
                        CFG['text']['default']['size'])
f_db = pygame_font.SysFont(CFG['text']['dB']['font'],
                           CFG['text']['dB']['size'])
f_button = pygame_font.SysFont(CFG['text']['button']['font'],
                               CFG['text']['button']['size'])

pygame.mouse.set_visible(CFG['mouse']['visible'])

colors = {
    "BLACK":    (0, 0, 0),
    "GREEN":     (92, 186, 73), 
    "BLUE":    (50, 102, 173),
    "RED":      (179, 79, 70),
    "ORANGE":   (255, 92, 0),
    "YELLOW":   (255, 255, 102),
    "WHITE":    (255, 255, 255)
}

bg = colors['BLACK']

done = False
clock = pygame.time.Clock()

margin = 1
samples_per_section = int(screensize[0] / 3 - 2 * margin)

sound_tracks = [[0] * samples_per_section] * 3
max_value = [0]*3

c_db = 3

current_section = 0

ac = 0
samples = []
avg = 0
max_db = 0

logo = pygame.image.load(os.path.join(logos, 'mic.png')) #tinggal ganti dir
pygame.display.set_icon(logo)

def ag_samples(sample):
    ''' collect samples and average if needed. '''
    global ac
    global samples
    global avg
    global max_db

    if ac < 1:
        if sample > 1:
            samples.append(sample)
            ac = ac+1
    else:
        avg = sum(samples) / len(samples)
        if float(avg) > float(max_db):
            max_db = "%.2f" % avg
        ac = 0
        samples = []

    return "%.2f" % avg

def clear_all():
    ''' Clear all the variables '''
    print("Inside Clear Function")
    global sound_tracks
    global max_value
    global max_db
    global current_selection
    sound_tracks = [[0] * samples_per_section] * 3
    max_value = [0] * 3
    max_db = 0
    current_selection = 0

def get_help():
    ''' funtion to put help context on the screen '''

while not done:

    total = 0
    data = stream.read(CHUNK,
                       exception_on_overflow=False)
    reading = audioop.max(data, 2)
    total = 20 * (math.log10(abs(reading)))

    db = ag_samples(total)
    if float(db) > CFG['ranges']['red']:
        bg = colors['BLUE']
        txt = colors['BLACK']
    elif float(db) > CFG['ranges']['yellow']:
        bg = colors['YELLOW']
        txt = colors['BLACK']
    elif float(db) > CFG['ranges']['green']:
        bg = colors['BLACK']
        txt = colors['GREEN']
    elif float(db) < CFG['ranges']['green']:
        bg = colors['BLACK']
        txt = colors['WHITE']

    screen.fill(colors[CFG['screen']['bg_color']])

    pygame.draw.rect(screen,
                     bg,
                     (screensize[0] / 3 + margin, 100,
                      (screensize[0] / 3) * 2,
                      screensize[1] - 100)) 
    text = f_db.render("%s dB"%db, True, txt, bg) # the val is 'db'
    screen.blit(text,
                [screensize[0] - (screensize[0] / 1.75),
                 screensize[1] / 2])

    sound_tracks[current_section] = sound_tracks[current_section][1:] + [total]
    max_value[current_section] = max(max_value[current_section], total)

    i = 0
    sectionx = i * screensize[0] / 3 + margin
    pygame.draw.rect(screen,
                     colors['BLUE'],
                     (sectionx,
                      screensize[1] - (max_value[i] * 5),
                      screensize[0] / 3 - 2 * margin,
                      max_value[i] * 5))

    text_peak = f.render("Peak: %s"%max_db,
                         True,
                         colors['WHITE'],
                         colors['BLACK'])

    screen.blit(text_peak,
                [screensize[0] -
                 (screensize[0] / 1.75),
                 10])

    for j in range(0, int(screensize[0] / 3) - 2 * margin):
        x = j + sectionx
        y = screensize[1] - (sound_tracks[i][j] * 5)
        pygame.draw.rect(screen,
                         colors['RED'],
                         (x, y, 1,
                          screensize[1] - margin))

    screen.blit(logo, (5, 5))

    pygame.draw.lines(screen,
                      colors['GREEN'],
                      True,
                      [(0, 0),
                       (screensize[0], 0),
                       (screensize[0],
                        screensize[1]),
                       (0, screensize[1])]) #(C,R)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clear_all()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True
            elif event.key == pygame.K_c:
                clear_all()
            elif event.key == pygame.K_h:
                get_help()


    time.sleep(.005)

pygame_font.quit()
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()

